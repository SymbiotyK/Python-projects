import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from matplotlib.pylab import subplots
fig,ax = subplots()
x = np.arange(20)
frames = [ax.plot(x,x,x[i],x[i],'ro',ms=5+i*10) for i in x]

g=animation.ArtistAnimation(fig,frames,interval=1)
plt.show()