import json
from pathlib import Path


def detect_category(issue):  # 定义 detect_category 函数，它负责判断客户问题属于什么类型
    issue_lower = issue.lower()  # 把客户输入的英文字符统一转换成小写，避免 Git 和 git 被当成两个词

    if any(word in issue_lower for word in ["git", "github", "branch", "commit", "push"]):  # 判断问题中是否包含 Git 相关关键词
        return "git"  # 如果发现 Git 相关关键词，就把问题类型返回为 git

    if any(word in issue_lower for word in ["api", "http", "401", "403", "json"]):  # 判断问题中是否包含 API 相关关键词
        return "api"  # 如果发现 API 相关关键词，就把问题类型返回为 api

    if any(word in issue_lower for word in ["python", "pip", "module", "venv"]):  # 判断问题中是否包含 Python 相关关键词
        return "python"  # 如果发现 Python 相关关键词，就把问题类型返回为 python

    if any(word in issue_lower for word in ["html", "css","javascript", "网页", "frontend"]):  # 判断问题中是否包含前端相关关键词
        return "frontend"  # 如果发现前端相关关键词，就把问题类型返回为 frontend

    return "general"  # 如果上面的关键词都没有命中，就把问题暂时归类为 general



def git_tool(issue):  # 定义 Git 工具，这个函数专门处理 Git/GitHub 类问题
    return {  # 返回一个字典，让结果成为结构化数据
        "problem": issue,  # 保存客户最初输入的问题
        "owner": "Git / DevOps",  # 指定这种问题通常属于 Git 或 DevOps 范畴
        "checks": [  # checks 字段保存建议执行的一组检查步骤
            "运行 git status 检查仓库状态",  # 第一步检查当前 Git 工作区状态
            "运行 git branch 检查当前分支",  # 第二步检查当前到底在哪个分支
            "运行 git remote -v 检查远程仓库",  # 第三步检查本地仓库连接的是哪个 GitHub 仓库
            "运行 git push 检查代码是否已经上传"  # 第四步检查本地 commit 是否真正 push 到远程仓库
        ]  # Git 检查列表结束
    }  # Git 工具返回的字典结束

def frontend_tool(issue):  # 定义前端工具，这个函数专门处理前端相关问题
    return {  # 返回一个字典，让结果成为结构化数据
        "problem": issue,
        "owner": "Frontend",
        "checks": [
            "检查 HTML 结构是否正确",
            "检查 CSS 是否正确加载",
            "检查 JavaScript 控制台是否有报错",
            "检查网络请求是否成功"
        ]
    }

def api_tool(issue):  # 定义 API 工具，它负责处理 HTTP/API 相关的问题
    return {  # 返回结构化字典
        "problem": issue,  # 保存原始问题
        "owner": "Backend / API",  # 标记问题所属领域
        "checks": [  # 保存 API 故障的检查步骤
            "检查 API URL 是否正确",  # 第一步确认请求地址
            "检查 HTTP Method 是否正确",  # 第二步检查 GET、POST 等请求方式
            "检查 Authorization 信息",  # 第三步检查身份认证信息
            "检查返回的 HTTP Status Code"  # 第四步检查 200、401、403、500 等状态码
        ]  # API 检查列表结束
    }  # API 工具返回结果结束


def python_tool(issue):  # 定义 Python 工具，专门处理 Python 环境和运行问题
    return {  # 返回结构化字典
        "problem": issue,  # 保存客户原始问题
        "owner": "Python",  # 标记问题所属技术领域
        "checks": [  # 保存 Python 故障检查步骤
            "运行 python --version",  # 检查当前 Python 版本
            "运行 pip --version",  # 检查 pip 是否存在以及对应哪个 Python
            "检查虚拟环境是否已经激活",  # 检查项目是否处于正确的虚拟环境
            "检查缺失的 Python package"  # 检查是否因为没有安装依赖导致程序失败
        ]  # Python 检查列表结束
    }  # Python 工具返回结果结束


def general_tool(issue):  # 定义兜底工具，当 Agent 无法识别问题类型时调用这个工具
    return {  # 返回结构化字典
        "problem": issue,  # 保存客户原始问题
        "owner": "Unknown",  # 暂时无法确定负责领域
        "checks": [  # 给出通用调查方法
            "收集完整报错信息",  # 要求先得到完整错误日志
            "确认问题发生步骤",  # 明确客户执行了什么操作以后出现错误
            "确认运行环境",  # 确认 Windows、Python、Node 等环境信息
            "进一步人工分析"  # 信息不足时交给工程师继续判断
        ]  # 通用检查列表结束
    }  # 通用工具结果结束


TOOLS = {  # 创建一个工具注册表，用字典保存“问题类型”和“函数”之间的对应关系
    "git": git_tool,  # 当问题类型是 git 时使用 git_tool
    "api": api_tool,  # 当问题类型是 api 时使用 api_tool
    "python": python_tool,  # 当问题类型是 python 时使用 python_tool
    "general": general_tool, # 无法识别时使用 general_tool
    "frontend": frontend_tool  # 当问题类型是 frontend 时使用 frontend_tool
}  # 工具注册表定义结束


def run_agent(issue):  # 定义整个 Agent 的核心执行函数
    category = detect_category(issue)  # 第一步，让 Router 判断客户问题属于哪个类别
    selected_tool = TOOLS[category]  # 第二步，根据类别从工具注册表中找到正确的工具函数
    tool_result = selected_tool(issue)  # 第三步，真正调用选中的 Tool，并把客户问题传给它

    result = {  # 创建最终 Agent 输出的数据结构
        "input": issue,  # 保存 Agent 收到的原始输入
        "category": category,  # 保存 Agent 判断出来的问题类型
        "tool_used": selected_tool.__name__,  # 保存 Agent 实际调用的函数名称
        "result": tool_result  # 保存 Tool 执行完成以后返回的结果
    }  # 最终结果字典定义结束

    return result  # 把完整 Agent 执行结果返回给调用者


def main():  # 定义程序入口函数，让整个程序的执行逻辑集中在这里
    try:  # 开始异常处理，避免程序出现错误时直接崩溃
        user_issue = input("请输入客户遇到的问题：")  # 从终端读取用户输入的问题

        agent_result = run_agent(user_issue)  # 把客户问题交给 Agent 进行判断和处理

        print("\nAgent 分析结果：")  # 在终端输出一个结果标题
        print(json.dumps(agent_result, ensure_ascii=False, indent=2))  # 把 Python 字典转换成易读的 JSON 格式并显示中文

        output_path = Path(__file__).resolve().parent / "agent_result.json"

        with open("agent_result.json", "w", encoding="utf-8") as file:  # 创建或覆盖 agent_result.json 文件，并指定 UTF-8 编码
            json.dump(agent_result, file, ensure_ascii=False, indent=2)  # 把 Agent 的结果正式写入 JSON 文件

        print("\n结果已经保存到 agent_result.json")  # 告诉用户 JSON 文件已经成功生成

    except Exception as error:  # 如果上面的程序执行过程中出现任何异常，就进入这里
        print(f"程序运行失败：{error}")  # 输出具体的错误信息，方便工程师排查问题


if __name__ == "__main__":  # 判断当前 Python 文件是不是被直接运行，而不是被其他文件 import
    main()  # 如果当前文件是直接运行的，就正式调用 main 函数启动程序