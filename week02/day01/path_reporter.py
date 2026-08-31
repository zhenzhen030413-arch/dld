from pathlib import Path
import json


BASE_DIR = Path(__file__).resolve().parent #BASE_DIR = path_reporter.py 所在的文件夹


def load_config(config_path):
    with config_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def load_paths(input_path):
    with input_path.open("r", encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip()]


def diagnose_path(raw_path, include_file_size):
    result = {"input_path": raw_path}

    try:
        target = Path(raw_path)

        if not target.is_absolute():
            target = BASE_DIR / target

        target = target.resolve()
        result["absolute_path"] = str(target)

        if target.is_file():
            result["exists"] = True
            result["type"] = "file"
            result["suffix"] = target.suffix or "无扩展名"

            if include_file_size:
                result["size_bytes"] = target.stat().st_size

        elif target.is_dir():
            result["exists"] = True
            result["type"] = "folder"

        else:
            result["exists"] = False
            result["type"] = "missing"

    except PermissionError as error:
        result["exists"] = None
        result["type"] = "error"
        result["error"] = f"没有访问权限：{error}"

    except OSError as error:
        result["exists"] = None
        result["type"] = "error"
        result["error"] = f"文件系统错误：{error}"

    return result


def build_summary(results):
    summary = {
        "total": len(results),
        "file": 0,
        "folder": 0,
        "missing": 0,
        "error": 0
    }

    for result in results:
        result_type = result["type"]

        if result_type in summary:
            summary[result_type] += 1

    return summary


def save_report(output_path, report):
    with output_path.open("w", encoding="utf-8") as file:
        json.dump(
            report,
            file,
            ensure_ascii=False,
            indent=2
        )


def main():
    config_path = BASE_DIR / "config.json"

    try:
        config = load_config(config_path)

        input_path = BASE_DIR / config["input_file"]
        output_path = BASE_DIR / config["output_file"]
        include_file_size = config.get("include_file_size", True)

        raw_paths = load_paths(input_path)

    except FileNotFoundError as error:
        print(f"启动失败：找不到文件：{error}")
        return

    except json.JSONDecodeError as error:
        print(
            "启动失败：JSON格式错误，"
            f"第{error.lineno}行，第{error.colno}列。"
        )
        return

    except KeyError as error:
        print(f"启动失败：配置中缺少字段：{error}")
        return

    results = []

    for raw_path in raw_paths:
        result = diagnose_path(raw_path, include_file_size)
        results.append(result)
        print(f"{result['input_path']} -> {result['type']}")

    report = {
        "project_name": config.get("project_name", "未命名项目"),
        "source_file": str(input_path.resolve()),
        "summary": build_summary(results),
        "results": results,
        "operator":config["operator"]
    }

    save_report(output_path, report)

    print(f"\n检查完成，共处理 {len(results)} 个路径。")
    print(f"报告已生成：{output_path.resolve()}")


if __name__ == "__main__":
    main()