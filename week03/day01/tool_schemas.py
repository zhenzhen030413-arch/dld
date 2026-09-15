# 创建工具列表。
# 后面可以不断往这个列表里面增加新的 Tool。
TOOLS = [

    # 第一个工具。
    {
        # 告诉模型，这是一个函数类型的工具。
        "type": "function",

        # function 中描述具体函数。
        "function": {

            # Python 函数名称。
            "name": "get_ticket",

            # 告诉 LLM 这个函数是干什么的。
            "description": "根据工单编号查询工单的问题、优先级和处理状态",

            # 定义调用函数时需要哪些参数。
            "parameters": {

                # 参数整体是一个 JSON Object。
                "type": "object",

                # properties 用于定义每一个参数。
                "properties": {

                    # ticket_id 就是我们的函数参数。
                    "ticket_id": {

                        # ticket_id 的数据类型是字符串。
                        "type": "string",

                        # 参数解释同样会提供给 LLM。
                        "description": "需要查询的工单编号，例如 T1001"
                    }
                },

                # required 表示哪些参数必须存在。
                "required": ["ticket_id"]
            }
        }
    }
]