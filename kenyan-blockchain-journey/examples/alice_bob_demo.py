"""Run a small Alice-and-Bob transaction example."""

from pathlib import Path
import sys

# Allows running this file directly from the repository root without installing a package.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from blockchain import Blockchain, Wallet


def main() -> None:
    alice = Wallet("Alice")
    bob = Wallet("Bob")
    miner = Wallet("Miner")

    # Educational genesis funding; production systems need a formal issuance model.
    chain = Blockchain(
        difficulty=2,
        mining_reward=10,
        max_supply=1_000,
        halving_interval=10,
        genesis_allocations={alice.address: 50},
    )

    print("Before transaction")
    print(f"Alice: {chain.get_balance(alice)}")
    print(f"Bob:   {chain.get_balance(bob)}")
    print(f"Miner: {chain.get_balance(miner)}")

    chain.create_transaction(alice, bob, amount=20, fee=2)
    mined = chain.mine_pending_transactions(miner)

    print("\nAfter mining")
    print(f"Block mined: #{mined.index if mined else 'none'}")
    print(f"Alice: {chain.get_balance(alice)}")  # 28
    print(f"Bob:   {chain.get_balance(bob)}")    # 20
    print(f"Miner: {chain.get_balance(miner)}")  # 12: 10 reward + 2 fee
    print("Chain valid:", chain.is_chain_valid())
    print("Summary:", chain.chain_summary())


if __name__ == "__main__":
    main()
