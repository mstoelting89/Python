import numpy as np

a = np.array([1,2,3,4])
print(a)

b = np.array([False,True,True,False])

print(b)

print(a[b])

print(a >= 3)

c = a >=3
print(a[c])

print(a[a>=3])