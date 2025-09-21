import hashlib
m = hashlib.md5()
print(m)
# 更新哈希对象的消息内容
m.update('test'.encode())
print(m.hexdigest())
m = hashlib.md5()
m.update('test'.encode())
print(m.hexdigest())
