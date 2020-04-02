import numpy as np

a = np.array([1,2,3,4,5,6,7,8])

reshaped = a.reshape(2,4)

print(reshaped[0])
print(reshaped[1])

reshaped = a.reshape(4,-1)
print(reshaped)
