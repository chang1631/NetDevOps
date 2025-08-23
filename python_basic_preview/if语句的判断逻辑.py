# ~ a=[123]
# ~ if a:
	# ~ print('It is true')
# ~ else:
	# ~ print('It is false')

'''
Python 会自动判断对象 a 的“真假”，它是通过以下优先顺序来判断的：
💡 Python 的判断步骤如下（从高到低）：
如果类定义了 __bool__() → 就调用它，必须返回 True 或 False。
如果没有 __bool__()，但定义了 __len__() → 就调用 __len__()，长度大于 0 视为 True，否则为 False。
如果两者都没有 → 这个对象在布尔判断下总是为 True。
'''
#例1：定义了 __bool__()
class A:
	def __bool__(self):
		print("called __bool___")
		return False
	
a=A()
if a:
	print("True")
else:
	print("False")	 # 输出 "False"，并打印 "called __bool__"
	
#例2：没有 __bool__()，但有 __len__()
class B:
	def __len__(self):
		print("called __len___")
		return 0
	
b=B()
if b:
	print("True")
else:
	print("False")	 # 输出 "False"，并打印 "called __len__"

#例3：既没有 __bool__() 也没有 __len__()
class C:
    pass

c = C()
if c:
    print("True")   # 永远是 True
else:
    print("False")
    
#总结
#当你写 if obj: 时，Python 会按顺序尝试调用 obj.__bool__() → obj.__len__() → 默认返回 True。

