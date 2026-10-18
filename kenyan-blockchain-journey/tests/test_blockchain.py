"""Unit tests for the educational blockchain prototype."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from blockchain import (
    AmountError,
    Blockchain,
    InsufficientFundsError,
    InvalidTransactionError,
    Transaction,
    Wallet,
)


class BlockchainTests(unittest.TestCase):
    def setUp(self):
        self.alice = Wallet("Alice")
        self.bob = Wallet("Bob")
        self.miner = Wallet("Miner")
        self.chain = Blockchain(
            difficulty=1,
            mining_reward=10,
            max_supply=1_000,
            halving_interval=10,
            genesis_allocations={self.alice.address: 50},
        )

    def test_genesis_balance(self):
        self.assertEqual(self.chain.get_balance(self.alice), 50)
        self.assertEqual(self.chain.get_balance(self.bob), 0)

    def test_signed_transaction_and_mining(self):
        self.chain.create_transaction(self.alice, self.bob, 20, fee=2)
        block = self.chain.mine_pending_transactions(self.miner)
        self.assertIsNotNone(block)
        self.assertEqual(self.chain.get_balance(self.alice), 28)
        self.assertEqual(self.chain.get_balance(self.bob), 20)
        self.assertEqual(self.chain.get_balance(self.miner), 12)
        self.assertTrue(self.chain.is_chain_valid())

    def test_rejects_zero_or_negative_amount(self):
        with self.assertRaises(AmountError):
            Transaction(self.alice.address, self.bob.address, 0)
        with self.assertRaises(AmountError):
            Transaction(self.alice.address, self.bob.address, -1)

    def test_rejects_insufficient_funds(self):
        with self.assertRaises(InsufficientFundsError):
            self.chain.create_transaction(self.alice, self.bob, 49, fee=2)

    def test_pending_pool_reserves_balance(self):
        self.chain.create_transaction(self.alice, self.bob, 30, fee=1)
        with self.assertRaises(InsufficientFundsError):
            self.chain.create_transaction(self.alice, self.bob, 20, fee=0)

    def test_rejects_unsigned_external_transaction(self):
        tx = Transaction(self.alice.address, self.bob.address, 5)
        with self.assertRaises(InvalidTransactionError):
            self.chain.add_transaction(tx)

    def test_rejects_tampered_transaction_signature(self):
        tx = Transaction(self.alice.address, self.bob.address, 5)
        tx.sign(self.alice)
        tx.amount = 6
        self.assertFalse(tx.verify_signature())

    def test_detects_tampered_block(self):
        self.chain.create_transaction(self.alice, self.bob, 5)
        self.chain.mine_pending_transactions(self.miner)
        self.assertTrue(self.chain.is_chain_valid())
        self.chain.chain[1].transactions[0].amount = 999
        self.assertFalse(self.chain.is_chain_valid())

    def test_empty_pool_does_not_mine(self):
        self.assertIsNone(self.chain.mine_pending_transactions(self.miner))
        self.assertEqual(len(self.chain.chain), 1)

    def test_reward_respects_remaining_supply(self):
        small = Blockchain(
            difficulty=0,
            mining_reward=10,
            max_supply=55,
            halving_interval=100,
            genesis_allocations={self.alice.address: 50},
        )
        small.create_transaction(self.alice, self.bob, 1)
        small.mine_pending_transactions(self.miner)
        self.assertEqual(small.total_issued, 55)
        self.assertLessEqual(small.total_issued, small.max_supply)


if __name__ == "__main__":
    unittest.main()
