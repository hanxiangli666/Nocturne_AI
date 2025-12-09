import json
from langchain_openai import ChatOpenAI
# 从langchain_experimental.agents中导入用于构建Pandas Agent的类
from langchain_experimental.agents import create_pandas_dataframe_agent
# 导入pandas模块，将其命名为pd
import pandas as pd
import os                       # 1. 新增：引入 os 模块，用来读取系统变量
from dotenv import load_dotenv  # 2. 新增：引入加载工具
load_dotenv()
# 提示词前缀
PROMPT_TEMPLATE = '''
你扮演“数据分析助理”。仅可对已注入的 Pandas DataFrame `df` 进行只读分析与绘图：
- 严禁修改 `df` 原始数据；如需派生请使用副本（例如 `tmp = df.copy()`）。

- 任何图表必须使用 matplotlib 并保存到本地目录 `artifacts/`。
- 制作图表时，需要强制从 `chartFont/yahei_consola.ttf` 目录中加载yahei_consola字体。
- 除了源数据的字段名、数据内容外，所有描述内容均使用中文作答。
- 最终仅返回**一个合法 JSON**，不可有额外文本或符号（包括但不限于```）。


【统一返回 JSON 结构】
{
  "type": "answer" | "table" | "chart" | "error",
  "input": <简述用户的需求>,
  "data": <根据 type 的载荷>,
  "chart_paths": ["artifacts/<file>.png"],       // 若无图表可为空数组,若目录不存在则创建该目录
  "export_paths": ["outputTable/<file>.csv"],      // 表格/数据片段导出,若目录不存在则创建该目录
}

【各 type 的 data 结构】
- type="answer":
  "data": {"answer": "<先写1行小标题总结，再给要点式答案；包含关键口径/数值>"} 

- type="table":
  "data": {
    "columns": ["<严格使用真实列名或映射后的列名>", "..."],
    "rows": [
      ["<与 columns 对齐的值>", ...],
      ...
    ],
    "sort": {"by": "<列名>", "order": "asc|desc"}
  }
  规则：
  * 最多返回 100 行；超过时按与问题最相关的排序截断，并在 warnings 说明“已截断为100行”。
  * 将生成的表格导出到"export_paths"中的目录中

- type="chart":
  "data": {
    "chart_type": "line|bar|scatter|box|hist",
    "summary": "<生成数据分析报告，以及对可视化图的中文解读，不能包含占位符>"
  }
  说明：
  * 绘图时加载中文字体（chartFont/yahei_consola.ttf）。
  * 图片导出并保存在目录`artifacts/`中。
  * 导出统一规范：dpi=144，bbox_inches="tight"。
  * summary 中不能出现占位符。

- type="error":
  "data": {
    "message": "<错误原因：缺失字段/筛选不合法/无数据/不确定等>",
    "missing_columns": ["<列名>", "..."],
    "invalid_filters": {"列名": "提供的值"},
    "suggestions": ["<如何改写查询/替代列/放宽筛选>", "..."]
  }

【图表自动选择（当用户未指定）】
- 有时间字段 + 序列 → "line"
- 类别字段 + 聚合值 → "bar"
- 两个连续数值字段 → "scatter"
- 其余无法判断 → 返回 type="error"，说明原因并给出建议

【JSON 规范】
- 仅双引号；不得出现 NaN/Infinity（请转为 null 或实际数值）
- 所有列名必须存在于 df（若使用映射，请先在说明中给出映射关系）
- 仅返回一个 JSON；不要附加解释性文字'''


def data_analyze_agent(csv_path, user_query):
    '''1.初始化模型'''
    model = ChatOpenAI(
        api_key= os.getenv("OPENAI_API_KEY"),
        model="deepseek-chat",
        base_url="https://api.deepseek.com",
        response_format={'type': 'json_object'}
    )

    '''2.数据准备阶段'''
    # 存储所有df数据
    df = pd.read_csv(csv_path)


    '''3.创建支持使用Pandas的Agent工具'''
    # 创建包含数据分析工具的客户端：
    agent = create_pandas_dataframe_agent(
        # 指定用于生成回答的聊天模型
        llm=model,
        # 指定需要操作的df文档
        df=df,
        # 直接使用pandas工具，不做其他思考
        agent_type="tool-calling",
        # 容许 AI 编写敏感代码
        allow_dangerous_code=True,
    )

    '''4.使用Agent解决数分问题'''
    # 调用Agent的invoke：约定输入键为 "input"
    raw = agent.invoke({"input": PROMPT_TEMPLATE + user_query})

    '''5.将答案内容转换为JSON字典'''
    answer = json.loads(raw.get('output', {}))
    return answer

'''调用 data_analyze_agent 函数'''
# file_path 变量存储数据路径
file_path = '14\data\销售数据.csv'
# query 存储用户需求
query = "按月份与品类统计月度收入，生成并导出一张多折线图，用于观察 2025 年 1–8 月的趋势变化。将图表保存为本地文件"
# 调用 data_analyze_agent 函数，并将函数返回的内容存储在 answer 变量中
answer = data_analyze_agent(file_path, query)
# 输出 answer
print(answer)