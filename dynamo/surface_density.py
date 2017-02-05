"""Density profiles
All functions with distances use "R" to refer to a projected length on the sky,
and "r" to refer to the de-projected distance from the galaxy center.  
All lengths are physical (i.e., they are actual distances, not angle subtended on the sky)
"""

import numpy as np
from scipy import special
from scipy.integrate import quad

def b_cb(n):
    """'b' parameter in the Sersic function, from the Ciotti & Bertin (1999) 
    approximation.
    """
    return - 1. / 3 + 2. * n + 4 / (405. * n) + 46 / (25515. * n**2)

def I_nuker(R, Ib, Rb, alpha, beta, gamma):
    """Double power law density profile.
    R is projected radius.
    Ib is intensity at the break radius.
    Rb is the break radius.
    alpha is the transition strength (gradual -> sharp)
    beta is the outer power law index.
    gamma is the inner power law index.
    """
    I = Ib * 2**((beta - gamma) / alpha) * (R / Rb)**(-gamma) * (1 + (R / Rb)**alpha)**((gamma - beta) / alpha)
    return I


def I_sersic(R, I0, Re, n):
    """Sersic surface brightness profile.
    R is the projected radius at which to evaluate the function.
    I0 is the central brightness.
    Re is the effective radius (at which half the luminosity is enclosed).
    n is the Sersic index.
    """
    I = I0 * np.exp(-b_cb(n) * (R / Re)**(1. / n))
    return I


def mu_sersic(R, mu_eff, Re, n):
    return mu_eff + 2.5 * b_cb(n) / np.log(10) * ((R / Re)**(1 / n) - 1)


def mu_eff_sersic(mtot, Re, n):
    b = b_cb(n)
    return mtot + 5 * np.log(Re) + 2.5 * np.log(2 * np.pi * n * np.exp(b) * special.gamma(2 * n) / b**(2 * n))


def mu0_sersic(mtot, Re, n):
    mu_eff = mu_eff_sersic(mtot, Re, n)
    return mu_eff - 2.5 * b_cb(n) / np.log(10)
