x='qytang'
y=88
z='python'

print(x,y,z,sep='...!',file=open('data.txt','w'))
print(open('data.txt','r').read())
