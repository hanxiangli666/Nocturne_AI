# 从langchain_openai中导入ChatOpenAI类
from langchain_openai import ChatOpenAI
# 从langchain的prompts子模块中导入PromptTemplate类
from langchain_core.prompts import PromptTemplate
# 从langchain.output_parsers子模块中导入CommaSeparatedListOutputParser类
from langchain_core.output_parsers import CommaSeparatedListOutputParser
import os                       # 1. 新增：引入 os 模块，用来读取系统变量
from dotenv import load_dotenv  # 2. 新增：引入加载工具
load_dotenv()

# 创建模型客户端
client = ChatOpenAI(
    # 使用练习密钥"mock-key-123"
    api_key = os.getenv("OPENAI_API_KEY"),
    # 使用的模型 deepseek-chat
    model="deepseek-chat",
    # 指定Deepseek的API服务地址
    base_url="https://api.deepseek.com"
)

# 创建列表解析器，并获取给模型的格式指令
output_parser = CommaSeparatedListOutputParser()
format_instructions = output_parser.get_format_instructions()

# 创建提示词模板：请列举8种{garbage_type}垃圾的常见物品
prompt = PromptTemplate.from_template(
    template="请列举8种{garbage_type}垃圾的常见物品。\n{format_instructions}",
    # 将{format_instructions}绑定为具体的格式指令内容
    partial_variables={"format_instructions": format_instructions}
)

# 使用模板格式化提示词，传入变量"garbage_type":"可回收"
final_prompt = prompt.invoke({"garbage_type": "可回收"})

# 调用模型客户端的invoke方法，传入格式化好的提示词，获取模型响应
response = client.invoke(final_prompt)

# 使用输出解析器解析模型响应，将输出转换为列表
parsed_response = output_parser.parse(response.content)

# 输出解析后的结果
print(parsed_response)