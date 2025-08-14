from enum import Enum
from typing import Any, Dict, Optional, Union

from pydantic import Field
from tau2.environment.db import DB
from tau2.utils.pydantic_utils import BaseModelNoExtra, update_pydantic_model_with_dict


# Enums for common states
class CardStatus(str, Enum):
    ACTIVE = "active"
    BLOCKED = "blocked"
    EXPIRED = "expired"


class AccountType(str, Enum):
    SAVINGS = "savings"
    CHECKING = "checking"
    CREDIT = "credit"


class TransactionStatus(str, Enum):
    PENDING = "pending"
    CLEARED = "cleared"
    DISPUTED = "disputed"


# Nested models
class Account(BaseModelNoExtra):
    account_id: str
    account_type: AccountType
    balance: float
    overdraft_enabled: bool = False


class Card(BaseModelNoExtra):
    card_id: str
    linked_account: str
    status: CardStatus = CardStatus.ACTIVE
    credit_limit: Optional[float] = None
    current_usage: Optional[float] = 0.0


class Transaction(BaseModelNoExtra):
    transaction_id: str
    amount: float
    merchant: Optional[str] = None
    status: TransactionStatus = TransactionStatus.PENDING
    card_id: Optional[str] = None
    disputed: bool = False


class PaymentSetting(BaseModelNoExtra):
    auto_pay_enabled: bool = False
    preferred_account_id: Optional[str] = None


class BankingUserDevice(BaseModelNoExtra):
    authenticated: bool = True
    has_2fa_enabled: bool = True
    login_location: Optional[str] = "domestic"
    recent_login_attempts: int = 0


class UserSurroundings(BaseModelNoExtra):
    signal_strength: str = "strong"
    is_abroad: bool = False
    network_accessible: bool = True
    device: BankingUserDevice = Field(default_factory=BankingUserDevice)


# Main user DB
class BankingUserDB(DB):
    accounts: Dict[str, Account] = Field(default_factory=dict)
    cards: Dict[str, Card] = Field(default_factory=dict)
    transactions: Dict[str, Transaction] = Field(default_factory=dict)
    payment_settings: PaymentSetting = Field(default_factory=PaymentSetting)
    surroundings: UserSurroundings = Field(default_factory=UserSurroundings)

    def update_user(self, updates: Dict[str, Any]) -> None:
        self.update_with_dict(updates)


# Instantiation helper
def get_user_db(
    initial_state: Optional[Union[BankingUserDB, Dict[str, Any]]] = None
) -> BankingUserDB:
    if initial_state is None:
        return BankingUserDB()
    if isinstance(initial_state, BankingUserDB):
        return initial_state

    try:
        user = BankingUserDB()
        return update_pydantic_model_with_dict(user, initial_state)
    except Exception as e:
        print("[BankingUserDB] Error loading user state:", e)
        return BankingUserDB()
