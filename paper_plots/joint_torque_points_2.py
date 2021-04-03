from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
import math
from matplotlib import cm
from scipy.optimize import curve_fit
from scipy import interpolate
from scipy.signal import bspline
import itertools



#### FIT SHEAR VS NORM RELATIONSHIP ####
def fit_shear_vs_norm(norm_vec, shear_vec, std_dev_vec):

    global fit_func, color
    def fit_func(x, a, b):
        return a * np.power(x, b) # + shear_vec[0]   #(shear_vec[0] - norm_vec[0]*shear_vec[0])
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

# if (show3DPlots_planar or show3DPlots_convex):
#     ax = plt.axes(projection='3d')
#     ax.set_box_aspect((2, 1, .5))

def calc_max_shear_force_planar(penetration, slope):
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

    shear_stress_integral = np.sum(shear_stress_array)/1000
    norm_stress_integral = np.sum(norm_stress_array)/1000
    c_p = -0.5 + pad_x/2 - np.sum(norm_stress_x_moment)/np.sum(norm_stress_array)

    # print("stress_integral: " + str(shear_stress_integral))
    # print("c_p mag: " + str(c_p))
    # print("penetration: " + str(penetration))
    # print()

    return shear_stress_integral, c_p, norm_stress_integral

def cp_fn_to_fs_planar(cp, fn):
    # max_pen = w_0
    cp = np.abs(cp)
    slope_increment = 0.01
    pen_increment = 0.05
    penetration = 0.01
    cur_slope = 0.01
    cur_fn = 0

    # print("Fn: " + str(fn))
    # print("Cp: " + str(cp))

    while cur_fn <= fn:
        max_slope = (w_0 - penetration) / (pad_x / 2)
        cur_slope = 0.00
        cur_cp = 0.0
        # cur_slope = 0
        while cur_cp <= cp:
            shear_stress_int, cur_cp, cur_fn = calc_max_shear_force_planar(penetration, cur_slope)
            cur_slope += slope_increment
            # print("God dammit")
        penetration += pen_increment

    # print("Final penetration: " + str(penetration))
    # print("Final slope: " + str(cur_slope))
    # print("Resultant max shear force: " + str(shear_stress_int))

    return shear_stress_int, cur_fn, cur_cp



# Calculate max sustainable stress for range of cp
# cp_z = 0
# num_points = 15
# w_0 = 10
# for p in range(10):
#     slope_max = (w_0-p)/(pad_x/2)
#     max_shear_vec = []  # np.zeros(num_points)
#     cp_vec = []  # np.zeros(num_points)
#     for slope in np.linspace(0,slope_max,num_points, endpoint=False):
#         # cp_x = i
#         w_0 = 10
#         penetration = p
#         # slope = i*.05
#         cur_max_shear, cur_cp = calc_max_shear_force_planar()
#         max_shear_vec.append(cur_max_shear)
#         cp_vec.append(cur_cp)
#         # max_shear_vec[i], cp_vec[i] = calc_max_shear_force_planar()
#
#     plt.plot(cp_vec, max_shear_vec)

# fig = plt.figure(figsize=(5,5))
# plt.xlim((0,10))
# plt.ylim((15,33))
# plt.show()

def calc_max_shear_force_convex():
    # r_o = w_0*3
    # penetration = 3

    ob_center_x = tip_x
    ob_center_z = cp_z

    # define for plane
    object_height = w_0 + r_o - penetration - np.sqrt(r_o ** 2 - (surf_x - pad_x / 2 - ob_center_x) ** 2 - (surf_z - pad_z / 2 - ob_center_z) ** 2)
    # print("just calced ob height")
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

# fig = plt.figure(figsize=(3,5))
# ax = plt.axes(projection='2d')
# ax.set_box_aspect((1,1))

# # Calculate max sustainable stress for range of cp
# cp_z = 0
# for r in [20*w_0, 15*w_0, 10*w_0, 7*w_0, 6*w_0]:
#     num_points = 50
#     max_shear_vec = np.zeros(num_points)
#     cp_vec = np.zeros(num_points)
#     for i in range(num_points):
#         tip_x = i  #*((r/2)/num_points)
#         w_0 = 10
#         cp_z = 0
#         r_o = r
#         penetration = 5
#         slope = i*.05
#         max_shear_vec[i], cp_vec[i] = calc_max_shear_force_convex()
#
#     plt.plot(cp_vec, max_shear_vec)
#
# plt.xlim([0,10])
# plt.ylim([15,30])
# plt.show()



# Press the green button in the gutter to run the script.

if __name__ == '__main__':

    print("Starting Main Method...\n")

    color = itertools.cycle(('r', 'g', 'b', 'y'))

    #### Setup shear vs normal stress mapping ####
    show3DPlots_planar = False
    show3DPlots_convex = False

    norm_vec_acrylic = [.2333, .4666, 1.1666, 2.333, 4.666]  # n_vs_s_data[:,0]
    shear_vec_acrylic = [5.62, 8, 14.14, 16.86, 22.5]  # n_vs_s_data[:,1]
    std_dev_vec_acrylic = [.57, .43, .95, .43, 1.6]

    norm_vec_paper = [.2333, .4666, 1.1666, 2.333, 4.666]  # n_vs_s_data[:,0]
    shear_vec_paper = [1.1, 1.4, 2.5, 4.4, 7.3]  # n_vs_s_data[:,1]
    std_dev_vec_paper = [.32, .60, .21, .40, .46]

    norm_vec_metal = [.2333, .4666, 1.1666, 2.333, 4.666]  # n_vs_s_data[:,0]
    shear_vec_metal = [5, 7.3, 11.6, 15.4, 18]  # n_vs_s_data[:,1]
    std_dev_vec_metal = [.38, .39, 1.45, .74, 1.40]

    fit_shear_vs_norm(norm_vec_paper, shear_vec_paper, std_dev_vec_paper)
    fit_shear_vs_norm(norm_vec_metal, shear_vec_metal, std_dev_vec_metal)
    fit_shear_vs_norm(norm_vec_acrylic, shear_vec_acrylic, std_dev_vec_acrylic)
    # plt.show()

    #### Setup normal stress vs strain mapping ####
    w_0 = 10
    norm_vec_distInner = [0, 1.5, 2.75, 3.5, 6.5, 13.25]
    norm_vec_distOuter = [0, 1.8, 2.85, 3.57, 5.7, 14.6]
    norm_vec_proxInner = [0, .83, 1.66, 2.66, 4.5, 8.33]
    norm_vec_proxOuter = [0, 1.6, 2.2, 2.4, 3.8, 8.8]
    displace_vec = np.asarray([0, 1, 2, 3, 4, 5])
    label = itertools.cycle(('dist in', 'dist out', 'prox in', 'prox out'))
    fit_norm_vs_strain(norm_vec_distOuter, displace_vec)
    fit_norm_vs_strain(norm_vec_proxInner, displace_vec)
    fit_norm_vs_strain(norm_vec_proxOuter, displace_vec)
    fit_norm_vs_strain(norm_vec_distInner, displace_vec)
    plt.legend()
    # plt.show()

    #### Grid search Tp and Td ####
    lp = 70
    ld = 40

    pad_x = 40
    pad_z = 20
    Tp_range = [.1, .5]
    Tp_vec = np.linspace(Tp_range[0],Tp_range[1],5)
    Td_range = [.01, .1]
    Td_vec = np.linspace(Td_range[0],Td_range[1],20)
    surf_x, surf_z = np.meshgrid(np.linspace(0, pad_x, pad_x), np.linspace(0, pad_z, pad_z))
    pad_height = surf_x * 0 + surf_z * 0 + w_0
    # surf_Td, surf_Tp = np.meshgrid(Td_vec,Tp_vec)
    # pad_height = surf_x * 0 + surf_z * 0
    tp_plotting = []
    td_plotting = []
    fs_plotting = []
    fs_coulomb_plotting = []
    cp_plotting = []

    for Tp in Tp_vec:
        for Td in Td_vec:
            # Calculate fn and cp
            #   Assume pinch joint config (and that movement afterwards is minimal)
            theta_p = 30*np.pi/180
            theta_d = -theta_p

            if (Tp > Td):

                cp = Td*lp*np.cos(theta_p)/((Tp-Td)*np.cos(theta_p-theta_d)) - ld/2
                # print(cp)

                peelOffFlag = False
                if (cp > pad_x/2/2):
                    cp = pad_x/2/2
                    peelOffFlag = True
                elif (cp < -pad_x/2/2):
                    cp = -pad_x/2/2
                    peelOffFlag = True
                fn = Td/(ld/2 + cp)*1000
                # fn = Tp/(np.cos(theta_p)*lp + ld/2 + cp)


                # Map cp and fn to shear force
                if not peelOffFlag:
                    # Calculate max shear force for adhesive condition
                    print("Input Fn: " + str(fn))
                    print("Input Cp: " + str(cp))
                    max_shear_force, output_fn, output_cp = cp_fn_to_fs_planar(cp, fn)
                    print("Output Fn: " + str(output_fn))
                    print("Output Cp: " + str(output_cp))
                    print()
                    tp_plotting.append(Tp)
                    td_plotting.append(Td)
                    fs_plotting.append(max_shear_force)
                    cp_plotting.append(output_cp)

                    # Calculate coulomb friction shear force max
                    mu = 0.6
                    fs_coulomb = fn * mu
                    fs_coulomb_plotting.append(fs_coulomb)

    #### Plotting ####
    fig = plt.figure(figsize=(4,4))
    ax = plt.axes(projection='3d')
    ax.set_box_aspect((1, 1, 1))

    tp_array = np.asarray(tp_plotting)
    td_array = np.asarray(td_plotting)
    fs_array = np.asarray(fs_plotting)
    cp_array = np.asarray(cp_plotting)
    fs_coulomb_array = np.asarray(fs_coulomb_plotting)

    # ax.scatter(np.asarray(tp_plotting), np.asarray(td_plotting), np.asarray(fs_plotting), marker='o')
    # ax.scatter(np.asarray(tp_plotting), np.asarray(td_plotting), np.asarray(cp_plotting), marker='x')
    ax.set_xlabel("Proximal Torque (Nm)")
    ax.set_ylabel("Distal Torque (Nm)")

    Tp_plotting = np.linspace(Tp_range[0], Tp_range[1], 50)
    Td_plotting = np.linspace(Td_range[0], Td_range[1], 50)
    X, Y = np.meshgrid(Tp_plotting,Td_plotting)

    Z = interpolate.griddata((tp_array, td_array), fs_array, (X,Y), method='cubic')
    for i in range(len(Z)):
        for j in range(len(Z[0])):
            if math.isnan(Z[i,j]):
                Z[i,j] = 0
    ax.plot_surface(X,Y,Z, cmap=cm.get_cmap('viridis'), alpha=0.75)
    ax.axes.set_zlim3d(0,25)

    temp_Tp = np.linspace(.1,.5, 10)
    theta_p = 30 * np.pi / 180
    theta_d = -theta_p
    const_1 = np.cos(theta_p - theta_d)*(ld/2) / (lp*np.cos(theta_p) + np.cos(theta_p - theta_d) * ld/2)
    print(const_1)
    temp_Td = temp_Tp * const_1
    Z_2 = interpolate.griddata((tp_array, td_array), fs_array, (temp_Tp, temp_Td), method='linear')
    plt.plot(temp_Tp, temp_Td, Z_2+1, '--', color = 'k', zorder=10)

    fig = plt.figure(figsize=(4, 4))
    ax = plt.axes(projection='3d')
    ax.set_box_aspect((1, 1, 1))

    # ax.scatter(np.asarray(tp_plotting), np.asarray(td_plotting), np.asarray(fs_plotting), marker='o')
    Z = interpolate.griddata((tp_array, td_array), fs_coulomb_array, (X,Y), method='linear')
    for i in range(len(Z)):
        for j in range(len(Z[0])):
            if math.isnan(Z[i,j]):
                Z[i,j] = 0
    ax.plot_surface(X, Y, Z, cmap=cm.get_cmap('inferno'), alpha=0.75)

    # ax.axes.set_xlim3d()
    # ax.axes.set_ylim3d(.01,.1)
    ax.axes.set_zlim3d(0,4)
    plt.show()

    # cp_fn_to_fs_planar(2, 10)

