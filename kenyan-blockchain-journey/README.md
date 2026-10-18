# Python Blockchain Journey — Weeks 1–29

A practical, educational blockchain project built while learning Python, with a long-term focus on how trustworthy shared records and digital-payment infrastructure might support Kenya's financial sector.

> **Status:** Learning prototype, not production software.  
> **Learning checkpoint:** Week 29.  
> **Primary language:** Python.  
> **Dependencies:** Python standard library plus `cryptography` for elliptic-curve wallet keys and digital signatures.

## Why this repository exists

This repository records the journey from beginner Python concepts to a small account-based blockchain prototype. It is intended to make the learning visible, reproducible, and reviewable—not to claim that a toy blockchain is ready to handle real money.

The project explores:
- transactions and validation;
- SHA-256 transaction and block hashes;
- blocks linked through previous hashes;
- Proof of Work and nonces;
- wallets using elliptic-curve cryptography;
- transaction signatures;
- pending transaction pools;
- account balances and available-balance checks;
- transaction fees and miner rewards;
- supply limits and halving-style reward logic;
- chain integrity checks and tests;
- potential financial-sector use cases in Kenya.

## Repository map

```text
kenyan-blockchain-journey/
├── README.md
├── LICENSE
├── .gitignore
├── requirements.txt
├── blockchain.py
├── examples/
│   └── alice_bob_demo.py
├── tests/
│   └── test_blockchain.py
└── docs/
    ├── LEARNING_ROADMAP.md
    ├── ARCHITECTURE.md
    ├── SECURITY_AND_LIMITATIONS.md
    └── KENYA_FINANCIAL_SECTOR.md
```

## Quick start

### 1. Install Python

Use Python 3.10 or newer. Confirm it is installed:

```bash
python --version
```

### 2. Clone the repository

Replace `YOUR-USERNAME` with your GitHub username after creating the repository:

```bash
git clone https://github.com/YOUR-USERNAME/kenyan-blockchain-journey.git
cd kenyan-blockchain-journey
```

### 3. Create and activate a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install the one external dependency

```bash
python -m pip install -r requirements.txt
```

### 5. Run the Alice and Bob example

```bash
python examples/alice_bob_demo.py
```

The example creates a small chain, funds Alice through a genesis allocation for demonstration, sends a signed transaction to Bob, mines it, and prints balances. Genesis allocation is a testing convenience—not a real-world issuance model.

### 6. Run the tests

```bash
python -m unittest discover -s tests -v
```

## Design choices

- **Account-based model:** balances are associated with wallet addresses. This preserves the model used in the learning journey so far. UTXO is a possible future study topic, not implemented here.
- **No web framework, database, or networking layer:** the code is intentionally local and small so core concepts remain visible.
- **Integer coin units:** transaction amounts are integers to avoid floating-point rounding issues in this learning prototype. A production system would define currency denomination and precision carefully.
- **ECDSA over SECP256K1:** wallet signatures use the `cryptography` package. Public keys are serialized before hashing; a public-key object itself is not text and cannot be encoded directly.
- **Proof of Work:** difficulty is represented as the number of leading zeroes required in a block hash. This is only a teaching mechanism.
- **Deterministic block payload:** block hashing uses canonical JSON serialization so the same block data produces the same hash.

## What this is—and is not

This is a local educational prototype. It does **not** include peer-to-peer networking, distributed consensus, production key storage, encrypted backups, a persistent database, a mempool policy engine, smart contracts, a formal threat model, or independent security review. It must not be used to custody funds or process real payments.

A blockchain is not automatically better than a conventional database. For many financial workflows, a well-governed database with access controls and audit logs may be more efficient. Blockchain is worth considering when multiple parties need a shared, tamper-evident record and governance can be agreed upon.

## Suggested GitHub description

**A beginner-to-intermediate Python blockchain learning project through Week 29: transactions, SHA-256, Proof of Work, ECC wallets, signatures, balances, fees, mining, and Kenyan financial-sector research.**

Suggested topics: `python`, `blockchain`, `cryptography`, `fintech`, `proof-of-work`, `kenya`, `learning-project`

## Suggested first commit

```bash
git init
git add .
git commit -m "Document blockchain learning journey through week 29"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/kenyan-blockchain-journey.git
git push -u origin main
```

Create an empty repository on GitHub first. Do not commit private keys, `.env` files, virtual environments, or real customer data.
