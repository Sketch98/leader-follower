from matplotlib import pyplot
from numpy import loadtxt, ravel

v = loadtxt('b.csv', delimiter=",", dtype='float', comments="#", skiprows=0,
            usecols=None)
v_hist = ravel(v)  # 'flatten' v
fig = pyplot.figure()
ax1 = fig.add_subplot(111)

n, bins, patches = ax1.hist(v_hist, bins=100, normed=1, facecolor='red')
pyplot.show()
