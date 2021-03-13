from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
import math
from matplotlib import cm
from scipy.optimize import curve_fit

# plt.ion()
fig = plt.figure()


#### FIT SHEAR VS NORM RELATIONSHIP ####
norm_vec = [0, 10, 20, 100] #n_vs_s_data[:,0]
shear_vec = [20, 40, 55, 90] #n_vs_s_data[:,1]

def fit_func(x, a, b, c):
    return a * np.power(x, b) + shear_vec[0]
    # return a*np.sqrt(x) + c

plt.scatter(norm_vec, shear_vec)
plt.xlim([0,110])
plt.ylim([0,160])
pars, cov = curve_fit(f=fit_func, xdata=norm_vec, ydata=shear_vec,
                      p0=[0,0,20], bounds=(-np.inf,np.inf), maxfev=10000)

print("Curve fit param results: " + str(pars))

def calc_shear_from_norm(norm_stress):
    return fit_func(norm_stress, pars[0], pars[1], pars[2])

x_curve_fit = np.linspace(0,100,100)
plt.plot(x_curve_fit, calc_shear_from_norm(x_curve_fit))
# plt.show()
#### FIT SHEAR VS NORM RELATIONSHIP ####


#### FIT NORM VS STRAIN RELATIONSHIP ####
norm_vec_2 = [0,6,10,14,15,16]
w_0 = 10
displace_vec = np.asarray([0, 2, 4, 6, 8 ,10])
plt.scatter(displace_vec, norm_vec_2)
def fit_func_2(x, a, b):
    return a * np.power(x, b)

pars_2, cov = curve_fit(f=fit_func_2, xdata=displace_vec, ydata=norm_vec_2,
                      p0=[0,0], bounds=(-np.inf,np.inf), maxfev=10000)

print("Curve fit param results: " + str(pars_2))

def calc_norm_from_displace(displace_val):
    return fit_func_2(displace_val, pars_2[0], pars_2[1])

x_curve_fit = np.linspace(0,w_0,100)

plt.plot(x_curve_fit, calc_norm_from_displace(x_curve_fit))
# plt.show()
#### FIT NORM VS STRAIN RELATIONSHIP ####


pad_x = 40
pad_z = 20

def pad_force_to_stress(force_across_pad):
    return force_across_pad/(pad_x/1000*pad_z/1000)

print("1N to Stress: " + str(pad_force_to_stress(1)))


ax = plt.axes(projection='3d')
surf_x, surf_z = np.meshgrid(np.linspace(0,pad_x,pad_x), np.linspace(0,pad_z,pad_z))
pad_height = surf_x * 0 + surf_z * 0 + w_0
ax.set_box_aspect((2, 1, .5))

def calc_max_shear_force(r_o, penetration):
    # r_o = w_0*3
    # penetration = 3

    object_height = w_0 + r_o - penetration - np.sqrt(r_o ** 2 - (surf_x - pad_x / 2) ** 2 - (surf_z - pad_z / 2) ** 2)

    penetration_array = np.zeros((pad_z,pad_x))
    norm_stress_array = np.zeros((pad_z,pad_x))
    shear_stress_array = np.zeros((pad_z,pad_x))
    for i in range(pad_z):
        for j in range(pad_x):
            # calculate penetration
            penetration_array[i,j] = pad_height[i,j] - object_height[i,j]
            if (penetration_array[i,j] <= 0):
                penetration_array[i,j] = 0
            # calculate norm_stress from penetration
            norm_stress_array[i,j] = calc_norm_from_displace(penetration_array[i,j])
            if (penetration_array[i,j] <= 0):
                norm_stress_array[i,j] = 0
            # calculate shear_stress from norm_stress
            shear_stress_array[i,j] = calc_shear_from_norm(norm_stress_array[i,j])
            if (penetration_array[i,j] <= 0):
                shear_stress_array[i,j] = 0

    fig = plt.figure()
    plt.xlim([0, 110])
    plt.ylim([0, 160])
    ax = plt.axes(projection='3d')
    ax.set_box_aspect((2, 1, .5))

    ax.plot_surface(surf_x, surf_z, pad_height, alpha=0.75)
    ax.plot_surface(surf_x, surf_z, object_height, alpha=0.75)
    ax.plot_surface(surf_x,surf_z,shear_stress_array)

    plt.show()

    stress_integral = np.sum(shear_stress_array)
    print("stress_integral: " + str(stress_integral))

max_shear_vec = np.zeros(10)
for i in range (w_0):
    max_shear_vec[i] = calc_max_shear_force(w_0*4, i)
    # plt.draw()
