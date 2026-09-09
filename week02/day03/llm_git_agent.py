import os

from volcenginesdkarkruntime import Ark


api_key = os.getenv("ARK_API_KEY")
model = os.getenv("ARK_MODEL")

if not api_key:
    raise ValueError("没有找到 ARK_API_KEY，请先在终端设置 API Key")
if not model:
    raise ValueError("没有找到 ARK_MODEL，请先在终端设置模型 ID")

client = Ark(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key=api_key,
)
tools = [
    {
        "type": "function",
        "name": "get_current_branch",
        "description": "读取当前 Git 仓库所在的分支",
        "parameters": {
            "type": "object",
            "properties": {},
        },
    }
]

response = client.responses.create(
    model=model,
    input="请用一句话解释 Git branch 是什么。",
    tools=tools,
)

for item in response.output:
    if item.type == "message":
        for content in item.content:
            if content.type == "output_text":
                print(content.text)
