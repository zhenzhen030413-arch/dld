from pathlib import Path
print("=== FDE 客户文件路径诊断器 ===")
raw_path = input("请输入要检查的文件或文件夹路径：").strip().strip('"')
if raw_path == "":
    print("诊断结果：没有输入路径，程序结束。")
else:
    target = Path(raw_path)
    absolute_target = target.resolve()

    print(f"当前工作目录：{Path.cwd()}")
    print(f"解析后的绝对路径：{absolute_target}")
    if target.exists() and target.is_file():
        size_bytes = target.stat().st_size
        suffix = target.suffix

        if suffix == "":
            suffix = "无扩展名"

        print("诊断结果：目标存在，并且是文件。")
        print(f"文件名：{target.name}")
        print(f"扩展名：{suffix}")
        print(f"文件大小：{size_bytes} 字节")

    elif target.exists() and target.is_dir():
        print("诊断结果：目标存在，并且是文件夹。")

    else:
        print("诊断结果：目标不存在。")
        print("建议：检查当前目录、盘符、文件名和扩展名。")