#encoding:utf-8
import numpy.random as npr 
import numpy as np 
import matplotlib.pyplot as plt 

sample = 500
'''
rn1 = npr.rand(sample,3)
rn2 = npr.randint(0,10,sample)
rn3 = npr.random(sample)
a = [0,25,50,75,100]
rn4 = npr.choice(a,sample)

fig ,((ax1,ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2, figsize=(7,7))

ax1.hist(rn1,bins=25,stacked=True)
ax1.set_title('rand')
ax2.set_ylabel('frequency')
ax1.grid(True)

ax2.hist(rn2,bins=25)
ax2.set_title('randint')
ax2.grid(True)

ax3.hist(rn3,bins=25)
ax3.set_title('random')
ax3.set_ylabel('frequency')
ax3.grid(True)

ax4.hist(rn4,bins=25)
ax4.set_title('choice')
ax4.grid(True)

plt.show()
'''

rm1 = npr.standard_normal(sample)
rm2 = npr.normal(100,20,sample)
rm3 = npr.chisquare(0.5,sample)
rm4 = npr.poisson(1.0,sample)
fig,((ax1,ax2), (ax3,ax4)) = plt.subplots(nrows=2,ncols=2,figsize=(7,7))
ax1.hist(rm1,bins=25)
ax1.set_title('standard normal')
ax1.set_ylabel('frequency')
ax1.grid(True)

ax2.hist(rm2,bins=25)
ax2.set_title('normal(100,20)')
ax2.grid(True)

ax3.hist(rm3,bins=25)
ax3.set_title('frequency')
ax3.set_ylabel('chi square')
ax3.grid(True)

ax4.hist(rm4,bins=25)
ax4.set_title('poisson')
ax4.grid(True)

plt.show()








