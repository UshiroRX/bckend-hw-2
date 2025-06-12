from autogen import AssistantAgent, GroupChat, GroupChatManager, UserProxyAgent
from config import settings
import os

os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY

product_describer = AssistantAgent(
    name="ProductDescriber",
    llm_config={"model": "gpt-4"},
    system_message="Ты создаешь красивое объявление о продаже продукта."
)

lang_translarot = AssistantAgent(
    name="LangTranslator",
    llm_config={"model": "gpt-4"},
    system_message="Ты переводишь объявление на английский и казахский язык."
)

user = UserProxyAgent(
    name="User",
    human_input_mode="NEVER",
    is_termination_msg=lambda msg: False  
)

groupchat = GroupChat(
    agents=[user, product_describer, lang_translarot],
    messages=[],
    max_round=3
)

chat_manager = GroupChatManager(
    groupchat=groupchat,
    llm_config={"model": "gpt-4"},
    system_message="""
Ты управляешь чатом. Когда пользователь пишет, первым отвечает ProductDescriber с красивым объявлением.
Затем PriceFinder переводит объявление на английский и казахский. После этого можно завершить разговор.
"""
)

def run_market_agents(user_input: str) -> str:
    user.initiate_chat(
        chat_manager,
        message=f"Хочу продать: {user_input}. Сгенерируй хорошее объявление"
    )

    messages = groupchat.messages

    generated = [m["content"] for m in messages if m["name"] == "ProductDescriber"]
    translated = [m["content"] for m in messages if m["name"] == "LangTranslator"]

    return {
        "generated": generated[-1] if generated else None,
        "translated": translated[-1] if translated else None,
    }
