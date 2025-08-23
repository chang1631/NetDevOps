# ~ s='lichang'
# ~ for x in s:print(x,end=' ')

# ~ T = ('welcome','to','shanghai')
# ~ for x in T:print(x,end=' ')

# ~ T=[(1,2),(3,4),(5,6)]
# ~ for (x,y) in T:print(x,'加',y,'等于',str(x+y))

# ~ D=dict(zip(['a','b','c'],[1,2,3]))
# ~ for key in D:print(key,'=>',D[key])

l1=list(range(1,11))

max=100
for x in l1:
		if x>max:
			break
		print(x)
else:
	print("all under max")


l1=list(range(-5,5)),list(range(5,-5,-1))
print(l1)

for x in range(5,-5,-1):
	print(x,end=' ')
