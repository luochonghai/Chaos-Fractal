from matplotlib import pyplot as plt

N = 3
M = 10
for i in range(-M*M,M*M):
	plt.plot([-i,i],[-N,N],color = 'coral')
plt.hlines(-1.15,-M*M,M*M,color = 'coral')
plt.hlines(1.15,-M*M,M*M,color = 'coral')
plt.show()
