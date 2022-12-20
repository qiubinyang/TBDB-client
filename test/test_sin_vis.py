import matplotlib.pyplot as plt
import math
import random

x = [i for i in range(1000)]
y = [(1.5+math.sin((1/(10*math.pi))*i)+random.uniform(-0.5, 0.5))/10 for i in x]

plt.figure(figsize=(15, 5))
plt.plot(x, y)
plt.show()
