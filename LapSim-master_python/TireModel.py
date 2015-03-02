from math import sin, cos, atan, exp, pi, fabs
from TrigHelpers import sign
from Plotter import plot_many_y_funcs
from functools import partial
import numpy as np


def getF_x(F_z, kappa, alpha, gamma, p_i):
    # normalization of parameters
    F_z0 = 200  # nominal vertical force in lbf
    p_i0 = 10  # nominal tire inflation pressure in psi

    df_z = (F_z - F_z0) / F_z0  # normalized vertical force change
    dp_i = (p_i - p_i0) / p_i0  # normalized inflation pressure change

    # unit conversions
    F_z = 4.44822162 * F_z  # convert from lbf to N
    F_z0 = 4.44822162 * F_z0  # convert from lbf to N
    kappa = kappa * pi / 180  # convert from degrees to radians
    alpha = alpha * pi / 180  # convert from degrees to radians
    gamma = gamma * pi / 180  # convert from degrees to radians
    p_i = 6894.75729 * p_i  # convert from psi to Pa
    df_z = 4.44822162 * df_z  # convert from lbf to N
    dp_i = 6894.75729 * dp_i  # convert from psi to Pa

    # scaling coefficients
    lambda_cx = 1  # shape factor
    lambda_mux = 1  # peak friction coefficient
    lambda_ex = 1  # curvature factor
    lambda_kxkappa = 1  # slip stiffness
    lambda_hx = 1  # horizontal shift
    lambda_vx = 1  # vertical shift
    lambda_xalpha = 1  # alpha influence

    # longitudinal coefficients
    p_cx1 = 1.372
    p_dx1 = 2.3904
    p_dx2 = -0.5
    p_dx3 = 0
    p_ex1 = 0.14053
    p_ex2 = 0.6172
    p_ex3 = 0
    p_ex4 = -0.9
    p_kx1 = 51.24
    p_kx2 = -15
    p_kx3 = -0.19595
    p_hx1 = 0.0020286
    p_hx2 = 0.0016866
    p_vx1 = -0.1
    p_vx2 = -0.05516

    r_bx1 = 11.98
    r_bx2 = 14.51
    r_bx3 = 0
    r_cx1 = 1.0154
    r_ex1 = -0.4098
    r_ex2 = 1.0438
    r_hx1 = -0.01837

    p_px1 = -0.25437
    p_px2 = -0.5734
    p_px3 = -0.17727
    p_px4 = -0.26627

    # MF-Tyre/Swift 6.2 Longitudinal force Fx
    S_vx = F_z * (p_vx1 + p_vx2 * df_z) * lambda_vx * lambda_mux  # no turnslip
    S_hx = (p_hx1 + p_hx2 * df_z) * lambda_hx
    K_xkappa = (F_z * (p_kx1 + p_kx2 * df_z) * exp(p_kx3 * df_z) *
                (1 + p_px1 * dp_i + p_px2 * dp_i ** 2) * lambda_kxkappa)
    E_x = ((p_ex1 + p_ex2 * df_z + p_ex3 * df_z ** 2) *
           (1 - p_ex4 * sign(kappa_x)) * lambda_ex)
    if E_x > 1:
        E_x = 1
    mu_x = ((p_dx1 + p_dx2 * df_z) * (1 + p_px3 * dp_i ** 2) *
            (1 - p_dx3 * gamma ** 2) * lambda_mux)
    D_x = mu_x * F_z  # no turn slip
    C_x = p_cx1 * lambda_cx
    B_x = K_xkappa / (C_x * D_x)
    kappa_x = kappa + S_hx

    E_xalpha = r_ex1 + r_ex2 * df_z
    B_xalpha = ((r_bx1 + r_bx3 * gamma ** 2) *
                cos(atan(r_bx2*kappa)) * lambda_xalpha)
    C_xalpha = r_cx1
    S_hxalpha = r_hx1
    alpha_s = alpha + S_hxalpha
    G_xalpha = (cos(C_xalpha * atan(B_xalpha * alpha_s -
                E_xalpha * (B_xalpha * alpha_s - atan(B_xalpha * alpha_s)))) /
                cos(C_xalpha * atan(B_xalpha * S_hxalpha - E_xalpha *
                    (B_xalpha * S_hxalpha - atan(B_xalpha * S_hxalpha)))))
    F_x = ((D_x * sin(C_x * atan(B_x * kappa_x - E_x *
            (B_x * kappa_x - atan(B_x * kappa_x)))) + S_vx) * G_xalpha)

    F_x = 0.224808943 * F_x  # N to lbf

    return F_x


def getF_y(F_z, kappa, alpha, gamma, p_i):
    # normalization of parameters
    F_z0 = 200  # nominal vertical force in lbf
    p_i0 = 10  # nominal tire inflation pressure in psi

    df_z = (F_z - F_z0) / F_z0  # normalized vertical force change
    dp_i = (p_i - p_i0) / p_i0  # normalized inflation pressure change

    # unit conversions
    F_z = 4.44822162 * F_z  # convert from lbf to N
    F_z0 = 4.44822162 * F_z0  # convert from lbf to N
    kappa = kappa * pi / 180  # convert from degrees to radians
    alpha = alpha * pi / 180  # convert from degrees to radians
    gamma = gamma * pi / 180  # convert from degrees to radians
    p_i = 6894.75729 * p_i  # convert from psi to Pa
    df_z = 4.44822162 * df_z  # convert from lbf to N
    dp_i = 6894.75729 * dp_i  # convert from psi to Pa

    # scaling coefficients
    lambda_cy = 1  # shape factor
    lambda_muy = 1  # seak friction coefficient
    lambda_ey = 1  # curvature factor
    lambda_kyalpha = 1  # cornering stiffness
    lambda_kygamma = 1  # camber stiffness
    lambda_kzgamma = 1  # camber moment stiffness
    lambda_hy = 1  # horizontal shift
    lambda_vy = 1  # vertical shift
    lambda_ykappa = 1  # kappa influence
    lambda_vykappa = 1  # kappa induced 'plysteer'
    lambda_kygamma = 1  # camber stiffness
    lambda_cgamma = 1  # camber shape
    lambda_egamma = 1  # camber curvature

    # lateral coefficients
    p_cy1 = 1.0997
    p_dy1 = 2.5
    p_dy2 = -0.3024
    p_dy3 = 0
    p_ey1 = -0.0719
    p_ey2 = 0.2008
    p_ey3 = -2.637
    p_ey4 = 4.467
    p_ey5 = 0
    p_ky1 = -34.284
    p_ky2 = 1.0752
    p_ky3 = 1
    p_ky4 = 2
    p_ky5 = 0
    p_ky6 = 0.5
    p_ky7 = 2.5
    p_hy1 = -0.009507
    p_hy2 = -0.003813
    p_vy1 = -0.05477
    p_vy2 = -0.1
    p_vy3 = 1
    p_vy4 = 1.5

    r_by1 = 17.94
    r_by2 = 13.82
    r_by3 = -0.01677
    r_by4 = 0
    r_cy1 = 1.018
    r_ey1 = 0.4921
    r_ey2 = -0.12683
    r_hy1 = 0.006166
    r_hy2 = -0.001296
    r_vy1 = -0.07817
    r_vy2 = -0.1404
    r_vy3 = -0.14438
    r_vy4 = 15
    r_vy5 = 2.2
    r_vy6 = 8.11

    p_py1 = 0.4577
    p_py2 = 1.9085
    p_py3 = -0.04457
    p_py4 = -0.13383
    p_py5 = 0

    # equations
    S_vy = S_vy0 + S_vygamma
    S_vygamma = (F_z * (p_vy3 + p_vy4 * df_z) * gamma
                 * lambda_kygamma * lambda_muy)
    S_vy0 = F_z(p_vy1 + p_vy2 * df_z) * lambda_vy * lambda_muy
    S_hy = S_hy0 + S_hygamma
    S_hygamma = (K_ygamma0 * gamma - Svygamma) / K_yalpha
    S_hy0 = (p_hy1 + p_hy2 * df_z) * lambda_hy
    B_y = K_yalpha / C_y / D_y
    K_ygamma0 = ((p_ky6 + p_ky7 * df_z) * F_z *
                 lambda_kygamma * (1 + p_py5 * dp_i))
    K_yalpha0 = (p_ky1 * F_z0 * (1 + p_py1 * dp_i) *
                 sin(p_ky4 * atan(F_z / (p_ky2 * F_z0 * (1 + p_py2 * dp_i))))
                 * lambda_kyalpha)
    K_yalpha = (p_ky1 * F_z0 * (1 + p_py1 * dp_i) * sin(p_ky4 * atan(F_z /
                ((p_ky2 _ p_ky5 * gamma ** 2) * F_z0 * (1 + p_py2 * dp_i)))) *
                (1 - p_ky3 * fabs(gamma)) * lambda_kyalpha)
    E_y = ((p_ey1 + p_ey2 * df_z) *
           (1 + p_ey5 * gamma ** 2 - (p_ey3 + p_ey4 * gamma) * sign(alpha_y))
           * lambda_ey)
    if E_y > 1:
        E_y = 1
    mu_y = ((p_dy1 + p_dy2 * df_z) * (1 + p_py3 * dp_i + p_py4 * dp_i ** 2)
            * (1 - p_dy3 * gamma ** 2) * lambda_muy)
    D_y = mu_y * F_z  # no turnslip
    C_y = p_cy1 * lambda_cy
    alpha_y = alpha + S_hy
    F_yp = (D_y *
            sin(C_y *
                atan(B_y * alpha_y -
                     E_y * (B_y * alpha_y - atan(B_y * alpha_y)))) + S_vy)

    D_vykappa = (mu_y * F_z *
                 (r_vy1 + r_vy2 * df_z + r_vy3 * gamma)
                 * cos(atan(r_vy4 * alpha)))
    S_vykappa = D_vykappa * sin(r_vy5 * atan(r_vy6 * kappa)) * lambda_vykappa

    S_hykappa = r_hy1 + r_hy2 * df_z
    E_ykappa = r_ey1 + r_ey2 * df_z
    C_ykappa = r_cy1
    B_ykappa = ((r_by1 + r_by4 * gamma ** 2) *
                cos(atan(r_by2 * (alpha - r_by3))) * lambda_ykappa)
    kappa_s = kappa + S_hykappa
    G_ykappa = (cos(C_ykappa * atan(B_ykappa * kappa_s -
                                    E_ykappa *
                                    (B_ykappa * kappa_s
                                     - atan(B_ykappa * kappa_s))))
                / cos(C_ykappa * atan(B_ykappa * S_hykappa
                                      - E_ykappa * (B_ykappa * S_hykappa
                                                    - atan(B_ykappa *
                                                           S_hykappa)))))

    F_y = G_ykappa * F_yp + S_Vykappa

    F_y = 0.224808943 * F_y  # N to lbf

    return F_y
