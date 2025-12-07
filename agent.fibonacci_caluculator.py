import os
from dotenv import load_dotenv  # 2. 新增：引入加载工具
load_dotenv()
# 从 langchain_openai 中导入 ChatOpenAI
from langchain_openai import ChatOpenAI
# 从 langchain_core 导入 tool 装饰器 (新版标准位置)
from langchain_core.tools import tool
# 从 langchain_experimental 导入 PythonREPLTool
from langchain_experimental.tools import PythonREPLTool
# 【核心升级】导入 LangGraph 的预构建 Agent 和 内存检查点
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

"""1.初始化模型"""
# 创建模型客户端
model = ChatOpenAI(
    # 使用练习密钥 (实际运行时请确保是有效的 DeepSeek/OpenAI Key)
    api_key= os.getenv("OPENAI_API_KEY"), 
    # 使用的模型 deepseek-chat
    model="deepseek-chat",
    # 指定Deepseek的API服务地址
    base_url="https://api.deepseek.com",
    # 设置温度参数为0，确保计算准确性
    temperature=0,
)

"""2.准备工具"""
# 定义斐波那契工具
@tool("fibonacci_calculator")
def fibonacci_calculator(n: int):
    """计算斐波那契数列的第n项数值。对于斐波那契数列相关问题，优先使用此工具。"""
    # 转换输入类型，防止模型有时传入字符串
    try:
        n = int(n)
    except ValueError:
        return "输入必须是整数"

    if n <= 0:
        return "请输入正整数"
    elif n == 1:
        return 0
    elif n == 2:
        return 1

    a, b = 0, 1
    for i in range(3, n + 1):
        a, b = b, a + b
    return b

# 创建工具列表
tools = [fibonacci_calculator, PythonREPLTool()]

"""3.创建 Agent (LangGraph 架构)"""
# 【关键变化】LangGraph 使用 checkpointer 来管理记忆，而不是 Memory 类
memory = MemorySaver()

# 使用 create_react_agent 自动整合模型和工具
# 这取代了之前的 create_react_agent + AgentExecutor
graph = create_react_agent(model, tools=tools, checkpointer=memory)

"""4.执行对话"""
# LangGraph 通过 config 中的 thread_id 来区分不同的对话历史（相当于以前的 memory 对象）
config = {"configurable": {"thread_id": "thread-1"}}

print("--- 问题 1 ---")
question_1 = "请计算斐波那契数列的第10项是多少？"
# invoke 的输入格式变成了 messages 列表
inputs_1 = {"messages": [("user", question_1)]}
ret_1 = graph.invoke(inputs_1, config=config)
# 输出位于 messages 的最后一条
print(ret_1["messages"][-1].content)

print("\n--- 问题 2 ---")
question_2 = "斐波那契数列的第15项数值是多少？"
inputs_2 = {"messages": [("user", question_2)]}
# 传入相同的 config，Agent 会自动读取之前的上下文
ret_2 = graph.invoke(inputs_2, config=config)
print(ret_2["messages"][-1].content)

print("\n--- 问题 3 ---")
question_3 = "刚才那两个数相加是多少？"
inputs_3 = {"messages": [("user", question_3)]}
# 继续使用 config，Agent 知道"刚才那两个数"指的是前两轮的结果
ret_3 = graph.invoke(inputs_3, config=config)
print(ret_3["messages"][-1].content)