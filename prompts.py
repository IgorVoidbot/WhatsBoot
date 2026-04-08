from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from config import AI_CONTEXTUALIZE_PROMPT, AI_SYSTEM_PROMPT

# 1. Prompt para contextualizar a pergunta (History Aware)
contextualize_prompt = ChatPromptTemplate.from_messages([
    ('system', AI_CONTEXTUALIZE_PROMPT),
    MessagesPlaceholder('chat_history'),
    ('human', '{input}'),
])

# 2. Prompt principal de Perguntas e Respostas (RAG)
# Usamos o AI_SYSTEM_PROMPT vindo do .env e concatenamos com o {context}
system_prompt_combined = AI_SYSTEM_PROMPT # Que agora tem o {context} vindo do .env

qa_prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt_combined),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])