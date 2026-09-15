1.GET 和 POST 最大区别是什么？
get通常用于读取资源，按照http协议应该是安全且幂等的。post用于提交数据和创建资源，一般是不幂等的。GET参数一般出现在URL  Query中，POST参数一般保存在body中。