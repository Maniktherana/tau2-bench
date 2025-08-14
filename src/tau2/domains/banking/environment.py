from functools import partial
from typing import Optional

from tau2.data_model.tasks import Task
from tau2.domains.banking.data_model import BankingDB
from tau2.domains.banking.tools import BankingTools

from tau2.domains.banking.user_data_model import BankingUserDB
from tau2.domains.banking.user_tools import BankingUserTools
from tau2.domains.banking.utilts import BANKING_DB_PATH, BANKING_POLICY_PATH, BANKING_USER_POLICY_PATH, BANKING_TASK_SET_PATH
from tau2.environment.environment import Environment
from tau2.utils import load_file


class BankingEnvironment(Environment):
    tools: BankingTools
    user_tools: BankingUserTools

    def __init__(
        self,
        domain_name: str,
        policy: str,
        tools: BankingTools,
        user_tools: BankingUserTools,
    ):
        super().__init__(domain_name, policy, tools, user_tools)

    def sync_tools(self):
        """
        Sync environment state with current user status. Useful for dynamic assertions,
        e.g., checking payment requests, card status, dispute tracking, etc.
        """
        phone = self.user_tools.db.phone_number
        if not phone:
            return

        try:
            customer = self.tools.get_customer_by_phone(phone)
            self.user_tools.db.customer_id = customer.customer_id

            # Sync primary account status
            if customer.account_ids:
                account = self.tools.get_account(customer.account_ids[0])
                self.user_tools.db.primary_account_active = account.status == "Active"
                self.user_tools.db.primary_account_id = account.account_id
                self.user_tools.db.account_balance = account.current_balance

            # Sync first card status
            if customer.card_ids:
                card = self.tools._get_card(customer.card_ids[0])
                self.user_tools.db.primary_card_active = card.status == "Active"
                self.user_tools.db.primary_card_id = card.card_id

        except Exception as e:
            # If sync fails, just continue - user tools will use default values
            pass


def get_environment(
    db: Optional[BankingDB] = None,
    user_db: Optional[BankingUserDB] = None,
    solo_mode: bool = False,
) -> BankingEnvironment:
    if db is None:
        db = BankingDB.load(BANKING_DB_PATH)
    tools = BankingTools(db)

    if user_db is None:
        user_db = BankingUserDB.load()
    user_tools = BankingUserTools(user_db)

    if solo_mode:
        policy = load_file(BANKING_USER_POLICY_PATH)
    else:
        policy = load_file(BANKING_POLICY_PATH)

    env = BankingEnvironment(
        domain_name="banking",
        policy=policy,
        tools=tools,
        user_tools=user_tools,
    )
    if solo_mode:
        env.set_solo_mode(True)

    return env


def load_tasks(path: str) -> list[Task]:
    tasks = load_file(path)
    if isinstance(tasks, dict) and "tasks" in tasks:
        tasks = tasks["tasks"]
    return [Task.model_validate(task) for task in tasks]


def get_environment_main() -> BankingEnvironment:
    return get_environment(solo_mode=False)


def get_environment_solo() -> BankingEnvironment:
    return get_environment(solo_mode=True)


def get_tasks() -> list[Task]:
    return load_tasks(BANKING_TASK_SET_PATH)
