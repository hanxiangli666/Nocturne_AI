# 从 openai 库中导入 OpenAI 类
from openai import OpenAI
import os                       # 1. 新增：引入 os 模块，用来读取系统变量
from dotenv import load_dotenv  # 2. 新增：引入加载工具
load_dotenv()
# 创建OpenAI客户端实例
client = OpenAI(
    # 使用练习密钥"mock-key-123"
    api_key = os.getenv("OPENAI_API_KEY"),  
     # Deepseek的API服务地址
    base_url="https://api.deepseek.com"
)

# 编写prompt提示词
msg = [
    {"role": "user", "content": "你能告诉我人工智能的定义吗？"}
]

# 使用client方法发送请求并获取回复
long_response = client.chat.completions.create(
    # 使用通用模型 deepseek-chat
    model="deepseek-chat",  
    # 将提示词赋值给模型
    messages=msg,
    # TODO 限制AI回复tokens为300
    max_tokens=300
)

# 输出人工智能的定义
print('人工智能的定义：')
# 输出经过裁剪的内容
print(long_response.choices[0].message.content)