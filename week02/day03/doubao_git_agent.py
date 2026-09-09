import json  # 用来处理JSON字符串，例如解析LLM生成的Tool参数

import os  # 用来读取ARK_API_KEY和ARK_MODEL环境变量


from volcenginesdkarkruntime import Ark  # 导入豆包/火山方舟客户端


from real_git_tools import get_git_status  # 导入我们之前写好的真实Git状态工具

from real_git_tools import get_current_branch  # 导入读取当前Git分支的真实工具

from real_git_tools import get_git_remotes  # 导入读取Git远程仓库的真实工具

from real_git_tools import get_latest_commit  # 导入读取最近commit的真实工具


api_key = os.getenv("ARK_API_KEY")  # 从系统环境变量读取API Key

model = os.getenv("ARK_MODEL")  # 从系统环境变量读取当前使用的豆包模型


if not api_key:  # 如果API Key不存在
    raise ValueError("没有找到ARK_API_KEY")  # 停止程序，避免发送无效请求


if not model:  # 如果模型ID不存在
    raise ValueError("没有找到ARK_MODEL")  # 停止程序并提示配置模型


client = Ark(  # 创建豆包API客户端
    base_url="https://ark.cn-beijing.volces.com/api/v3",  # 指定火山方舟API地址
    api_key=api_key  # 提供身份认证信息
)


TOOLS = [  # 定义所有允许LLM看到的工具说明
    {
        "type": "function",  # 表示这是一个普通函数工具

        "function": {
            "name": "get_git_status",  # LLM看到的工具名称

            "description": (
                "读取当前Git仓库的真实状态，包括当前分支以及是否存在未提交修改。"
                "这是只读工具，不会修改仓库。"
            ),  # 描述越清楚，LLM越容易正确选择工具

            "parameters": {
                "type": "object",  # 参数必须是一个JSON对象

                "properties": {}  # 这个函数目前不需要任何输入参数
            }
        }
    },

    {
        "type": "function",

        "function": {
            "name": "get_current_branch",

            "description": (
                "读取当前Git仓库所在的真实branch。"
                "当用户询问当前分支时使用。"
            ),

            "parameters": {
                "type": "object",

                "properties": {}
            }
        }
    },

    {
        "type": "function",

        "function": {
            "name": "get_git_remotes",

            "description": (
                "读取当前Git仓库真实的remote远程仓库配置。"
                "适合排查GitHub远程仓库连接问题。"
            ),

            "parameters": {
                "type": "object",

                "properties": {}
            }
        }
    },

    {
        "type": "function",

        "function": {
            "name": "get_latest_commit",

            "description": (
                "读取当前Git仓库最近一次commit的信息。"
                "适合检查代码是否已经成功commit。"
            ),

            "parameters": {
                "type": "object",

                "properties": {}
            }
        }
    }
]


TOOL_MAP = {  # 建立“工具名字”和“真正Python函数”的映射关系
    "get_git_status": get_git_status,

    "get_current_branch": get_current_branch,

    "get_git_remotes": get_git_remotes,

    "get_latest_commit": get_latest_commit
}


def execute_tool(tool_name, tool_arguments):  # 创建统一的Tool执行器
    if tool_name not in TOOL_MAP:  # 安全检查：禁止LLM执行没有注册的函数
        return {
            "success": False,

            "error": f"不允许执行工具：{tool_name}"
        }


    real_function = TOOL_MAP[tool_name]  # 根据工具名称找到真正的Python函数


    try:  # 开始捕获工具执行过程中可能出现的异常
        result = real_function(**tool_arguments)  # 真正执行Git Tool

        return {
            "success": True,

            "data": result
        }


    except Exception as error:  # 如果真实函数执行失败
        return {
            "success": False,

            "error": str(error)
        }


def run_agent(user_question):  # 定义我们的最小Agent Loop

    messages = [  # 创建本轮Agent的上下文
        {
            "role": "system",

            "content": (
                "你是一名FDE Git排障助手。"
                "当问题涉及当前真实Git仓库信息时，应调用提供的只读工具获取真实数据。"
                "不要编造仓库状态。"
                "目前只能使用只读工具，禁止尝试修改Git仓库。"
            )
        },

        {
            "role": "user",

            "content": user_question
        }
    ]


    max_steps = 5  # 最多允许Agent进行5轮，防止出现无限Tool Calling循环


    for step in range(max_steps):  # 开始Agent循环

        print(f"\n===== Agent Step {step + 1} =====")  # 方便我们观察Agent当前运行到第几轮


        response = client.chat.completions.create(  # 把当前上下文和Tools一起发送给豆包
            model=model,

            messages=messages,

            tools=TOOLS,

            tool_choice="auto"  # 允许LLM自己决定是否需要调用工具
        )


        message = response.choices[0].message  # 取得豆包本轮返回的Assistant消息


        messages.append(message.model_dump(exclude_none=True))  # 把豆包本轮消息加入上下文，供下一轮继续使用


        if not message.tool_calls:  # 如果LLM本轮没有要求执行任何Tool
            return message.content  # 说明模型认为信息已经足够，直接返回最终回答


        for tool_call in message.tool_calls:  # 如果LLM一次请求了一个或多个Tools

            tool_name = tool_call.function.name  # 读取LLM决定调用的函数名称


            raw_arguments = tool_call.function.arguments  # 读取模型生成的JSON参数字符串


            tool_arguments = json.loads(raw_arguments or "{}")  # 把JSON字符串转换成Python字典


            print(f"LLM决定调用Tool：{tool_name}")  # 把LLM的Tool决策打印出来


            print(f"Tool参数：{tool_arguments}")  # 显示LLM准备传给函数的参数


            tool_result = execute_tool(  # 真正进入Python工具执行阶段
                tool_name,

                tool_arguments
            )


            print(f"Tool真实结果：{tool_result}")  # 显示Git真正返回的数据


            messages.append(  # 把真实Tool Result加入上下文
                {
                    "role": "tool",

                    "tool_call_id": tool_call.id,  # 告诉LLM这个结果对应哪一次Tool Call

                    "content": json.dumps(
                        tool_result,

                        ensure_ascii=False
                    )
                }
            )


    return "Agent已经达到最大执行步数，停止运行。"  # 防止模型无限循环调用工具


def main():  # 程序正式入口

    user_question = input("请输入Git问题：")  # 让用户通过自然语言提出Git问题


    answer = run_agent(user_question)  # 把问题交给Agent Loop


    print("\n===== Agent最终回答 =====")  # 输出最终结果标题


    print(answer)  # 输出豆包根据真实Git结果生成的答案


if __name__ == "__main__":  # 判断当前文件是否直接运行

    main()  # 启动Agent程序