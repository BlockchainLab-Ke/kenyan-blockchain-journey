"""Educational account-based blockchain prototype for the Week 29 checkpoint.

This module is intentionally small enough to study. It is not production-ready.
Amounts are integer coin units. Wallet private keys are kept in memory only.
"""

from __future__ import annotations

import hashlib
import json
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec


class BlockchainError(Exception):
    """Base exception for expected blockchain application errors."""


class AmountError(BlockchainError):
    """Raised when an amount or fee is invalid."""


class InsufficientFundsError(BlockchainError):
    """Raised when a sender cannot cover an outgoing transaction."""


class InvalidTransactionError(BlockchainError):
    """Raised when a transaction fails validation."""


class BlockFullError(BlockchainError):
    """Reserved for a future maximum-transactions-per-block feature."""


def utc_timestamp() -> str:
    """Return a timezone-aware UTC timestamp as an ISO 8601 string."""
    return datetime.now(timezone.utc).isoformat()


def sha256_text(value: str) -> str:
    """Return the SHA-256 hexadecimal digest of text."""
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


class Wallet:
    """An ECC wallet whose private key signs transactions."""

    def __init__(self, owner: str):
        if not owner.strip():
            raise ValueError("Wallet owner must not be empty.")
        self.owner = owner
        self.private_key = ec.generate_private_key(ec.SECP256K1())
        self.public_key = self.private_key.public_key()
        self.address = self._generate_address()

    def _public_key_bytes(self) -> bytes:
        """Serialize the public-key object before hashing it."""
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.X962,
            format=serialization.PublicFormat.UncompressedPoint,
        )

    def _generate_address(self) -> str:
        """Create a demo address from the public key.

        This is not a standard cryptocurrency address format.
        """
        return sha256_text(self._public_key_bytes().hex())[-40:]

    def sign(self, message: str) -> bytes:
        """Sign a message using ECDSA with SHA-256."""
        return self.private_key.sign(
            message.encode("utf-8"),
            ec.ECDSA(hashes.SHA256()),
        )

    def export_public_key_pem(self) -> str:
        """Return a shareable PEM public key; never export private keys here."""
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode("utf-8")


@dataclass
class Transaction:
    """A signed transfer between accounts, or a special mining reward."""

    sender: str
    receiver: str
    amount: int
    fee: int = 0
    timestamp: str = field(default_factory=utc_timestamp)
    transaction_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    signature: Optional[bytes] = None
    public_key_pem: Optional[str] = None
    is_reward: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.amount, int) or isinstance(self.amount, bool):
            raise AmountError("Amount must be an integer coin amount.")
        if self.amount <= 0:
            raise AmountError("Amount must be greater than zero.")
        if not isinstance(self.fee, int) or isinstance(self.fee, bool) or self.fee < 0:
            raise AmountError("Fee must be a non-negative integer.")
        if not self.sender or not self.receiver:
            raise InvalidTransactionError("Sender and receiver are required.")
        if self.is_reward and self.fee != 0:
            raise InvalidTransactionError("Reward transactions cannot pay a fee.")

    def signing_payload(self) -> str:
        """Return the stable transaction fields covered by the signature."""
        return json.dumps(
            {
                "transaction_id": self.transaction_id,
                "sender": self.sender,
                "receiver": self.receiver,
                "amount": self.amount,
                "fee": self.fee,
                "timestamp": self.timestamp,
                "is_reward": self.is_reward,
            },
            sort_keys=True,
            separators=(",", ":"),
        )

    def sign(self, wallet: Wallet) -> None:
        """Attach the wallet's public key and signature to this transaction."""
        if self.is_reward:
            raise InvalidTransactionError("Reward transactions are not signed by users.")
        if wallet.address != self.sender:
            raise InvalidTransactionError("The signing wallet does not own the sender address.")
        self.public_key_pem = wallet.export_public_key_pem()
        self.signature = wallet.sign(self.signing_payload())

    def verify_signature(self) -> bool:
        """Verify the signature and confirm the public key derives this sender address."""
        if self.is_reward:
            return self.signature is None and self.public_key_pem is None
        if not self.signature or not self.public_key_pem:
            return False
        try:
            public_key = serialization.load_pem_public_key(
                self.public_key_pem.encode("utf-8")
            )
            if not isinstance(public_key, ec.EllipticCurvePublicKey):
                return False
            encoded = public_key.public_bytes(
                encoding=serialization.Encoding.X962,
                format=serialization.PublicFormat.UncompressedPoint,
            )
            derived_address = sha256_text(encoded.hex())[-40:]
            if derived_address != self.sender:
                return False
            public_key.verify(
                self.signature,
                self.signing_payload().encode("utf-8"),
                ec.ECDSA(hashes.SHA256()),
            )
            return True
        except (InvalidSignature, ValueError, TypeError):
            return False

    def to_dict(self) -> dict:
        """Convert transaction data to JSON-compatible values."""
        return {
            "transaction_id": self.transaction_id,
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "fee": self.fee,
            "timestamp": self.timestamp,
            "signature": self.signature.hex() if self.signature else None,
            "public_key_pem": self.public_key_pem,
            "is_reward": self.is_reward,
        }


@dataclass
class Block:
    """A group of transactions linked to the preceding block."""

    index: int
    transactions: list[Transaction]
    previous_hash: str
    difficulty: int
    timestamp: str = field(default_factory=utc_timestamp)
    nonce: int = 0
    hash: str = ""

    def hash_payload(self) -> str:
        """Serialize block header and transaction data deterministically."""
        payload = {
            "index": self.index,
            "transactions": [tx.to_dict() for tx in self.transactions],
            "previous_hash": self.previous_hash,
            "difficulty": self.difficulty,
            "timestamp": self.timestamp,
            "nonce": self.nonce,
        }
        return json.dumps(payload, sort_keys=True, separators=(",", ":"))

    def calculate_hash(self) -> str:
        return sha256_text(self.hash_payload())

    def mine(self) -> str:
        """Increment nonce until the hash satisfies the configured difficulty."""
        target = "0" * self.difficulty
        while True:
            candidate = self.calculate_hash()
            if candidate.startswith(target):
                self.hash = candidate
                return candidate
            self.nonce += 1


class Blockchain:
    """A local account-based chain with a pending transaction pool."""

    def __init__(
        self,
        difficulty: int = 3,
        mining_reward: int = 10,
        max_supply: int = 1_000_000,
        halving_interval: int = 100,
        genesis_allocations: Optional[dict[str, int]] = None,
    ):
        if difficulty < 0 or difficulty > 5:
            raise ValueError("For this demo, difficulty must be between 0 and 5.")
        if mining_reward < 0 or max_supply <= 0 or halving_interval <= 0:
            raise ValueError("Reward must be non-negative; supply and interval must be positive.")
        self.difficulty = difficulty
        self.initial_mining_reward = mining_reward
        self.max_supply = max_supply
        self.halving_interval = halving_interval
        self.total_issued = 0
        self.balances: dict[str, int] = {}
        self.pending_transactions: list[Transaction] = []
        self.chain: list[Block] = []
        self._create_genesis_block(genesis_allocations or {})

    def _create_genesis_block(self, allocations: dict[str, int]) -> None:
        """Create the first block and optional demo balances."""
        for address, amount in allocations.items():
            if not isinstance(amount, int) or amount < 0:
                raise AmountError("Genesis allocations must be non-negative integers.")
            if not address:
                raise InvalidTransactionError("Genesis allocation address cannot be empty.")
            self.balances[address] = self.balances.get(address, 0) + amount
            self.total_issued += amount
        if self.total_issued > self.max_supply:
            raise AmountError("Genesis allocations exceed maximum supply.")
        genesis = Block(
            index=0,
            transactions=[],
            previous_hash="0" * 64,
            difficulty=self.difficulty,
        )
        genesis.mine()
        self.chain.append(genesis)

    @property
    def latest_block(self) -> Block:
        return self.chain[-1]

    def get_balance(self, wallet_or_address: Wallet | str) -> int:
        address = wallet_or_address.address if isinstance(wallet_or_address, Wallet) else wallet_or_address
        return self.balances.get(address, 0)

    def get_available_balance(self, wallet_or_address: Wallet | str) -> int:
        """Balance after accounting for outgoing transactions already in the pool."""
        address = wallet_or_address.address if isinstance(wallet_or_address, Wallet) else wallet_or_address
        reserved = sum(
            tx.amount + tx.fee
            for tx in self.pending_transactions
            if tx.sender == address and not tx.is_reward
        )
        return self.get_balance(address) - reserved

    def create_transaction(
        self, sender_wallet: Wallet, receiver_wallet: Wallet, amount: int, fee: int = 0
    ) -> Transaction:
        """Validate, sign, and add a transfer to the pending pool."""
        if sender_wallet.address == receiver_wallet.address:
            raise InvalidTransactionError("Sender and receiver must be different.")
        tx = Transaction(
            sender=sender_wallet.address,
            receiver=receiver_wallet.address,
            amount=amount,
            fee=fee,
        )
        if self.get_available_balance(sender_wallet) < amount + fee:
            raise InsufficientFundsError(
                f"{sender_wallet.owner} has insufficient available funds."
            )
        tx.sign(sender_wallet)
        if not tx.verify_signature():
            raise InvalidTransactionError("Transaction signature verification failed.")
        self.pending_transactions.append(tx)
        return tx

    def add_transaction(self, tx: Transaction) -> None:
        """Validate an externally supplied transaction before adding it to the pool."""
        if tx.is_reward:
            raise InvalidTransactionError("Reward transactions cannot be submitted to the pool.")
        if not tx.verify_signature():
            raise InvalidTransactionError("Invalid or missing transaction signature.")
        if self.get_available_balance(tx.sender) < tx.amount + tx.fee:
            raise InsufficientFundsError("Sender has insufficient available funds.")
        self.pending_transactions.append(tx)

    def _reward_for_next_block(self) -> int:
        """Return the reward after scheduled halvings; never negative."""
        next_height = len(self.chain)
        halvings = next_height // self.halving_interval
        return self.initial_mining_reward // (2 ** halvings)

    def mine_pending_transactions(self, miner_wallet: Wallet) -> Optional[Block]:
        """Mine pending transfers, apply them, and pay reward plus collected fees."""
        if not self.pending_transactions:
            return None

        transactions = list(self.pending_transactions)
        # Re-check sequentially against a temporary balance map before mining.
        working_balances = dict(self.balances)
        total_fees = 0
        for tx in transactions:
            if not tx.verify_signature():
                raise InvalidTransactionError("A pending transaction has an invalid signature.")
            if working_balances.get(tx.sender, 0) < tx.amount + tx.fee:
                raise InsufficientFundsError("Pending transactions overspend the sender's balance.")
            working_balances[tx.sender] -= tx.amount + tx.fee
            working_balances[tx.receiver] = working_balances.get(tx.receiver, 0) + tx.amount
            total_fees += tx.fee

        reward = min(self._reward_for_next_block(), self.max_supply - self.total_issued)
        reward_tx = None
        if reward > 0:
            reward_tx = Transaction(
                sender="NETWORK",
                receiver=miner_wallet.address,
                amount=reward,
                fee=0,
                is_reward=True,
            )
            transactions.append(reward_tx)

        block = Block(
            index=len(self.chain),
            transactions=transactions,
            previous_hash=self.latest_block.hash,
            difficulty=self.difficulty,
        )
        block.mine()

        # Commit balances only after the block has been mined successfully.
        self.balances = working_balances
        self.balances[miner_wallet.address] = self.balances.get(miner_wallet.address, 0) + total_fees
        if reward_tx:
            self.balances[miner_wallet.address] += reward
            self.total_issued += reward
        self.chain.append(block)
        self.pending_transactions.clear()
        return block

    def is_chain_valid(self) -> bool:
        """Check stored hashes, proof of work, block links, and transaction signatures."""
        if not self.chain:
            return False
        for index, block in enumerate(self.chain):
            if block.hash != block.calculate_hash():
                return False
            if not block.hash.startswith("0" * block.difficulty):
                return False
            if index == 0:
                if block.previous_hash != "0" * 64:
                    return False
            else:
                previous = self.chain[index - 1]
                if block.previous_hash != previous.hash:
                    return False
            for tx in block.transactions:
                if not tx.verify_signature():
                    return False
        return True

    def chain_summary(self) -> dict:
        """Return useful high-level information for demos and debugging."""
        return {
            "height": len(self.chain) - 1,
            "blocks": len(self.chain),
            "pending_transactions": len(self.pending_transactions),
            "total_issued": self.total_issued,
            "max_supply": self.max_supply,
            "valid": self.is_chain_valid(),
        }
