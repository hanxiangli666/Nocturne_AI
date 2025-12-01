# TODO 从 openai 库中导入 OpenAI 类
from openai import OpenAI
import os                       # 1. 新增：引入 os 模块，用来读取系统变量
from dotenv import load_dotenv  # 2. 新增：引入加载工具
load_dotenv()
# TODO 创建客户端
client = OpenAI(
    # TODO 使用练习密钥"mock-key-123"
    api_key = os.getenv("OPENAI_API_KEY"),
    # TODO Deepseek的API服务地址
    base_url="https://api.deepseek.com"
)

# TODO 编写prompt提示词
msg = [{"role": "system", 
         # 系统消息："你是一名专业的法语翻译官，翻译用户输入的内容"
         "content": "你是一名专业的法语翻译官，翻译用户输入的内容"},
          # 用户消息："我超级喜欢编程"
        {"role": "user",
         "content": "我超级喜欢编程"}  # 用户输入
    ]








# TODO 使用client.chat.completions.create() 方法发送请求并获取回复
response = client.chat.completions.create(
     # TODO 使用通用模型 deepseek-chat
     model = "deepseek-chat",
    # TODO 将我们编写好的提示词赋值给模型
     messages = msg
)

# TODO 输出模型返回的翻译结果
print(response.choices[0].message.content)