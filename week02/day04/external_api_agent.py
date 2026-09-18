import json
import os
from api_client import get_todo

from volcenginesdkarkruntime import Ark

api_key = os.getenv("ARK_API_KEY")  # 从系统环境变量读取API Key

model = os.getenv("ARK_MODEL")  # 从系统环境变量读取当前使用的豆包模型


if not api_key:  # 如果API Key不存在
    raise ValueError("没有找到ARK_API_KEY")  # 停止程序，避免发送无效请求


if not model:  # 如果模型ID不存在
    raise ValueError("没有找到ARK_MODEL")  # 停止程序并提示配置模型


client = Ark( # 创建豆包API客户端
    base_url="https://ark.cn-beijing.volces.com/api/v3",  # 指定火山方舟API地址
    api_key=api_key  # 提供身份认证信息
)
TOOLS = [
    {
        "type": "function",

        "function": {
            "name": "get_todo",

            "description": "根据任务ID查询Todo任务信息",

            "parameters": {
                "type": "object",

                "properties": {
                    "todo_id": {
                        "type": "integer",
                        "description": "Todo任务ID"
                    }
                },

                "required": ["todo_id"]
            }
        }
    }
]
def execute_tool(tool_name, arguments):
    # 只允许执行 TOOL_MAP 中注册的工具
    if tool_name not in TOOL_MAP:
        return {"success": False, "error": "不允许执行这个工具"}

    # 检查模型传来的参数
    if not isinstance(arguments, dict):
        return {"success": False, "error": "工具参数必须是字典"}

    if set(arguments) != {"todo_id"}:
        return {"success": False, "error": "必须且只能提供 todo_id"}

    todo_id = arguments["todo_id"]

    if type(todo_id) is not int or todo_id <= 0:
        return {"success": False, "error": "todo_id 必须是正整数"}

    # 找到真实函数并执行，例如 get_todo(todo_id=17)
    return TOOL_MAP[tool_name](**arguments)


def run_agent(user_question):
    # 准备系统要求和用户问题
    messages = [
        {
            "role": "system",
            "content": (
                "你是待办事项查询助手。"
                "查询具体任务时，使用 get_todo 获取数据，不要编造。"
                "未提供任务ID时，先询问用户。"
                "一般知识问题直接回答，无须调用工具。"
                "工具查询失败时，明确说明失败原因。"
            ),
        },
        {"role": "user", "content": user_question},
    ]

    # 最多请求模型5轮，避免一直循环
    for step in range(5):
        print(f"\n===== 第 {step + 1} 轮 =====")

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
        )

        message = response.choices[0].message

        # 将模型回复转换成字典，加入聊天记录
        messages.append(message.model_dump(exclude_none=True))

        # 没有工具调用请求，就返回模型回答
        if not message.tool_calls:
            return message.content or "模型没有返回文字回答。"

        # 执行模型请求的工具
        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name
            print("模型请求调用：", tool_name)

            try:
                arguments = json.loads(
                    tool_call.function.arguments or "{}"
                )
            except json.JSONDecodeError:
                tool_result = {
                    "success": False,
                    "error": "工具参数不是有效的JSON",
                }
            else:
                print("调用参数：", arguments)
                tool_result = execute_tool(tool_name, arguments)

            print("工具结果：", tool_result)

            # 保存工具结果，下一轮一起发送给豆包
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(
                    tool_result, ensure_ascii=False
                ),
            })

    return "已达到最大执行轮数，停止查询。"

TOOL_MAP = {
    "get_todo": get_todo
}

def main():
    # 等待你输入问题，按回车后保存到 user_question
    user_question = input("请输入你的问题：")

    # 把问题交给 Agent，等待它返回最终答案
    answer = run_agent(user_question)

    # 显示答案
    print("\n===== Agent 最终回答 =====")
    print(answer)


# 直接运行这个文件时，执行 main()
if __name__ == "__main__":
    main() 