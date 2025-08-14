from tau2.environment.toolkit import ToolKitBase
from tau2.environment.toolkit import is_tool, ToolType
from tau2.domains.banking.user_data_model import BankingUserDB


class BankingUserTools(ToolKitBase):
    """
    Tools for interacting with the banking environment.
    """

    db: BankingUserDB

    def __init__(self, db: BankingUserDB):
        super().__init__(db)

    def update_user(self, **kwargs):
        """Update user data with the provided key-value pairs."""
        for key, value in kwargs.items():
            if hasattr(self.db, key):
                setattr(self.db, key, value)

    @is_tool(ToolType.READ)
    def get_account_balance(self) -> str:
        """Returns current account balance."""
        if self.db.account_balance is not None:
            return f"Account balance: ${self.db.account_balance:.2f}"
        return "Account balance not available."

    @is_tool(ToolType.READ)
    def check_card_status(self) -> str:
        """Returns the status of the primary card."""
        if self.db.primary_card_active is not None:
            status = "Active" if self.db.primary_card_active else "Inactive"
            return f"Primary card status: {status}"
        return "Card status not available."

    @is_tool(ToolType.READ)
    def get_customer_info(self) -> str:
        """Returns basic customer information."""
        info = []
        if self.db.customer_id:
            info.append(f"Customer ID: {self.db.customer_id}")
        if self.db.phone_number:
            info.append(f"Phone: {self.db.phone_number}")
        if self.db.primary_account_id:
            info.append(f"Primary Account: {self.db.primary_account_id}")
        return "\n".join(info) if info else "Customer information not available."
