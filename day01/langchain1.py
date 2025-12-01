# 从 langchain_openai 库中导入 ChatOpenAI 类
from langchain_openai import ChatOpenAI
# 从 langchain_core 库中导入 SystemMessage 和 HumanMessage 类
from langchain_core.messages import SystemMessage, HumanMessage
import os                       # 1. 新增：引入 os 模块，用来读取系统变量
from dotenv import load_dotenv  # 2. 新增：引入加载工具
load_dotenv()

# 创建客户端实例
client = ChatOpenAI(
    # 使用练习密钥"mock-key-123"
    api_key = os.getenv("OPENAI_API_KEY") ,
    # 使用的模型 deepseek-chat
    model="deepseek-chat",
    # 指定Deepseek的API服务地址
    base_url="https://api.deepseek.com",
    # 设置较低的temperature值
    temperature=0.1,
    # 设置最大生成长度为1000个token
    max_tokens=1000,
)

# 构建LangChain格式的消息列表
msg = [
    # 系统消息：设定AI的角色为诗人
    SystemMessage(content="你是一位诗人，擅长写抒情诗。"),
    # 用户消息：提出具体的写诗请求
    HumanMessage(content="请帮我扩写这首诗：曾涵晞我喜欢你,你是人间四月天,你是我的白月光"),
]

# 调用invoke方法发送请求并获取回复
response = client.invoke(msg)
# 输出回复内容中的文本部分
print(response.content)