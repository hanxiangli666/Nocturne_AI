import os
from dotenv import load_dotenv  # 2. 新增：引入加载工具
load_dotenv()

# 1. 导入核心组件
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser # 新增：用于把结果解析成字符串
from langchain_community.chat_message_histories import ChatMessageHistory # 新增：用于管理具体的聊天记录
from langchain_core.runnables.history import RunnableWithMessageHistory # 新增：用于给链条"挂载"记忆

# --- 2. 设置模型 (和原来一样) ---
client = ChatOpenAI(
    api_key = os.getenv("OPENAI_API_KEY"),
    model="deepseek-chat",
    base_url="https://api.deepseek.com",
)

# --- 3. 设置 Prompt (和原来基本一样) ---
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一位图书推荐助手，根据用户的阅读偏好推荐书籍。回答要简洁准确。"),
        MessagesPlaceholder(variable_name="chat_history"), # 记忆占位符
        ("human", "{input}"), # 用户输入占位符
    ]
)

# --- 4. 定义基础链 (核心变化点！) ---
# 语法含义：Prompt -> 传给 Model -> 传给 OutputParser (变成纯文本)
basic_chain = prompt | client | StrOutputParser()

# --- 5. 设置记忆管理 (核心变化点！) ---
# 我们需要一个地方存每个用户的历史记录，用字典模拟
store = {}

# 这个函数用于获取指定 session_id 的历史记录
def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# 将记忆功能"包裹"在基础链外面
final_chain = RunnableWithMessageHistory(
    basic_chain,
    get_session_history,
    input_messages_key="input",        # 对应 Prompt 中的 {input}
    history_messages_key="chat_history" # 对应 Prompt 中的 MessagesPlaceholder
)

# --- 6. 调用 (Invoke) ---

# 第一个问题 (需要传入 config 来指定 session_id，区分不同用户)
response1 = final_chain.invoke(
    {"input": "我喜欢科幻小说，有什么推荐吗？"},
    config={"configurable": {"session_id": "user_1"}}
)
print(f"回答1: {response1}") 
# 注意：这里直接打印 response1 即可，因为 StrOutputParser 已经帮我们将对象转为了字符串

# 第二个问题 (使用同一个 session_id，自动带入历史)
response2 = final_chain.invoke(
    {"input": "这些书中有适合入门的吗？"},
    config={"configurable": {"session_id": "user_1"}}
)
print(f"回答2: {response2}")