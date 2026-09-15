import requests

BASE_URL = "https://jsonplaceholder.typicode.com/todos"


def get_todo(todo_id: int):
    url = f"{BASE_URL}/{todo_id}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # 遇到4xx或5xx状态码时抛出异常
        data = response.json()      # 把响应中的JSON解析成Python数据

        return {
            "success": True,
            "data": data,
        }

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "API请求超时",
        }

    except requests.exceptions.RequestException as error:
        return {
            "success": False,
            "error": str(error),
        }


# 直接运行本文件时，单独测试工具
if __name__ == "__main__":
    result = get_todo(todo_id=9999)
    print(result)