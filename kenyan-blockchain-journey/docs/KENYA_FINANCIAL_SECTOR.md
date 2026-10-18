# Connecting the learning project to Kenya's financial sector

The long-term goal behind this learning journey is to understand whether blockchain and related cryptographic tools can help solve real problems in Kenya's financial sector. This repository is a foundation for research and discussion, not a deployment proposal.

## Problem areas worth studying

### 1. Inter-institution reconciliation
Banks, payment providers and other institutions may need to reconcile records across separate systems. A shared, permissioned, tamper-evident event log could be investigated where governance and access rules are agreed.

Questions to research:
- Which reconciliation step is slow or costly?
- Who is allowed to write, read, correct or dispute an entry?
- Would an API and shared database solve the problem more simply?

### 2. Cross-border payments
Explore whether better status visibility and standardized messages could reduce uncertainty across payment providers. A blockchain is only one possible component; foreign exchange, liquidity, compliance, settlement finality and consumer protection remain central.

### 3. Audit trails and fraud controls
Cryptographic hashes can help reveal whether records changed after being committed. They do not prove that the original input was truthful, and they do not prevent fraud by themselves.

### 4. Verifiable credentials
Digital signatures can help verify that a credential was issued by a known authority. Personal data should not be placed on a public immutable chain. Consider storing minimal proofs and keeping sensitive records off-chain.

## Responsible design principles

- Start with a clearly defined user problem, not with the assumption that blockchain is required.
- Minimize personal data and protect confidentiality.
- Define governance, liability, dispute handling and correction procedures.
- Design for accessibility, low-cost devices, intermittent connectivity and local language needs.
- Consider consumer protection, operational resilience and regulatory obligations.
- Measure outcomes against a conventional database/API baseline.
- Do not claim compliance or regulatory approval without qualified review.

## A practical future portfolio project

**Prototype idea: Payment Reconciliation Audit Trail**

Create a local demo in which two fictional institutions submit payment-event hashes and compare event status. Keep personal information off-chain. Measure:
- duplicate-event detection;
- mismatch identification;
- audit history;
- reconciliation time in a controlled test;
- usability and operational trade-offs.

A later version could compare a conventional relational database with a permissioned-ledger design. The key deliverable would be an evidence-based comparison, not a claim that blockchain is always superior.
