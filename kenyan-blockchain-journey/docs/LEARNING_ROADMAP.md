# Learning Roadmap — Weeks 1–29

This is a reconstructed learning map of the concepts covered so far. The early weeks built general Python foundations; later weeks applied those skills to a growing blockchain project.

## Phase 1 — Python foundations

| Weeks | Main learning themes | Evidence in the journey |
|---|---|---|
| 1–3 | Variables, types, input/output, conditions, loops | Small exercises and basic transaction rules |
| 4–6 | Functions, lists, dictionaries, reusable logic | Balance and transaction-list operations |
| 7 | JSON and file handling | Banking account data saved and loaded as JSON |
| 8–10 | Exceptions and object-oriented programming | Custom errors, `BankAccount`, classes and properties |
| 11–13 | Composition, validation, defensive input handling | Banking-system project and composed objects |

## Phase 2 — From Python to blockchain

| Weeks | Main learning themes | Blockchain connection |
|---|---|---|
| 14–16 | Classes, object relationships, identifiers, timestamps | Transactions as objects with unique IDs |
| 17–18 | Transaction and block structure | Grouping transactions into blocks |
| 19 | Block building and mining motivation | Nonces and Proof of Work |
| 20–21 | Hashing, links, validation | SHA-256 and tamper-evident block references |
| 22–24 | Wallets and cryptography | ECC keys, addresses, signing and signature verification |
| 25–26 | Balances and transaction flow | Account state, pending transactions, insufficient-funds checks |
| 27 | Transfer accounting and validation | Updating sender/receiver balances safely |
| 28 | Fees and miner incentives | Fees collected and credited to miner |
| 29 | Integrating the educational chain | Consolidated code, testing, and design review |

## Concepts represented in the current repository

- Python classes, dataclasses, type hints, exceptions and dictionaries.
- SHA-256 hashing and deterministic JSON serialization.
- Block links, nonce search and a configurable Proof-of-Work target.
- ECC wallet keys and ECDSA signatures.
- Pending transaction pool and available-balance calculation.
- Transfer accounting, transaction fees, miner rewards and supply cap.
- Chain integrity checks and unit tests.
- Applying the technology critically to Kenyan financial-sector problems.

## Suggested next learning stage

Do not jump straight to a production network. First strengthen the current project:

1. Add persistence and reload tests, while clearly separating saved chain data from secret keys.
2. Write tests for transaction ordering, duplicate transaction IDs, reward accounting and supply edge cases.
3. Add a formal transaction/block validation pipeline.
4. Study consensus attacks and why Proof of Work in one local process is not distributed consensus.
5. Only later consider networking, peer synchronization, a UTXO model, and permissioned-ledger architecture.

Keep each change small and add tests before expanding the feature set.
