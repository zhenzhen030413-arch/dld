from pathlib import Path


def diagnose_path(raw_path):
    cleaned_path = raw_path.strip().strip('"').strip()

    if cleaned_path == "":
        return "诊断结果：输入为空，已跳过。"

    target = Path(cleaned_path)

    try:
        absolute_target = target.resolve()

        if target.is_file():
            size_bytes = target.stat().st_size
            suffix = target.suffix

            if suffix == "":
                suffix = "无扩展名"
            if suffix.lower() == ".md":
              file_category = "Markdown学习文档"
            elif suffix.lower() == ".py":
                file_category = "Python源代码"
            else:
              file_category = "其他文件"

            return (
                f"绝对路径：{absolute_target}\n"
                "诊断结果：目标存在，并且是文件。\n"
                f"文件名：{target.name}\n"
                f"扩展名：{suffix}\n"
                f"文件大小：{size_bytes} 字节"
                f"文件类型：{file_category}\n"
            )

        elif target.is_dir():
            return (
                f"绝对路径：{absolute_target}\n"
                "诊断结果：目标存在，并且是文件夹。"
            )

        else:
            return (
                f"绝对路径：{absolute_target}\n"
                "诊断结果：目标不存在。\n"
                "建议：检查当前目录、盘符、文件名和扩展名。"
            )

    except PermissionError:
        return "诊断失败：没有权限访问该路径。"

    except OSError as error:
        return f"诊断失败：发生文件系统错误：{error}"


def main():
    print("=== FDE 批量客户文件路径诊断器 ===")
    print("多个路径请使用英文分号分隔，输入 q 退出。")

    while True:
        user_input = input("\n请输入路径：")

        if user_input.strip().lower() == "q":
            print("程序结束。")
            break

        raw_paths = user_input.split(";")

        for index, raw_path in enumerate(raw_paths, start=1):
            result = diagnose_path(raw_path)

            print(f"\n--- 第 {index} 个路径 ---")
            print(result)


if __name__ == "__main__":
    main()