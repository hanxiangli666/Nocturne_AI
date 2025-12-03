# 从 openai 库中导入 OpenAI 类
from openai import OpenAI
import os                       # 1. 新增：引入 os 模块，用来读取系统变量
from dotenv import load_dotenv  # 2. 新增：引入加载工具
load_dotenv()
# 创建客户端
client = OpenAI(
    # 使用练习密钥"mock-key-123"
    api_key = os.getenv("OPENAI_API_KEY"),  
    # Deepseek的API服务地址
    base_url="https://api.deepseek.com"
)

# 编写prompt提示词
msg = [
    # 用户消息："请写一段关于人工智能未来可能发展的方向"
    {"role": "user", "content": "请写一段关于人工智能未来可能发展的方向"}
]

# 第一次请求
res1 = client.chat.completions.create(
    # 使用通用模型 deepseek-chat
    model="deepseek-chat",
    # 将提示词赋值给模型
    messages=msg
)

# 第二次请求
res2 = client.chat.completions.create(
    # 使用通用模型 deepseek-chat
    model="deepseek-chat",
    # 将提示词赋值给模型
    messages=msg,
    # TODO 设置重复度参数为1.2，降低重复的概率
    frequency_penalty=1.2,
    # TODO 设置话题延展性参数为1，鼓励模型引入新概念
    presence_penalty=1
)

# 输出第一次请求的生成结果
print(res1.choices[0].message.content)

# 输出第二次请求的生成结果
print(res2.choices[0].message.content)
