from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
import math
from matplotlib import cm

fig = plt.figure()
ax = plt.axes(projection='3d')

# total_distance = 200
num_r = 150
num_l = 50
r_offset = 20
l_offset = 35

r0 = np.linspace(r_offset,num_r+r_offset,num_r)
lf = np.linspace(l_offset,num_l+l_offset,num_l)
x, y = np.meshgrid(r0,lf)
og_s = x - np.sqrt(x**2 - (y/2)**2)

print("Shape of og s: " + str(og_s.shape))
for i in range(len(og_s)):
    for j in range(len(og_s)):
        if math.isnan(og_s[i,j]):
            og_s[i,j] = lf[i]

s_lines = np.zeros((num_l,num_r))
s_index = 0

for i in range(len(y)): # for each phalange size

    prev_distance = 100000
    cur_distance = 10000

    s = og_s[i,:]

    for j in range(len(s)):
        if math.isnan(s[j]):
            s[j] = 0
    s_guess = 0

    while (prev_distance > cur_distance):

        # guess line
        s_guess = s_guess+0.1
        line = np.ones(num_r)*s_guess

        # calculate distance
        prev_distance = cur_distance
        cur_distance = np.linalg.norm(line-s)
        # print("cur distance: " + str(cur_distance))

    s_lines[s_index,:] = line
    s_index += 1

surf = ax.plot_surface(x,y,og_s, cmap=cm.get_cmap('viridis'), alpha=0.75)

for i in range(0,len(s_lines),15):
    r_vec = r0
    lf_vec = np.ones(num_r)*lf[i]
    s_vec = s_lines[i]
    cur_line = ax.plot3D(r_vec,lf_vec,s_vec,'r',linewidth=2, alpha=1.0)

print("Key distal data:")
index = 45-l_offset
print("Index: " + str(index))
print("lf_value: " + str(lf[index]))
dist_height = s_lines[index,1]
print("s_line height: " + str(dist_height))

print("\nKey proximal data:")
index = 70-l_offset
print("Index: " + str(index))
print("lf_value: " + str(lf[index]))
prox_height = s_lines[index,1]
print("s_line height: " + str(prox_height))

print("Average recommended w0: " + str((dist_height+prox_height)/2))


ax.set_xlabel('r0')
ax.set_ylabel('lf')
ax.set_zlabel('s');

plt.show()

