# Security, limitations and responsible use

## Never use this prototype for real money

This project exists to learn. It has not had an independent security audit and is not suitable for custody, settlement, customer accounts, or production payments.

## Known limitations

1. **Private-key storage:** wallet keys exist in process memory and are not encrypted, backed up, hardware-protected, or managed through a secure keystore.
2. **No networking:** there are no peers, gossip protocol, synchronization, fork choice, or distributed consensus.
3. **Local Proof of Work:** mining a block locally demonstrates nonce search; it does not make the chain secure against a network attacker.
4. **No persistent storage:** a process restart loses chain and balance state.
5. **No account registration or access-control layer:** wallet ownership is only checked through signatures in the local program.
6. **No replay protection across chains:** the signing payload has no network/chain identifier or protocol version.
7. **No duplicate-ID policy:** transaction IDs are UUIDs, but the chain does not maintain a comprehensive duplicate/replay index.
8. **No mature mempool policy:** fee prioritization, replacement, expiry and denial-of-service protections are absent.
9. **Reward accounting is simplified:** the supply cap and halving logic are educational and need deeper tests before any protocol claims.
10. **No formal monetary model:** integer units are used, but no denomination, decimal conversion, monetary policy or regulatory model is defined.
11. **No privacy features:** addresses and transfers are not confidential.
12. **No smart contracts:** transaction execution is limited to simple transfers.
13. **No distributed validation:** chain validation checks stored structure but does not reconstruct and independently replay every historical state transition from genesis.

## Security practices for a learning repository

- Never commit private keys, seed phrases, API tokens, passwords or real customer information.
- Keep secrets out of examples and screenshots.
- Use test wallets and fictitious balances only.
- Review dependencies and pin versions for reproducible releases.
- Add negative tests whenever a new validation rule is introduced.
- Treat every external transaction as untrusted input.
- For real financial use, engage qualified security, legal, compliance, and infrastructure specialists.

## A database may be the better answer

A conventional database may be better when one trusted institution controls the records, high throughput is required, or privacy and correction workflows dominate. A permissioned ledger may be worth evaluating when multiple institutions need shared, auditable updates and no single party should unilaterally control the history. The governance model matters as much as the code.
