import numpy as np
import time 
from math import sin,cos,pi 
from matplotlib import cm
from matplotlib import pyplot as plt
from matplotlib import collections

def iter_point(c):
	z = c
	for i in range(1,100):
		if abs(z) > 2:
			break
		z = z*z+c
	return i

def draw_mandelbrot(cx,cy,d):
	x0,x1,y0,y1 = cx-d,cx+d,cy-d,cy+d
	y,x = np.ogrid[y0:y1:200j,x0:x1:200j]
	c = x+y*1j
	start = time.clock()
	mandelbrot = np.frompyfunc(iter_point,1,1)(c).astype(np.float)
	print("time = ",time.clock()-start)
	plt.imshow(mandelbrot,cmap = cm.jet,extent = [x0,x1,y0,y1])
	plt.gca().set_axis_off()

def test_mandelbrot():
	x,y = 0.27322626,0.595153338

	plt.subplot(231)
	draw_mandelbrot(-0.5,0,1.5)
	for i in range(2,7):
		plt.subplot(230+i)
		draw_mandelbrot(x,y,0.2**(i-1))
	plt.subplots_adjust(0.02,0,0.98,1,0.02,0)
	plt.show()

def ifs(p,eq,init,n):
	pos = np.ones(3,dtype = np.float)
	pos[:2] = init
	p = np.add.accumulate(p)
	rands = np.random.rand(n)
	select = np.ones(n,dtype = np.int)*(n-1)
	for i,x in enumerate(p[::-1]):
		select[rands<x] = len(p)-i-1

	result = np.zeros((n,2),dtype = np.float)
	c = np.zeros(n,dtype = np.float)

	for i in range(n):
		eqidx = select[i]
		tmp = np.dot(eq[eqidx],pos)
		pos[:2] = tmp

		result[i] = tmp
		c[i] = eqidx

	return result[:,0],result[:,1],c

def test_leaf():
	eq1 = np.array([[0,0,0],[0,0.16,0]])
	p1 = .01

	eq2 = np.array([[0.2,-0.26,0],[0.23,.22,1.6]])
	p2 = .07

	eq3 = np.array([[-.15,.28,0],[.26,.24,.44]])
	p3 = .07

	eq4 = np.array([[.85,.04,0],[-.04,.85,1.6]])
	p4 = .85

	start = time.clock()
	x,y,c = ifs([p1,p2,p3,p4],[eq1,eq2,eq3,eq4],[0,0],100000)
	time.clock()-start
	plt.figure(figsize = (6,6))
	plt.subplot(121)
	plt.scatter(x,y,s = 1,c = "g", marker = "s", linewidths = 0)
	plt.axis("equal")
	plt.axis("off")
	plt.subplot(122)
	plt.scatter(x,y,s = 1,c = c,marker = "s", linewidths = 0)
	plt.axis("equal")
	plt.axis("off")
	plt.subplots_adjust(left = 0,right = 1,bottom = 0,top = 1,wspace = 0,hspace = 0)
	plt.gcf().patch.set_facecolor("#D3D3D3")
	plt.show()


class L_System(object):
	def __init__(self,rule):
		info = rule['S']

		for i in range(rule['iter']):
			ninfo = []

			for c in info:
				if c in rule:
					ninfo.append(rule[c])
				else:
					ninfo.append(c)
				info = "".join(ninfo)
			self.rule = rule
			self.info = info

	def get_lines(self):
		d = self.rule['direct']
		a = self.rule['angle']
		p = (.0,.0)
		l = 1.0
		lines = []
		stack = []
		for c in self.info:
			if c in "Ff":
				r = d*pi/180
				t = p[0]+l*cos(r),p[1]+l*sin(r)
				lines.append(((p[0],p[1]),(t[0],t[1])))
				p = t
			elif c == "+":
				d += a
			elif c == "-":
				d -= a
			elif c == "[":
				stack.append((p,d))
			elif c == "]":
				p,d = stack[-1]
				del stack[-1]
		return lines


rules = [
	{
		"F":"F+F--F+F","S":"F",
		"direct":180,
		"angle":60,
		"iter":5,
		"title":"Koch"
	},
	{
		"X":"X+YF+","Y":"-FX-Y","S":"FX",
		"direct":0,
		"angle":90,
		"iter":13,
		"title":"Dragon"
	},
	{
		"f":"F-f-F","F":"f+F+f","S":"f",
		"direct":0,
		"angle":60,
		"iter":7,
		"title":"Triangle"
	},
	{
		"X":"F-[[X]+X]+F[+FX]-X","F":"FF","S":"X",
		"direct":-45,
		"angle":25,
		"iter":6,
		"title":"Plant"
	},
	{
		"S":"X","X":"-YF+XFX+FY-","Y":"+XF-YFY-FX+",
		"direct":0,
		"angle":90,
		"iter":6,
		"title":"Hilbert"
	},
	{
		"S":"L--F--L--F","L":"+R-F-R+","R":"-L+F+L-",
		"direct":0,
		"angle":45,
		"iter":10,
		"title":"Sierpinski"
	},
]
def draw(ax,rule,iter = None):
	if iter != None:
		rule["iter"] = iter
	lines = L_System(rule).get_lines()
	linecollections = collections.LineCollection(lines)
	ax.add_collection(linecollections,autolim = True)
	ax.axis("equal")
	ax.set_axis_off()
	ax.set_xlim(ax.dataLim.xmin,ax.dataLim.xmax)
	ax.invert_yaxis()

def test():
	fig = plt.figure(figsize = (7,4.5))
	fig.patch.set_facecolor("papayawhip")

	for i in range(6):
		ax = fig.add_subplot(231+i)
		draw(ax,rules[i])

	fig.subplots_adjust(left = 0,right = 1,bottom = 0,top = 1,wspace = 0,hspace = 0)
	plt.show()

if  __name__ == '__main__':
	#test_mandelbrot()
	#test_leaf()
	test()
