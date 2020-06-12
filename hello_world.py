var1 = 4
var2 = var1 *2
var3 = var2  *2 -1
var4 = var3 + 1
var5 = var4 + 7
var6 = var1 *10  + 2

print(range(1,7))
for thing in list(range(1,7)):
    newvar = 'var'+ str(thing)
    print(globals()[newvar])

if 1==2 :
   print('hello world')
else:
  print('that is false')
