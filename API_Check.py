# 导入 requests 库，用于发送HTTP请求
import requests
import os                       # 1. 新增：引入 os 模块，用来读取系统变量
from dotenv import load_dotenv  # 2. 新增：引入加载工具

# 3. 加载 .env 文件 (这行代码会去找同级目录下的 .env 文件并读取它)
load_dotenv()

# 查询账户余额的API接口地址
url = "https://api.deepseek.com/user/balance"

# 4. 修改核心：读取 API Key
# ⚠️ 注意：getenv("...") 括号里的名字，必须和你 .env 文件里写的变量名完全一致！
# 如果你在 .env 里写的是 OPENAI_API_KEY=sk-xxx，这里就填 "OPENAI_API_KEY"
key = os.getenv("OPENAI_API_KEY") 

# 检查一下是否成功读取（方便调试）
if not key:
    print("❌ 错误：未找到 Key，请检查 .env 文件是否配置正确！")
else:
    print("✅ Key 读取成功，准备发送请求...")

# 构建请求头，用于身份验证和内容协商
headers = {
    'Accept': 'application/json',
    'Authorization': f'Bearer {key}'
}

# 获取并返回账户余额信息
response = requests.request("GET", url, headers=headers, data={})
print(f'你的API余额信息为：{response.text}')