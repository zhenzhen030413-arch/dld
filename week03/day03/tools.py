# 创建模拟工单数据库。
# 目前先使用 Python 字典模拟真实公司的数据库。
TICKET_DATABASE = {

    # 第一条模拟工单。
    "T1001": {
        "user": "张三",
        "problem": "用户无法登录系统",
        "priority": "P1",
        "status": "处理中"
    },

    # 第二条模拟工单。
    "T1002": {
        "user": "李四",
        "problem": "网页加载速度较慢",
        "priority": "P2",
        "status": "待处理"
    },

    # 第三条模拟工单。
    "T1003": {
        "user": "张三",
        "problem": "用户忘记登录密码",
        "priority": "P2",
        "status": "已解决"
    }
}

def get_ticket(ticket_id):

    
    ticket = TICKET_DATABASE.get(ticket_id)
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

def search_ticket(keyword):
    # 在模拟数据库中搜索工单
    if not isinstance(keyword, str) or not keyword.strip():
        raise ValueError("搜索关键字必须是非空字符串")
        
    keyword = keyword.strip()
    results = []
    for ticket_id, ticket in TICKET_DATABASE.items():
        if keyword in ticket["problem"]:
           results.append({
               "ticket_id": ticket_id,
               "problem": ticket["problem"],

           })
    return results

def get_user_ticket(user_name):
    # 在模拟数据库中搜索用户的工单
    if not isinstance (user_name, str) or not user_name.strip():
        raise ValueError("用户名必须是非空字符串")
        
    user_name = user_name.strip()
    results = []
    for ticket_id, ticket in TICKET_DATABASE.items():
        if user_name == ticket["user"]:
            results.append({
                "ticket_id": ticket_id,
                "ticket": ticket
            })
    return results