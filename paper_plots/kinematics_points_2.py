import numpy as np
import matplotlib.pyplot as plt
import math
from matplotlib import cm
from scipy.optimize import curve_fit
from scipy import interpolate
import itertools


fig = plt.figure(figsize=(3,3))
show3DPlots_planar = False
show3DPlots_convex = True

color = itertools.cycle(('k', 'y'))
# color = itertools.cycle(('r', 'g', 'b', 'y'))

#### FIT SHEAR VS NORM RELATIONSHIP ####
def fit_shear_vs_norm(norm_vec, shear_vec, std_dev_vec):

    global fit_func, color
    def fit_func(x, a, b):
        return a * np.power(x, b) + shear_vec[0]   #(shear_vec[0] - norm_vec[0]*shear_vec[0])
        # return a*np.sqrt(x) + c

    # plt.scatter(norm_vec, shear_vec)
    plt.xlim([0,5])
    plt.ylim([0,25])
    pars, cov = curve_fit(f=fit_func, xdata=norm_vec, ydata=shear_vec,
                          p0=[0,0], bounds=(-np.inf,np.inf), maxfev=1000)

    print("Curve fit param results: " + str(pars))

    global calc_shear_from_norm
    def calc_shear_from_norm(norm_stress):
        return fit_func(norm_stress, pars[0], pars[1])

    x_curve_fit = np.linspace(0,100,1000)
    cur_color = next(color)
    plt.plot(x_curve_fit, calc_shear_from_norm(x_curve_fit), cur_color + '--')
    plt.errorbar(norm_vec, shear_vec, yerr=std_dev_vec, marker = 'o', color = cur_color, ls='none', capsize=3)
    # plt.show()
    #### FIT SHEAR VS NORM RELATIONSHIP ####

norm_vec_acrylic = np.asarray([.2333, .4666, 1.1666, 2.333, 4.666])  # n_vs_s_data[:,0]
norm_vec_acrylic = norm_vec_acrylic - norm_vec_acrylic[0]
shear_vec_acrylic = [5.62, 8, 14.14, 16.86, 22.5]  # n_vs_s_data[:,1]
std_dev_vec_acrylic = [.57, .43, .95, .43, 1.6]

norm_vec_paper = norm_vec_acrylic  # n_vs_s_data[:,0]
shear_vec_paper = [1.1, 1.4, 2.5, 4.4, 7.3]  # n_vs_s_data[:,1]
std_dev_vec_paper = [.32, .60, .21, .40, .46]

norm_vec_metal = norm_vec_acrylic  # n_vs_s_data[:,0]
shear_vec_metal = [5, 7.3, 11.6, 15.4, 18]  # n_vs_s_data[:,1]
std_dev_vec_metal = [.38, .39, 1.45, .74, 1.40]

fit_shear_vs_norm(norm_vec_paper, shear_vec_paper, std_dev_vec_paper)
fit_shear_vs_norm(norm_vec_metal, shear_vec_metal, std_dev_vec_metal)
fit_shear_vs_norm(norm_vec_acrylic, shear_vec_acrylic, std_dev_vec_acrylic)
plt.show()

# plt.show()

fig = plt.figure(figsize=(3,3))

#### FIT NORM VS STRAIN RELATIONSHIP ####
def fit_norm_vs_strain(norm_vec, displace_vec):

    global color
    cur_color = next(color)
    plt.scatter(displace_vec/w_0, norm_vec, marker='o', color=cur_color)
    plt.xlim([0,.6])
    plt.ylim([0,15])

    global fit_func_2
    def fit_func_2(x, a, b, c):
        # return a * np.power(x, b)
        return a*x**3 + b*x**2 + c*x

    pars_2, cov = curve_fit(f=fit_func_2, xdata=displace_vec, ydata=norm_vec,
                          p0=[0,0,0], bounds=(-np.inf,np.inf), maxfev=10000)

    print("Curve fit param results: " + str(pars_2))

    global calc_norm_from_displace
    def calc_norm_from_displace(displace_val):
        return fit_func_2(displace_val, pars_2[0], pars_2[1], pars_2[2])

    x_curve_fit = np.linspace(0,w_0,100)

    plt.plot(x_curve_fit/w_0, calc_norm_from_displace(x_curve_fit), '--', color=cur_color, label = next(label))

w_0 = 10
# norm_vec_distInner = [0,7,11,13,16,17]
norm_vec_distInner = [0, 1.5, 2.75, 3.5, 6.5, 13.25]
norm_vec_distOuter = [0,1.8,2.85,3.57,5.7,14.6]
norm_vec_proxInner = [0,.83, 1.66, 2.66, 4.5, 8.33]
norm_vec_proxOuter = [0,1.6, 2.2, 2.4, 3.8, 8.8]
displace_vec = np.asarray([0,1,2,3,4,5])

label = itertools.cycle(('dist in', 'dist out', 'prox in', 'prox out'))
fit_norm_vs_strain(norm_vec_distInner, displace_vec)
fit_norm_vs_strain(norm_vec_distOuter, displace_vec)
fit_norm_vs_strain(norm_vec_proxInner, displace_vec)
fit_norm_vs_strain(norm_vec_proxOuter, displace_vec)
# plt.legend()

# plt.show()
#### FIT NORM VS STRAIN RELATIONSHIP ####


# fig = plt.figure(figsize=(3,5))
pad_x = 40
pad_z = 20
surf_x, surf_z = np.meshgrid(np.linspace(0, pad_x, pad_x), np.linspace(0, pad_z, pad_z))
pad_height = surf_x * 0 + surf_z * 0 + w_0

if (show3DPlots_planar or show3DPlots_convex):
    ax = plt.axes(projection='3d')
    ax.set_box_aspect((2, 1, .5))

def calc_max_shear_force_planar():

    # define for plane
    object_height = w_0 - penetration + surf_z*0 + (surf_x - pad_x/2)*slope

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

    shear_force = np.sum(shear_stress_array)/1000
    norm_force = np.sum(norm_stress_array)/1000
    c_p = -0.5 + pad_x/2 - np.sum(norm_stress_x_moment)/np.sum(norm_stress_array)

    return shear_force, c_p, norm_force


# Calculate max sustainable stress for range of p and slope
cp_z = 0
num_points = 25
num_points_2 = 10
w_0 = 10
displace_max = 5

fn_vec = []
fs_vec = []
cp_vec = []
partial_contact_flag = []
transition_point_flag = []

for p in np.linspace(0.5,4.5,num_points):
    slope_max = (displace_max-p)/(pad_x/2)
    transition_happened = False

    for slope in np.linspace(0,slope_max,num_points, endpoint=False):

        if (slope*pad_x/2 > p):
            print("Partial Contact")
            partial_contact_flag.append(True)
            transition_point_flag.append(False)
            transition_happened = True

        else:
            print("Full contact")
            partial_contact_flag.append(False)



        w_0 = 10
        penetration = p
        # slope = i*.05
        cur_max_shear, cur_cp, cur_fn = calc_max_shear_force_planar()
        print(cur_max_shear)
        fs_vec.append(cur_max_shear)
        cp_vec.append(cur_cp)
        fn_vec.append(cur_fn)
        # max_shear_vec[i], cp_vec[i] = calc_max_shear_force_planar()

fig = plt.figure(figsize=(3,5))
# ax = plt.axes(projection='3d')
# ax.set_ylabel("fs")
# ax.set_xlabel("cp")
# ax.set_box_aspect((1, 1, 1))
plt.title("Planar Object Shear Force")

for i in range(len(partial_contact_flag)):
    print(partial_contact_flag[i])
    # if partial_contact_flag[i]:
        # ax.scatter(cp_vec[i], fn_vec[i], fs_vec[i], marker='x')
        # plt.scatter(cp_vec[i], fs_vec[i], marker='x')

    # else:
        # print("Full Contact")
        # ax.scatter(cp_vec[i], fn_vec[i], fs_vec[i], marker='o')
        # plt.scatter(cp_vec[i], fs_vec[i], marker='o')

cp_range = [0,10]
fn_range = [1,3.5]
cp_array = np.asarray(cp_vec)
fn_array = np.asarray(fn_vec)
fs_array = np.asarray(fs_vec)
cp_plotting = np.linspace(cp_range[0], cp_range[1], num_points_2)
fn_plotting = np.linspace(fn_range[0], fn_range[1], num_points_2)
X, Y = np.meshgrid(cp_plotting,fn_plotting)

Z = interpolate.griddata((cp_array, fn_array), fs_array, (X,Y), method='cubic')
# for i in range(len(Z)):
#     for j in range(len(Z[0])):
#         if math.isnan(Z[i,j]):
#             Z[i,j] = 0
# ax.axes.set_zlim3d(bottom=8)
# ax.plot_surface(X,Y,Z, cmap=cm.get_cmap('inferno'), alpha=0.75)

# print(Y[:,0])
for i in range(1,num_points_2,int(num_points_2/7)):
    plt.plot(X[i],  Z[i], label = "fn=" + str(Y[i,0]), color=next(color))
    # plt.plot(X[i], Z[i])

# plt.ylim(8,17.5)
# plt.legend()
# ax.scatter(cp_vec, fn_vec, fs_vec)

# plt.show()

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

    plt.plot(cp_vec, max_shear_vec, label = 'r=' + str(r), color = next(color))

plt.title("Convex Object Shear Force")
# plt.xlim([0,10])
# plt.ylim([15,30])
# plt.legend()
plt.show()
