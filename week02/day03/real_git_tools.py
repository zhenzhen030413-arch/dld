import subprocess  # 导入 Python 的 subprocess 模块，它允许 Python 启动并执行外部程序，例如 git

from pathlib import Path  # 导入 Path，用于更加安全、清晰地处理文件夹路径


SCRIPT_DIR = Path(__file__).resolve().parent  # 获取当前 Python 文件所在的绝对文件夹路径


def run_git_command(arguments):  # 定义底层 Git 执行函数，arguments 用来接收 Git 命令参数列表
    result = subprocess.run(  # 真正启动一个外部程序，并等待这个程序执行完成
        ["git", *arguments],  # 要执行的程序是 git，并把 arguments 中的参数展开到 git 后面
        cwd=SCRIPT_DIR,  # 指定 Git 命令从当前脚本所在目录开始执行；Git 会自动向上寻找仓库根目录
        capture_output=True,  # 捕获 Git 的标准输出和错误输出，而不是直接全部显示到终端
        text=True,  # 告诉 Python 把输出读取成字符串，而不是 bytes 二进制数据
        check=False  # Git 命令即使失败也不要直接让 Python 抛异常，由我们自己分析返回码
    )  # subprocess.run 调用结束

    return {  # 把 Git 执行结果整理成结构化字典
        "command": "git " + " ".join(arguments),  # 保存实际执行的 Git 命令，方便排障
        "return_code": result.returncode,  # 保存程序退出码；通常 0 表示执行成功
        "stdout": result.stdout.strip(),  # 保存 Git 正常输出，并去掉首尾多余换行
        "stderr": result.stderr.strip()  # 保存 Git 错误输出，并去掉首尾多余换行
    }  # 返回字典结束


def get_git_status():  # 定义第一个真实 Tool，用来读取 Git 工作区与分支状态
    return run_git_command(["status", "--short", "--branch"])  # 真正执行 git status --short --branch


def get_current_branch():  # 定义第二个真实 Tool，用来读取当前分支
    return run_git_command(["branch", "--show-current"])  # 真正执行 git branch --show-current


def get_git_remotes():  # 定义第三个真实 Tool，用来读取远程仓库配置
    return run_git_command(["remote", "-v"])  # 真正执行 git remote -v


def get_latest_commit():  # 定义第四个真实 Tool，用来读取最近一次 commit
    return run_git_command(["log", "-1", "--oneline"])  # 真正执行 git log -1 --oneline


def main():  # 定义程序入口函数
    print("=== Git Status ===")  # 输出第一个测试标题
    print(get_git_status())  # 调用真实 Git Tool

    print("\n=== Current Branch ===")  # 输出第二个测试标题
    print(get_current_branch())  # 调用当前分支 Tool

    print("\n=== Git Remote ===")  # 输出第三个测试标题
    print(get_git_remotes())  # 调用远程仓库 Tool

    print("\n=== Latest Commit ===")  # 输出第四个测试标题
    print(get_latest_commit())  # 调用最近 Commit Tool


if __name__ == "__main__":  # 判断当前文件是否由 Python 直接运行
    main()  # 调用 main 函数启动程序