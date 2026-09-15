def get_ticket(ticket_id):

    # 创建一个简单的字典，用来模拟真实公司的工单数据库。
    ticket_database = {

        # 模拟第一条工单数据。
        "T1001": {
            "problem": "用户无法登录系统",
            "priority": "P1",
            "status": "处理中"
        },

        # 模拟第二条工单数据。
        "T1002": {
            "problem": "网页加载速度较慢",
            "priority": "P2",
            "status": "待处理"
        }
    }
    ticket = ticket_database.get(ticket_id)
    if ticket:

        # 如果查到了，就把完整工单信息返回。
        return {
            "ticket_id": ticket_id,
            "problem": ticket["problem"],
            "priority": ticket["priority"],
            "status": ticket["status"]
        }

    # 如果没有查询到工单，则返回错误信息。
    return {
        "error": f"没有找到工单 {ticket_id}"
    }
