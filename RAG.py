# 导入TextLoader: 从本地文本文件加载为Document列表
from langchain_community.document_loaders import TextLoader
# 导入递归字符切分器
from langchain_text_splitters import RecursiveCharacterTextSplitter
# 导入HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
# 导入FAISS: 本地内存型向量数据库
from langchain_community.vectorstores import FAISS
# 导入ChatOpenAI聊天模型客户端
from langchain_openai import ChatOpenAI

# --- [NEW] LCEL 核心组件导入 ---
from langchain_classic.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
import os                       # 1. 新增：引入 os 模块，用来读取系统变量
from dotenv import load_dotenv  # 2. 新增：引入加载工具
load_dotenv()
# ================= 数据准备阶段 =================

# 指定原始文档路径 (请确保路径正确)
file_path = "data/ProductFile.txt"

# 读取本地文件
loader = TextLoader(file_path, encoding='utf-8') # 建议显式加上 encoding
docs = loader.load()

# 创建文本切分器
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=60,
    chunk_overlap=30,
    separators=["\n\n", "\n", "Q:", "A:", "。", "！", "？", "，", "、", " ", ""]
)

# 切分文档
chunks = text_splitter.split_documents(docs)

# 加载嵌入模型
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# 构建向量索引
db = FAISS.from_documents(chunks, embeddings)
retriever = db.as_retriever()

# ================= 模型配置阶段 =================

# 创建模型客户端
model = ChatOpenAI(
    api_key = os.getenv("OPENAI_API_KEY"), # 请替换为你的真实 Key，或者保持 mock
    model="deepseek-chat",
    base_url="https://api.deepseek.com",
)

# ================= LCEL 链条构建阶段 (核心修改) =================

# 1. 定义[上下文改写]提示词
# 作用：如果用户问"它多少钱"，将结合历史记录改写为"智能健身镜多少钱"
contextualize_q_system_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is."
)

contextualize_q_prompt = ChatPromptTemplate.from_messages([
    ("system", contextualize_q_system_prompt),
    MessagesPlaceholder("chat_history"), # 这里的名字必须和后面传入的参数一致
    ("human", "{input}"),
])

# 创建历史感知检索器 (History Aware Retriever)
history_aware_retriever = create_history_aware_retriever(
    model, retriever, contextualize_q_prompt
)

# 2. 定义[问答]提示词
# 作用：基于检索到的 context 回答问题
qa_system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}"
)

qa_prompt = ChatPromptTemplate.from_messages([
    ("system", qa_system_prompt),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])

# 创建文档问答链
question_answer_chain = create_stuff_documents_chain(model, qa_prompt)

# 3. 创建最终的 RAG 链 (Retrieval Chain)
rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

# ================= 执行与测试阶段 =================

# 初始化聊天记录列表 (LCEL 中手动管理这个列表，比旧版 Memory 类更透明)
chat_history = []

print("--- 第一轮对话 ---")
question1 = "什么是智能健身镜？"
# invoke 需要传入 input 和 chat_history
response1 = rag_chain.invoke({"input": question1, "chat_history": chat_history})

print(f"User: {question1}")
print(f"AI:   {response1['answer']}")

# 更新历史记录
# 将这一轮的问答加入到历史列表中
chat_history.extend([
    HumanMessage(content=question1),
    AIMessage(content=response1['answer'])
])

print("\n--- 第二轮对话 (测试多轮记忆) ---")
question2 = "它如何使用？" # 这里的“它”需要 AI 结合上文理解
response2 = rag_chain.invoke({"input": question2, "chat_history": chat_history})

print(f"User: {question2}")
print(f"AI:   {response2['answer']}")