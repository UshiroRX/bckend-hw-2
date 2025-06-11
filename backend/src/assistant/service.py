from autogen import AssistantAgent, GroupChat, GroupChatManager, UserProxyAgent
import os
from config import settings

os.environ["OPENAI_API_KEY"] = settings

product_describer = AssistantAgent(
    name="ProductDescriber",
    llm_config={"model": "gpt-4"}
)

price_finder = AssistantAgent(
    name="PriceFinder",
    llm_config={"model": "gpt-4"},
)

manager = AssistantAgent(
    name="ProductManager",
    llm_config={"model": "gpt-4"},
)

def run_market_agents(user_input: str) -> str:
    user = UserProxyAgent(
        name="User",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=10
    )

    groupchat = GroupChat(
        agents=[user, product_describer, price_finder, manager],
        messages=[],
        max_round=8
    )

    manager_agent = GroupChatManager(
        groupchat=groupchat,
        llm_config={"model": "gpt-4"}
    )

    user.initiate_chat(
        manager_agent,
        message=f"Хочу продать: {user_input}. Сгенерируй хорошее объявление и найди оптимальную цену."
    )

    return groupchat.messages[-1]["content"]
