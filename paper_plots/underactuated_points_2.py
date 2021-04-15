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

        # plt.show()

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

    # print("Angle of distal phalange: " + str(cur_theta_p - cur_theta_d))

    if (plotting_visible):
        plt.plot(xc, yc)
        plt.plot(xf, yf)
        plt.show()

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

    color = itertools.cycle(('r', 'g', 'b', 'y'))

    #### Setup shear vs normal stress mapping ####
    show3DPlots_planar = False
    show3DPlots_convex = False

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


    #### Variable Setup ####
    lp = 70
    ld = 40
    # pad_x = 40
    # pad_z = 20

    #### TESTING ####
    # cur_theta_p, cur_theta_d, lp_eff, ld_eff = get_contact_geometry(110,6,True, 0.1) # input: r, h, show_plot, theta_increment
    # print("Lp_eff: " + str(c))
    # print("Ld_eff: " + str(d))

    coulomb_pullout_vec = []
    adhesive_pullout_vec = []
    mu = 0.6
    # h_vec = [4,6,8,10,12]
    # r_vec = [90,100,110,120]
    h_range = [0,12]
    h_vec = np.linspace(h_range[0], h_range[1],3)
    r_range = [90,120]
    r_vec = np.linspace(r_range[0], r_range[1],3)

    phw = 32

    fig = plt.figure(figsize=(4, 4))
    ax = plt.axes(projection='3d')
    ax.set_box_aspect((1, 1, 1))

    fnp = 1
    fnd_vec = [1,3,5]
    coulomb_plotted = False

    for fnd in fnd_vec:
        coulomb_pullout_vec = []
        adhesive_pullout_vec = []
        r_plotting = []
        h_plotting = []
        print()
        print("fnd = " + str(fnd))

        for r in r_vec:
            print("r = " + str(r))
            r = int(r)

            for h in h_vec:
                tp, td, lp_eff, ld_eff = get_contact_geometry(r, h, False, .2)  # input: r, h, show_plot, theta_increment
                coulomb_pullout_vec.append(calc_coulomb_pullout(fnp,fnd,tp,td))
                adhesive_pullout_vec.append(calc_adhesive_pullout(fnp,fnd,tp,td,lp_eff,ld_eff))

                r_plotting.append(r)
                h_plotting.append(h)

                print("h = " + str(h))

        h_array = np.asarray(h_plotting)
        r_array = np.asarray(r_plotting)
        a_array = np.asarray(adhesive_pullout_vec)
        c_array = np.asarray(coulomb_pullout_vec)

        X, Y = np.meshgrid(h_array, r_array)
        for i in range(len(a_array)):
            if math.isnan((a_array[i])):
                a_array[i] = 0

        print(len(h_array))
        print(len(r_array))
        print(len(a_array))

        plotting_h = np.linspace(h_range[0], h_range[1], 25)
        plotting_r = np.linspace(r_range[0], r_range[1], 25)
        X, Y = np.meshgrid(plotting_h, plotting_r)

        Z = interpolate.griddata((h_array, r_array), a_array, (X, Y), method='cubic')
        ax.plot_surface(X, Y, Z, cmap=cm.get_cmap('viridis'), alpha=0.75)
        if fnd > 3:
            if not coulomb_plotted:
                Z = interpolate.griddata((h_array, r_array), c_array, (X, Y), method='cubic')
                for i in range(len(Z)):
                    for j in range(len(Z[0])):
                        if Z[i,j] < 0:
                            Z[i,j] = 0
                ax.plot_surface(X, Y, Z, cmap=cm.get_cmap('inferno'), alpha=0.75)
                coulomb_plotted = True

    # Z = X*Y*0
    # ax.plot_surface(X,Y,Z, alpha = 0.75)

    plt.show()
