from langchain_community.chat_message_histories import RedisChatMessageHistory

from config import REDIS_URL


def get_session_history(sesseion_id):
    return RedisChatMessageHistory(
        session_id=sesseion_id,
        url=REDIS_URL,
    )