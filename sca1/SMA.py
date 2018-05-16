import numpy as np
import matplotlib.pyplot as plt 

plt.figure(figsize = (10,6))


y = np.array([-3,-2.5,-1.5,-0.5,1,1.5,2.8])
x = np.arange(len(y))
A = np.vstack([x,np.ones_like(x)]).T
m1,c1 = np.linalg.lstsq(A,y)[0]
plt.plot(x , y , 'o')
plt.plot(x , m1 * x + c1,'r')
plt.legend()
plt.show()