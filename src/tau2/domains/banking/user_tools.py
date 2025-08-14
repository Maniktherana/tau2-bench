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

    # --- Account Tools ---

    @is_tool(ToolType.READ)
    def get_account_balances(self) -> str:
        """Returns current balances for all accounts."""
        balances = []
        for account in self.db.accounts:
            balances.append(f"{account.account_type.title()} Account ({account.account_id}): ${account.balance:.2f}")
        return "\n".join(balances) if balances else "No accounts found."

    # --- Card Tools ---

    @is_tool(ToolType.READ)
    def check_card_status(self) -> str:
        """Returns the status of all cards."""
        if not self.db.cards:
            return "No cards found."
        lines = []
        for card in self.db.cards:
            lines.append(f"Card ({card.card_id}) - Status: {card.status.value}, Linked Account: {card.linked_account_id}")
        return "\n".join(lines)

    # --- Dispute Tools ---

    @is_tool(ToolType.READ)
    def get_disputes(self) -> str:
        """Returns a list of current disputes."""
        if not self.db.disputes:
            return "No disputes found."
        lines = []
        for dispute in self.db.disputes:
            lines.append(f"Dispute ID: {dispute.dispute_id}, Status: {dispute.status.value}, Transaction: {dispute.transaction_id}")
        return "\n".join(lines)

    @is_tool(ToolType.WRITE)
    def resolve_dispute(self, dispute_id: str) -> str:
        """Marks a dispute as resolved."""
        for dispute in self.db.disputes:
            if dispute.dispute_id == dispute_id:
                dispute.status = "resolved"
                return f"Dispute {dispute_id} marked as resolved."
        return f"Dispute ID {dispute_id} not found."

    # --- Security Tools ---

    @is_tool(ToolType.READ)
    def check_login_status(self) -> str:
        """Checks if the user is currently logged in."""
        return "User is currently logged in." if self.db.security_context.logged_in else "User is not logged in."

    @is_tool(ToolType.WRITE)
    def log_in(self) -> str:
        """Logs the user in."""
        self.db.security_context.logged_in = True
        return "User is now logged in."

    @is_tool(ToolType.WRITE)
    def log_out(self) -> str:
        """Logs the user out."""
        self.db.security_context.logged_in = False
        return "User is now logged out."

    # --- Assertions ---

    def assert_account_balance(self, account_id: str, minimum_balance: float) -> bool:
        for account in self.db.accounts:
            if account.account_id == account_id:
                return account.balance >= minimum_balance
        return False

    def assert_logged_in(self, expected: bool = True) -> bool:
        return self.db.security_context.logged_in == expected

    def assert_card_status(self, card_id: str, expected_status: str) -> bool:
        for card in self.db.cards:
            if card.card_id == card_id:
                return card.status == expected_status
        return False
