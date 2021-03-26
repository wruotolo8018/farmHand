from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
import math
from matplotlib import cm
from scipy.optimize import curve_fit
from scipy import interpolate
from scipy.signal import bspline



#### FIT SHEAR VS NORM RELATIONSHIP ####
def fit_shear_vs_norm(norm_vec, shear_vec):

    global fit_func
    def fit_func(x, a, b):
        return a * np.power(x, b) + shear_vec[0]
        # return a*np.sqrt(x) + c

    # plt.scatter(norm_vec, shear_vec)
    # plt.xlim([0,40])
    # plt.ylim([0,70])
    pars, cov = curve_fit(f=fit_func, xdata=norm_vec, ydata=shear_vec,
                          p0=[0,0], bounds=(-np.inf,np.inf), maxfev=1000)

    print("Curve fit param results: " + str(pars))

    global calc_shear_from_norm
    def calc_shear_from_norm(norm_stress):
        return fit_func(norm_stress, pars[0], pars[1])

    x_curve_fit = np.linspace(0,100,1000)
    # plt.plot(x_curve_fit, calc_shear_from_norm(x_curve_fit))
    # plt.show()
    #### FIT SHEAR VS NORM RELATIONSHIP ####

#### FIT NORM VS STRAIN RELATIONSHIP ####
def fit_norm_vs_strain(norm_vec, displace_vec):

    # plt.scatter(displace_vec, norm_vec)
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

    # plt.plot(x_curve_fit, calc_norm_from_displace(x_curve_fit))

def calc_max_shear_force_convex(lf, l_eff, penetration, show_plot):
    r_o = r
    ob_center_x = np.abs(lf/2-l_eff)
    ob_center_z = 0
    w_0 = 10
    pad_z = 20
    surf_x, surf_z = np.meshgrid(np.linspace(0, lf, lf), np.linspace(0, pad_z, pad_z))
    pad_height = surf_x * 0 + surf_z * 0
    object_height = w_0 + r_o - penetration - np.sqrt(r_o ** 2 - (surf_x - lf / 2 - ob_center_x) ** 2 - (surf_z - pad_z / 2 - ob_center_z) ** 2)

    penetration_array = np.zeros((pad_z, lf))
    norm_stress_array = np.zeros((pad_z, lf))
    shear_stress_array = np.zeros((pad_z, lf))
    norm_stress_x_moment = np.zeros((pad_z, lf))

    for i in range(pad_z):
        for j in range(lf):
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

    if (show_plot):
        fig = plt.figure()
        ax = plt.axes(projection='3d')
        ax.set_box_aspect((2, 1, .5))

        print("Plotting for lf = " + str(lf) + " and l_eff = " + str(l_eff))
        ax.plot_surface(surf_x, surf_z, pad_height, alpha=0.75)
        ax.plot_surface(surf_x, surf_z, object_height, alpha=0.75)
        ax.plot_surface(surf_x, surf_z, shear_stress_array, alpha=0.75)

        plt.show()

    shear_force = np.sum(shear_stress_array)/1000
    normal_force = np.sum(norm_stress_array)/1000
    c_p = .5-(lf / 2 - np.sum(norm_stress_x_moment) / np.sum(norm_stress_array))

    # print("stress_integral: " + str(stress_integral))
    # print("c_p mag: " + str(c_p))

    return shear_force, normal_force

def get_contact_geometry(r, h, plotting_visible, theta_inc):

    def parametrize_fing_and_circle(r, h, phw, theta_p, theta_d, show_plot):
        # r = 150
        h = r + h
        f = np.linspace(0,ld+lp, ld+lp)
        theta_p = theta_p * np.pi / 180
        theta_d = -theta_d * np.pi / 180

        xc = np.linspace(0,r,r)
        yc = -np.sqrt(r**2 - xc**2) + h
        xf = np.zeros(len(f))
        yf = np.zeros(len(f))

        for l in range(len(f)):
            if (l < lp):
                xf[l] = phw + l*np.sin(theta_p)
                yf[l] = l*np.cos(theta_p)
            else:
                xf[l] = phw + lp*np.sin(theta_p) + (l-lp)*np.sin(theta_p+theta_d)
                yf[l] = lp*np.cos(theta_p) + (l-lp)*np.cos(theta_p + theta_d)

        if (show_plot):
            fig = plt.figure(figsize=(5, 5))
            plt.xlim((0,h))
            plt.ylim((0,h))

            plt.plot(xc, yc)
            plt.plot(xf, yf)
            plt.show()

        return xc, yc, xf, yf

    prox_intersect = False
    dist_intersect = False
    cur_theta_p = 90
    cur_theta_d = 0
    theta_increment = theta_inc

    def interpolate_double(xc, yc, xf, yf):
        ff = interpolate.interp1d(xf, yf, kind='linear')
        max_val = np.min([xf[-1], xc[-1]])
        x_master = np.linspace(phw, max_val, 100)
        yf_interp = ff(x_master)

        fc = interpolate.interp1d(xc, yc, kind='cubic')
        yc_interp = fc(x_master)

        return yf_interp, yc_interp, x_master

    def check_prox_intersect(yf_interp, yc_interp, x_master):
        for i in range(len(yf_interp)):
            if (yf_interp[i] > yc_interp[i]):
                # plt.scatter(x_master[i],0)
                lp_eff = (x_master[i]-phw)/np.sin(np.deg2rad(cur_theta_p))
                print(lp_eff)
                return True, lp_eff
        return False, 0

    def check_dist_intersect(yf_interp, yc_interp, x_master):
        contact_flag = 0
        for i in range(len(yf_interp)):

            if (contact_flag == 0):
                if (yf_interp[i] > yc_interp[i]):
                    # print("Contact flag 1")
                    contact_flag = 1

            if (contact_flag == 1):
                if (yf_interp[i] <= yc_interp[i]):
                    # print("Contact flag 2")
                    contact_flag = 2

            if (contact_flag == 2):
                if (yf_interp[i] > yc_interp[i]):
                    # print("Return True")
                    # plt.scatter(x_master[i], 0)
                    ld_eff = (x_master[i] - phw - lp*np.sin(np.deg2rad(cur_theta_p))) / np.sin(np.deg2rad(cur_theta_p-cur_theta_d))
                    return True, ld_eff

        return False, 0

    while (prox_intersect == False):
        cur_theta_p -= theta_increment
        xc, yc, xf, yf = parametrize_fing_and_circle(r, h, phw, cur_theta_p, cur_theta_d, False)
        yf_interp, yc_interp, x_master = interpolate_double(xc, yc, xf, yf)
        prox_intersect, lp_eff = check_prox_intersect(yf_interp, yc_interp, x_master)
    # print("Theta P for intercept: " + str(cur_theta_p))

    while (dist_intersect == False):
        cur_theta_d += theta_increment
        xc, yc, xf, yf = parametrize_fing_and_circle(r, h, phw, cur_theta_p, cur_theta_d, False)
        yf_interp, yc_interp, x_master = interpolate_double(xc, yc, xf, yf)
        dist_intersect, ld_eff = check_dist_intersect(yf_interp, yc_interp, x_master)
    # print("Theta D for intercept: " + str(cur_theta_d))

    print("Angle of distal phalange: " + str(cur_theta_p - cur_theta_d))

    if (plotting_visible):
        plt.plot(xc, yc)
        plt.plot(xf, yf)

    return cur_theta_p, cur_theta_d, lp_eff, ld_eff

def calc_coulomb_pullout(fnp, fnd, theta_p, theta_d):

    theta_p_rad = np.deg2rad(theta_p)
    theta_d_rad = np.deg2rad(theta_d)
    fsp_max = fnp * mu
    fsd_max = fnd * mu
    fsp_component = fsp_max * np.cos(theta_p_rad)
    fsd_component = fsd_max * np.cos(theta_p_rad - theta_d_rad)
    fnp_component = fnp * np.sin(theta_p_rad)
    fnd_component = fnd * np.sin(theta_p_rad - theta_d_rad)
    f_pullout = fsp_component + fsd_component - fnd_component - fnp_component
    return f_pullout

def calc_adhesive_pullout(fnp, fnd, theta_p, theta_d, lp_eff, ld_eff):
    theta_p_rad = np.deg2rad(theta_p)
    theta_d_rad = np.deg2rad(theta_d)
    # print("fnp input: " + str(fnp))
    # print("fnd input: " + str(fnd))

    # Get fsp_max
    cur_fnp = 0
    pen_inc = .1
    cur_pen = 0
    fsp_max = 0
    while cur_fnp < fnp:
        cur_pen += pen_inc
        fsp_max, cur_fnp = calc_max_shear_force_convex(lp, lp_eff, cur_pen, False)
    calc_max_shear_force_convex(lp, lp_eff, cur_pen, False)
    # print("fnp output: " + str(cur_fnp))

    # Get fsd_max
    cur_fnd = 0
    pen_inc = .1
    cur_pen = 0
    fsd_max = 0
    while cur_fnd < fnd:
        cur_pen += pen_inc
        fsd_max, cur_fnd = calc_max_shear_force_convex(ld, ld_eff, cur_pen, False)
    calc_max_shear_force_convex(ld, ld_eff, cur_pen, False)
    # print("fnd output: " + str(cur_fnd))

    fsp_component = fsp_max * np.cos(theta_p_rad)
    fsd_component = fsd_max * np.cos(theta_p_rad - theta_d_rad)
    fnp_component = fnp * np.sin(theta_p_rad)
    fnd_component = fnd * np.sin(theta_p_rad - theta_d_rad)
    f_pullout = fsp_component + fsd_component - fnd_component - fnp_component
    return f_pullout


if __name__ == '__main__':

    print("Starting Main Method...\n")

    #### Setup shear vs normal stress mapping ####
    show3DPlots_planar = False
    show3DPlots_convex = False

    norm_vec_acrylic = [0, 10, 20, 30]  # n_vs_s_data[:,0]
    shear_vec_acrylic = [20, 35, 45, 50]  # n_vs_s_data[:,1]

    norm_vec_wood = [0, 5, 10, 20, 30]  # n_vs_s_data[:,0]
    shear_vec_wood = [10, 13, 15, 16, 16]  # n_vs_s_data[:,1]

    norm_vec_metal = [0, 10, 20, 30]  # n_vs_s_data[:,0]
    shear_vec_metal = [12, 18, 23, 25]  # n_vs_s_data[:,1]

    fit_shear_vs_norm(norm_vec_wood, shear_vec_wood)
    fit_shear_vs_norm(norm_vec_metal, shear_vec_metal)
    fit_shear_vs_norm(norm_vec_acrylic, shear_vec_acrylic)
    # plt.show()
    # fig = plt.figure(figsize=(3, 3))


    #### Setup normal stress vs strain mapping ####
    w_0 = 10
    norm_vec_distInner = [0, 7, 11, 13, 16, 17]
    norm_vec_distOuter = [0, 5, 12, 13, 14.5, 15]
    norm_vec_proxInner = [0, 6.5, 10.5, 13.5, 14, 17]
    norm_vec_proxOuter = [0, 6, 10, 14, 15, 16]
    displace_vec = np.asarray([0, 2, 4, 6, 8, 10])
    fit_norm_vs_strain(norm_vec_distInner, displace_vec)
    fit_norm_vs_strain(norm_vec_distOuter, displace_vec)
    fit_norm_vs_strain(norm_vec_proxInner, displace_vec)
    fit_norm_vs_strain(norm_vec_proxOuter, displace_vec)
    # plt.show()

    #### Variable Setup ####
    lp = 70
    ld = 40
    # pad_x = 40
    # pad_z = 20

    #### TESTING ####
    # cur_theta_p, cur_theta_d, lp_eff, ld_eff = get_contact_geometry(110,6,True, 0.1) # input: r, h, show_plot, theta_increment
    # print("Lp_eff: " + str(c))
    # print("Ld_eff: " + str(d))

    num_values = 10
    coulomb_pullout_vec = []
    adhesive_pullout_vec = []
    r = 100
    mu = 0.6
    h_vec = np.linspace(0,12,20)
    phw = 32

    for h in h_vec:
        tp, td, lp_eff, ld_eff = get_contact_geometry(r, h, False, 0.2)  # input: r, h, show_plot, theta_increment
        coulomb_pullout_vec.append(calc_coulomb_pullout(2,5,tp,td))
        adhesive_pullout_vec.append(calc_adhesive_pullout(2,5,tp,td,lp_eff,ld_eff))

    fig = plt.figure(figsize=(5,5))
    plt.plot(h_vec, np.asarray(coulomb_pullout_vec))
    plt.plot(h_vec, np.asarray(adhesive_pullout_vec))
    plt.show()
