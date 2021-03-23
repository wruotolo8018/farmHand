from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
import math
from matplotlib import cm
from scipy.optimize import curve_fit
from scipy.signal import bspline

fig = plt.figure(figsize=(3,3))

#### FIT SHEAR VS NORM RELATIONSHIP ####
def fit_shear_vs_norm(norm_vec, shear_vec):

    global fit_func
    def fit_func(x, a, b):
        return a * np.power(x, b) + shear_vec[0]
        # return a*np.sqrt(x) + c

    plt.scatter(norm_vec, shear_vec)
    # plt.xlim([0,20000])
    plt.ylim([0,14000])
    pars, cov = curve_fit(f=fit_func, xdata=norm_vec, ydata=shear_vec,
                          p0=[0,0], bounds=(-np.inf,np.inf), maxfev=1000)

    # print("Curve fit param results: " + str(pars))

    global calc_shear_from_norm
    def calc_shear_from_norm(norm_stress):
        return fit_func(norm_stress, pars[0], pars[1])

    x_curve_fit = np.linspace(0,10000,1000)
    plt.plot(x_curve_fit, calc_shear_from_norm(x_curve_fit))
    # plt.show()
    #### FIT SHEAR VS NORM RELATIONSHIP ####

norm_vec_acrylic = np.asarray([0, 1, 2, 3])/0.04/0.01 #n_vs_s_data[:,0]
shear_vec_acrylic = np.asarray([2.0, 3.5, 4.5, 5.0])/0.04/0.01 #n_vs_s_data[:,1]

# norm_vec_wood = [0, 5, 10, 20, 30] #n_vs_s_data[:,0]
# shear_vec_wood = [10, 13, 15, 16, 16] #n_vs_s_data[:,1]
#
# norm_vec_metal = [0, 10, 20, 30] #n_vs_s_data[:,0]
# shear_vec_metal = [12, 18, 23, 25] #n_vs_s_data[:,1]

# fit_shear_vs_norm(norm_vec_wood, shear_vec_wood)
# fit_shear_vs_norm(norm_vec_metal, shear_vec_metal)
fit_shear_vs_norm(norm_vec_acrylic, shear_vec_acrylic)

plt.show()


##### Dist vs prox stress comparison #####
A_dist = .040*.020
A_prox = .070*.020

# Sweep ft and rd?
lp = 0.070
rp = 0.010
ld = 0.040

def calc_dist_shear(ft,rd):
    fnd = rd*ft/ld
    norm_stress_d_avg = fnd/A_dist
    # print("Norm stress d avg: " + str(norm_stress_d_avg))
    shear_stress_d_avg = calc_shear_from_norm(norm_stress_d_avg)
    shear_force_max = shear_stress_d_avg*A_dist
    return shear_force_max, fnd

def calc_prox_shear(ft):
    fnp = rp*ft/lp
    norm_stress_p_avg = fnp/A_prox
    shear_stress_p_avg = calc_shear_from_norm(norm_stress_p_avg)
    shear_force_max = shear_stress_p_avg*A_prox
    return shear_force_max, fnp

#### Sample calcs ####
ft = 10
rd = 0.01

print("Fnd: " + str(calc_dist_shear(ft,rd)[1]))
print("Fsd: " + str(calc_dist_shear(ft,rd)[0]))
print("Fnp: " + str(calc_prox_shear(ft)[1]))
print("Fsp: " + str(calc_prox_shear(ft)[0]))


ft_axis = np.linspace(5,20,100)
rd_axis = np.linspace(0,0.02,100)

fig = plt.figure()
surf_ft, surf_rd = np.meshgrid(ft_axis, rd_axis)
height = (calc_prox_shear(surf_ft)[0] + calc_dist_shear(surf_ft,surf_rd)[0])/(calc_prox_shear(surf_ft)[1] + calc_dist_shear(surf_ft,surf_rd)[1])
# height = (calc_prox_shear(surf_ft)[0] + calc_dist_shear(surf_ft,surf_rd)[0])

ax = plt.axes(projection='3d')
ax.set_box_aspect((1, 1, 1))
ax.plot_surface(surf_ft, surf_rd, height, alpha=0.75)
ax.set_zlim3d((0,10))
ax.set_xlabel("Tendon Force (N)")
ax.set_ylabel("Distal Joint Radius (m)")
# ax.set_zlabel("Total Shear/Total Normal")

plt.show()






'''
fig = plt.figure(figsize=(3,3))

#### FIT NORM VS STRAIN RELATIONSHIP ####
def fit_norm_vs_strain(norm_vec, displace_vec):

    plt.scatter(displace_vec, norm_vec)
    global fit_func_2
    def fit_func_2(x, a, b):
        return a * np.power(x, b)

    pars_2, cov = curve_fit(f=fit_func_2, xdata=displace_vec, ydata=norm_vec,
                          p0=[0,0], bounds=(-np.inf,np.inf), maxfev=10000)

    print("Curve fit param results: " + str(pars_2))

    global calc_norm_from_displace
    def calc_norm_from_displace(displace_val):
        return fit_func_2(displace_val, pars_2[0], pars_2[1])

    x_curve_fit = np.linspace(0,w_0,100)

    plt.plot(x_curve_fit, calc_norm_from_displace(x_curve_fit))

w_0 = 10
norm_vec_distInner = [0,7,11,13,16,17]
norm_vec_distOuter = [0,5,12,13,14.5,15]
norm_vec_proxInner = [0,6.5,10.5,13.5,14,17]
norm_vec_proxOuter = [0,6,10,14,15,16]
displace_vec = np.asarray([0, 2, 4, 6, 8, 10])

fit_norm_vs_strain(norm_vec_distInner, displace_vec)
fit_norm_vs_strain(norm_vec_distOuter, displace_vec)
fit_norm_vs_strain(norm_vec_proxInner, displace_vec)
fit_norm_vs_strain(norm_vec_proxOuter, displace_vec)

plt.show()
#### FIT NORM VS STRAIN RELATIONSHIP ####


fig = plt.figure(figsize=(3,5))
pad_x = 40
pad_z = 20
surf_x, surf_z = np.meshgrid(np.linspace(0, pad_x, pad_x), np.linspace(0, pad_z, pad_z))
pad_height = surf_x * 0 + surf_z * 0 + w_0

if (show3DPlots_planar or show3DPlots_convex):
    ax = plt.axes(projection='3d')
    ax.set_box_aspect((2, 1, .5))

def calc_max_shear_force_planar():
    # r_o = w_0*3
    # penetration = 3

    # ob_center_x = cp_x
    # ob_center_z = cp_z

    # define for plane
    object_height = w_0 - penetration + surf_z*0 + (surf_x - pad_x/2)*slope

        # w_0 + r_o - penetration - np.sqrt(r_o ** 2 - (surf_x - pad_x / 2 - ob_center_x) ** 2 - (surf_z - pad_z / 2 - ob_center_z) ** 2)

    penetration_array = np.zeros((pad_z,pad_x))
    norm_stress_array = np.zeros((pad_z,pad_x))
    shear_stress_array = np.zeros((pad_z,pad_x))
    norm_stress_x_moment = np.zeros((pad_z,pad_x))

    for i in range(pad_z):
        for j in range(pad_x):
            # calculate penetration
            penetration_array[i,j] = pad_height[i,j] - object_height[i,j]
            if (penetration_array[i,j] <= 0):
                penetration_array[i,j] = 0
            if (penetration_array[i,j] > w_0):
                penetration_array[i,j] = w_0

            # calculate norm_stress from penetration
            norm_stress_array[i,j] = calc_norm_from_displace(penetration_array[i,j])
            if (penetration_array[i,j] <= 0):
                norm_stress_array[i,j] = 0

            # calculate x moment of norm stress
            norm_stress_x_moment[i,j] = norm_stress_array[i,j]*j

            # calculate shear_stress from norm_stress
            shear_stress_array[i,j] = calc_shear_from_norm(norm_stress_array[i,j])
            if (penetration_array[i,j] <= 0):
                shear_stress_array[i,j] = 0

    if (show3DPlots_planar):
        fig = plt.figure()
        # plt.xlim([0, 110])
        # plt.ylim([0, 160])
        ax = plt.axes(projection='3d')
        ax.set_box_aspect((2, 1, .5))

        ax.plot_surface(surf_x, surf_z, pad_height, alpha=0.75)
        ax.plot_surface(surf_x, surf_z, object_height, alpha=0.75)
        ax.plot_surface(surf_x, surf_z, shear_stress_array)

        plt.show()

    stress_integral = np.sum(shear_stress_array)/1000
    c_p = -0.5 + pad_x/2 - np.sum(norm_stress_x_moment)/np.sum(norm_stress_array)

    print("stress_integral: " + str(stress_integral))
    print("c_p mag: " + str(c_p))

    return stress_integral, c_p


# Calculate max sustainable stress for range of cp
cp_z = 0
num_points = 15
w_0 = 10
for p in range(10):
    slope_max = (w_0-p)/(pad_x/2)
    max_shear_vec = []  # np.zeros(num_points)
    cp_vec = []  # np.zeros(num_points)
    for slope in np.linspace(0,slope_max,num_points, endpoint=False):
        # cp_x = i
        w_0 = 10
        penetration = p
        # slope = i*.05
        cur_max_shear, cur_cp = calc_max_shear_force_planar()
        max_shear_vec.append(cur_max_shear)
        cp_vec.append(cur_cp)
        # max_shear_vec[i], cp_vec[i] = calc_max_shear_force_planar()

    plt.plot(cp_vec, max_shear_vec)

# fig = plt.figure(figsize=(5,5))
plt.xlim((0,10))
plt.ylim((15,33))
plt.show()

def calc_max_shear_force_convex():
    # r_o = w_0*3
    # penetration = 3

    ob_center_x = tip_x
    ob_center_z = cp_z

    # define for plane
    object_height = w_0 + r_o - penetration - np.sqrt(r_o ** 2 - (surf_x - pad_x / 2 - ob_center_x) ** 2 - (surf_z - pad_z / 2 - ob_center_z) ** 2)
    print("just calced ob height")
    penetration_array = np.zeros((pad_z, pad_x))
    norm_stress_array = np.zeros((pad_z, pad_x))
    shear_stress_array = np.zeros((pad_z, pad_x))
    norm_stress_x_moment = np.zeros((pad_z, pad_x))

    for i in range(pad_z):
        for j in range(pad_x):
            # calculate penetration
            penetration_array[i, j] = pad_height[i, j] - object_height[i, j]
            if (penetration_array[i, j] <= 0):
                penetration_array[i, j] = 0

            # calculate norm_stress from penetration
            norm_stress_array[i, j] = calc_norm_from_displace(penetration_array[i, j])
            if (penetration_array[i, j] <= 0):
                norm_stress_array[i, j] = 0

            # calculate x moment of norm stress
            norm_stress_x_moment[i, j] = norm_stress_array[i, j] * j

            # calculate shear_stress from norm_stress
            shear_stress_array[i, j] = calc_shear_from_norm(norm_stress_array[i, j])
            if (penetration_array[i, j] <= 0):
                shear_stress_array[i, j] = 0

    if (show3DPlots_convex):
        fig = plt.figure()
        plt.xlim([0, 110])
        plt.ylim([0, 160])
        ax = plt.axes(projection='3d')
        ax.set_box_aspect((2, 1, .5))

        ax.plot_surface(surf_x, surf_z, pad_height, alpha=0.75)
        ax.plot_surface(surf_x, surf_z, object_height, alpha=0.75)
        ax.plot_surface(surf_x, surf_z, shear_stress_array)

        plt.show()

    stress_integral = np.sum(shear_stress_array)/1000
    c_p = .5-(pad_x / 2 - np.sum(norm_stress_x_moment) / np.sum(norm_stress_array))

    print("stress_integral: " + str(stress_integral))
    print("c_p mag: " + str(c_p))

    return stress_integral, c_p


fig = plt.figure(figsize=(3,5))
# ax = plt.axes(projection='2d')
# ax.set_box_aspect((1,1))

# Calculate max sustainable stress for range of cp
cp_z = 0
for r in [20*w_0, 15*w_0, 10*w_0, 7*w_0, 6*w_0]:
    num_points = 50
    max_shear_vec = np.zeros(num_points)
    cp_vec = np.zeros(num_points)
    for i in range(num_points):
        tip_x = i  #*((r/2)/num_points)
        w_0 = 10
        cp_z = 0
        r_o = r
        penetration = 5
        slope = i*.05
        max_shear_vec[i], cp_vec[i] = calc_max_shear_force_convex()

    plt.plot(cp_vec, max_shear_vec)

plt.xlim([0,10])
plt.ylim([15,30])
plt.show()

'''