# 从 openai 库中导入 OpenAI 类
from openai import OpenAI

# 创建OpenAI客户端实例
client = OpenAI(
    # 使用练习密钥"mock-key-123"
    api_key="sk-a2c3cb41b95d4261aa39d9270dd4f70f",  
    # Deepseek的API服务地址
    base_url="https://api.deepseek.com"
)

# 编写prompt提示词
msg = [
    # 用户消息："请帮我写一句关于人工智能的宣传语"
    {"role": "user", "content": "请帮我写一句关于人工智能的宣传语"}
]

# 第一次请求
low_temp_response = client.chat.completions.create(
    # 使用通用模型 deepseek-chat
    model="deepseek-chat",
    # 将提示词赋值给模型
    messages=msg,
    # 设置最大生成长度为50个token
    max_tokens=50, 
    # TODO 设置temperature值为0.3，使输出保守稳重
    temperature=0.3
)


# 第二次请求
high_top_p_response = client.chat.completions.create(
    # 使用通用模型 deepseek-chat
    model="deepseek-chat",
    # 将提示词赋值给模型
    messages=msg,
    # 设置最大生成长度为50个token
    max_tokens=50, 
    # TODO 设置top_p值为0.95，使输出更多样具有创意
    top_p=0.95
)


# 输出低temperature风格的标题
print("低 temperature 风格（标准理性）：")
# 输出低temperature生成的宣传语
print(low_temp_response.choices[0].message.content)


# 输出高top_p风格的标题
print("高 top_p 风格（多样创意）：")
# 输出高top_p生成的宣传语
print(high_top_p_response.choices[0].message.content)
