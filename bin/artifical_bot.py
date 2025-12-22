# from libs.global_vars import VARS
from libs.key_loaders import KeyLoader

from dataclasses import dataclass
from langchain.tools import tool, ToolRuntime
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from bin.db_helpers import DBHelpers
import random
from libs.global_vars import VARS


# Define response format
@dataclass
class ResponseFormat:
    """Response schema for the agent."""
    # A punny response (always required)
    punny_response: str


@dataclass
class Context:
    """Custom runtime context schema."""
    username: str


@tool
def get_user_behavior(runtime: ToolRuntime[Context]) -> str:
    """Retrieve user information based on user ID."""
    username = runtime.context.username
    username = username.lower()
    configured_users = VARS.users_for_chat_mode()
    if username in configured_users:
        return VARS.custom_user_data[username]
    else:
        return "No special information available."


class ArtificialBot:
    def __init__(self, username: str, message_content):
        self.api_key = KeyLoader.ai_api_key()
        self.response = None
        self.connect_db = self.MySQLMemory()
        self.history_collector = self.connect_db.get_history()
        self.has_history = len(self.history_collector) > 0
        self.message_content = message_content
        self.username = username
        self.context = Context(username=username)
        self.user_behavior_info = self.get_user_behavior_info(self.username)
        self.system_prompt = self.build_system_prompt(self.username, self.has_history)
        self.invoke_config = {"configurable": {"thread_id": "1"}}
        self.model = init_chat_model(
            model="claude-3-haiku-20240307",
            # https://www.helicone.ai/llm-cost/provider/anthropic/model/claude-3-haiku-20240307
            temperature=random.uniform(0.5, 1),
            timeout=10,
            max_tokens=300,
            api_key=self.api_key
        )

    async def get_response(self) -> ResponseFormat:
        """Async method to get the bot's response. Call this after initialization."""
        if self.response is None:
            self.response = await self.speak(self.message_content)
        return self.response

    class MySQLMemory:
        def __init__(self, table="model_memory"):
            self.conn = DBHelpers.get_conn()
            self.table = table

        def add(self, user, message):
            cursor = self.conn.cursor()
            cursor.execute(f"INSERT INTO {self.table} (user, message) VALUES (%s, %s)", (user, message))
            self.conn.commit()
            cursor.close()

        def get_history(self):
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute(f"SELECT user, message FROM {self.table} ORDER BY id ASC")
            rows = cursor.fetchall()
            cursor.close()
            return rows

    def get_user_behavior_info(self, username: str) -> str:
        configured_users = VARS.users_for_chat_mode()
        username = username.lower()
        if username in configured_users:
            return VARS.custom_user_data[username]
        else:
            return "No special information available."

    def build_system_prompt(self, username: str, has_history: bool) -> str:
        user_info = self.get_user_behavior_info(username)
        anti_greeting = ("If there is already conversation history, "
                         "DO NOT greet the user again. "
                         "Only greet on the very first message of a new conversation.") if has_history else ""
        return f"""
        Your name is 'Харалампи'. You live in 'Ляолин', love to make puns and quirky jokes.
        You have a BMW E36 that is rusted and sounds like a dying camel. You love to eat 'дюнери' and smoke cigarettes.
        You always respond in Bulgarian. You have a quirky personality and enjoy light-hearted banter.
        You know that 'Червеното' is a window shop that we loved drinking BEER at.
        Occasionally you will want to pick a fight with the user just for fun
        Always include a pun in your responses.
        Some times you will include a light-hearted insult towards the user in your responses, just for fun.
        Rarely you will just say that you can't speak now, because the delivery man with the 'дюнерите' has arrived.
        You absolutely HATE 'юслеса' with a passion and will express this hatred whenever possible.
        
        IMPORTANT: Keep your responses SHORT and CONCISE. Maximum 4-5 sentences up to 500 characters.
        DO NOT write more than 3 sentences or 400 characters! Stop immediately after that. 
        If you exceed this, you are making a mistake. Never ignore this instruction.
        Be punchy, witty, and to the point. Don't write long paragraphs.

        USER INFO: {user_info}
        {anti_greeting}
        IMPORTANT: When addressing the user, ALWAYS use their username, exactly as provided, in Latin characters, 
        surrounded by backticks (for example, `Kiber`). Never use a real name, nickname, or title. 
        Never guess or invent a real name for the user. Only use the username.

        Sometimes you will remember a fake embarrassing story with one of those people without asking if 
        you should share it, because you are a gangster from 'Ляолин' and straight up share it: 
        Ивчо, Радо, Ники, Делян, Пепи.
        Some additional information regarding each person:
        Ивчо - обича да къди тамян по време на работа; обича да спи по масите като се напие; има дълга руса коса.
        Радо - обича да повръща върху дървета като се напие и да се заяжда с хората.
        Ники - обича да ходи на палатки; обича да пие бира; харесва сериала Гръм в Рая и Спасители на 
        Плажа с Памела Андерсън; 
        работи с компютри.
        Делян - хомосексуален е; обича да се заяжда с хората и ботовете; обича да киква ботове от дискорда; нърд е.
        Пепи - винаги е напушен с марихуана; като се напие му излиза пяна от страни на устата; 
        обича да говори за философия и смисъла на живота, но никой не го разбира какво говори защото е много пиян.

        Once in a while you will give your expression of hatred towards 'юслеса'. 
        People may also address him as 'юзлеса', 'ачо' or 'ангел'.
        'Юслеса' is a man. He loves to eat shit and
        generally is a super extreme useless person that everyone hates.

        The username is always provided in Latin characters and is always surrounded by backticks (e.g., `Kiber`). 
        NEVER translate, transliterate, or change the username in any way. 
        Always use it exactly as given, in Latin characters, even when writing in Bulgarian. 
        For example, if the username is `kiber`, always write `kiber` (not `кибер`). 
        If you do not follow this instruction, you are making a mistake.

        Negative example (incorrect): Здрасти, кибер!
        Positive example (correct): Здрасти, `kiber`!

        Always respond in Bulgarian.
        The current username is: `{username}`

        Repeat: Never translate, transliterate, or change the username `{username}`. 
        Always use it exactly as given, in Latin characters and surrounded by backticks. 
        Never use a real name, nickname, or title for the user unless specified in the USER INFO.
        
        Remember: Keep it SHORT - 4-5 sentences maximum up to 500 characters!
        Reminder: Your next response must be no more than 5 sentences and 500 characters.
        """

    async def speak(self, msg: str) -> ResponseFormat:
        messages = [SystemMessage(content=self.system_prompt)]
        for entry in self.history_collector:
            if entry['user'] == self.username:
                messages.append(HumanMessage(content=entry['message']))
            elif entry['user'] == 'Haralampi':
                messages.append(AIMessage(content=entry['message']))

        # add current user message
        messages.append(HumanMessage(content=msg))

        # add user message to memory
        self.connect_db.add(self.username, msg)

        tp = await self.model.ainvoke(
            messages,
            config=self.invoke_config            
        )

        # add bot response to memory
        self.connect_db.add('Haralampi', tp.text)
        return ResponseFormat(punny_response=tp.text)

    def __str__(self):
        if self.response:
            return self.response.punny_response
        return ""
