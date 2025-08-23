# ~ s1='SPAM'
# ~ s2='SCAM'

# ~ i1=(1,2,3,4)
# ~ i2=(4,5,6,7)

# ~ def intersect(seq1,seq2):
	# ~ res = [x for x in seq1 if x in seq2]
	# ~ return res

# ~ test=intersect(s1,s2)
# ~ print(test)

# ~ test=intersect(i1,i2)
# ~ print(test)

###全局变量与函数本地变量
# ~ username='admin'
# ~ password='Cisc0123'
# ~ def ssh(ip,username,cmd):
	# ~ global res
	# ~ print(f'ssh {ip},user:{username}, pass:{password},execute:{cmd}')
	# ~ res=(f'ssh {ip},user:{username}, pass:{password},execute:{cmd}')

# ~ ssh('1.1.1.1','chang','show ver')


# ~ if res:
	# ~ print("OK")

###参数
# ~ def f(**args):print(args)
# ~ f()
# ~ f(a=100,b=200)

# ~ def f(a,b,c):print(a+b+c)
# ~ l={'a':8,'b':9,'c':10}
# ~ f(**l)

# ~ def f(a,*pargs,**kargs):print(a,pargs,kargs)
# ~ f(1,2,3,4,5,x=10,y=20)

def ctltype(count:int,ws:str)->list:
	return{count:count*ws}
	
print(ctltype(3,'hello '))
