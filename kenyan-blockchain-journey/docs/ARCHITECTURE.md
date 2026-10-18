# Architecture

## High-level flow

```text
Wallet
  │ creates and signs
  ▼
Transaction ── validation ──► Pending transaction pool
                                  │
                                  ▼
                           Block construction
                                  │
                         Proof-of-Work nonce search
                                  │
                                  ▼
                         Append block to local chain
                                  │
                                  ▼
                       Apply balances and miner fees
```

## Main classes

### `Wallet`
- Creates a SECP256K1 private/public key pair.
- Derives a demo address from the serialized public key.
- Signs messages using ECDSA with SHA-256.
- Exposes the public key as PEM for verification.

### `Transaction`
- Holds sender, receiver, amount, fee, timestamp and transaction ID.
- Uses a stable JSON payload for signing.
- Verifies the signature and checks that the public key matches the sender address.
- Uses a special `is_reward` flag for a miner reward transaction.

### `Block`
- Holds an index, transactions, previous hash, difficulty, timestamp and nonce.
- Hashes a canonical JSON representation.
- Increments the nonce until the hash starts with the configured number of zeroes.

### `Blockchain`
- Creates a genesis block and optional demo allocations.
- Tracks balances and pending transactions.
- Checks available balance before adding a transfer.
- Mines pending transfers, applies fees, pays a reward and appends the block.
- Checks block hashes, proof of work, links and signatures.

## Alice and Bob accounting

Initial state:
- Alice: 50
- Bob: 0
- Miner: 0

Alice sends Bob 20 with fee 2:
- Alice pays 22 total, leaving 28.
- Bob receives 20.
- Miner receives the 2 fee plus the 10 block reward, leaving 12.

Total balances become 60 because the 10-coin mining reward is newly issued. Fees are a transfer of value from Alice to the miner, not new issuance.

## Important implementation notes

- Balances are changed only after the block has been mined, following a temporary-balance validation pass.
- The transaction pool reserves outgoing amounts when calculating available balances.
- The model is account-based. It is not a UTXO implementation.
- `total_issued` tracks the genesis allocations plus mining rewards in this prototype.
- The genesis allocation is a demonstration shortcut. A real system needs an explicit issuance and governance policy.
