"""Likelihood functions"""

import numpy as np
from .pdf import (lngauss, lngauss_discrete)


def lnlike_continuous(sigma_jeans, sigma, dsigma):
    """Gaussian likelihood for a continuous tracer (e.g., unresolved field
    stars for which we have velocity dispersion measurements.

    Parameters
    ----------
    sigma_jeans : float or array_like
        Jeans model prediction.
    sigma : float or array_like
        Measured velocity dispersion.
    dsigma : float or array_like
        Measurement uncertainty in `sigma`.

    Returns
    -------
    float
        Log likelihood in range (-inf, 0)
    """
    return np.sum(lngauss(sigma, sigma_jeans, dsigma))


def lnlike_density(I_model, I, dI):
    """Gaussian likelihood for surface density data.

    Parameters
    ----------
    I_model : float or array_like
        Model prediction.
    I : float or array_like
        Measured surface density
    dI : float or array_like
        Measurement uncertainty in `I`.

    Returns
    -------
    float
        Log likelihood in range (-inf, 0)
    """
    return np.sum(lngauss(I, I_model, dI))


def lnlike_discrete(sigma_jeans, v, dv):
    """Gaussian likelihood of discrete tracers (e.g., globular cluster or
    planetary nebula line-of-sight velocities).

    Parameters
    ----------
    sigma_jeans : float or array_like
        Jeans model prediction.
    v : float or array_like
        Measured velocity.
    dv : float or array_like
        Measurement uncertainty in `v`.

    Returns
    -------
    float
        Log likelihood in range (-inf, 0)
    """
    return np.sum(lngauss_discrete(v, dv, sigma_jeans))


def lnlike_gmm(sigma_jeans_b, sigma_jeans_r, v, dv, c, dc, mu_color_b,
               mu_color_r, sigma_color_b, sigma_color_r, phi_b, **kwargs):
    """Gaussian mixture model likelihood

    Parameters
    ----------
    sigma_jeans_b : float or array_like
        velocity dispersion prediction for blues
    sigma_jeans_r : float or array_like
        velocity dispersion prediction for reds
    v : float or array_like
        velocity
    dv : float or array_like
        uncertainty in velocity
    c : float or array_like
        color
    dc : float or array_like
        uncertainty in color
    mu_color_b : float
        mean color for blues
    mu_color_r : float
        mean color for reds
    sigma_color_b : float
        std of color for blues
    sigma_color_r : float
        std of color for reds
    phi_b : float
        weight of blues (phi_r = 1 - phi_b)
    
    Returns
    -------
    float
        Log likelihood in range (-inf, 0)
    """
    ll_b_v = lngauss_discrete(v, dv, sigma_jeans_b)
    ll_b_c = lngauss(c, mu_color_b, np.sqrt(sigma_color_b**2 + dc**2))
    ll_b = np.log(phi_b) + ll_b_v + ll_b_c

    phi_r = 1 - phi_b
    ll_r_v = lngauss_discrete(v, dv, sigma_jeans_r)
    ll_r_c = lngauss(c, mu_color_r, np.sqrt(sigma_color_r**2 + dc**2))
    ll_r = np.log(phi_r) + ll_r_v + ll_r_c

    return np.sum(np.logaddexp(ll_b, ll_r))
