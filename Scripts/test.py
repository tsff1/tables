import numpy as np
import random

a = np.array([4,3,5,2,4,3])
c = np.zeros(len(a))

y_min = a[0]
y_c = y_min

for i in range(len(a)-1):
    y_min = min(y_min, a[i])
    if a[i] >= a[i-1]:
        c[i+1] = c[i]+y_c
    else:
        y_c = y_min
        c[i+1] = max(c[i],y_min*(i+2))
    print(y_min*(i+2))
print(c)
print(y_min)
