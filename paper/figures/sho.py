#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function

import numpy as np
import matplotlib.pyplot as plt
from plot_setup import setup, HORIZONTAL_FIGSIZE

setup()

def sho_psd(Q, x):
    x2 = x*x
    return 1.0 / ((x2 - 1)**2 + x2 / Q**2)

def sho_acf(Q, tau):
    t = np.abs(tau)
    if np.allclose(Q, 0.5):
        return np.exp(-t) * (1.0 + t)
    b = 1.0 / np.sqrt(4*Q**2 - 1)
    c = 0.5 / Q
    d = 0.5 * np.sqrt(4*Q**2 - 1) / Q
    return np.exp(-c * t) * (np.cos(d*t)+b*np.sin(d*t))

def lorentz_psd(Q, x):
    return Q**2 * (1.0 / ((x - 1)**2 * (2*Q)**2 + 1) +
                   1.0 / ((x + 1)**2 * (2*Q)**2 + 1))

def lorentz_acf(Q, tau):
    t = np.abs(tau)
    return np.exp(-0.5*t/Q) * np.cos(t)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=HORIZONTAL_FIGSIZE)
x = 10**np.linspace(-1.1, 1.1, 5000)
tau = np.linspace(0, 20, 5000)

for Q_name, Q in [("1/2", 0.5), ("1/\\sqrt{2}", 1./np.sqrt(2)),
                  ("2", 2.0), ("10", 10.0)]:
    ax1.plot(x, sho_psd(Q, x), label="$Q = {0}$".format(Q_name), lw=1.5)
    ax2.plot(tau, sho_acf(Q, tau), label="$Q = {0}$".format(Q_name), lw=1.5)

ax1.plot(x, lorentz_psd(10.0, x), "--k")
ax2.plot(tau, lorentz_acf(10.0, tau), "--k")

ax1.set_xscale("log")
ax1.set_yscale("log")
ax1.set_xlim(x.min(), x.max())
ax1.set_ylim(2e-4, 200.0)
ax1.legend(loc=3, fontsize=11)
ax1.set_xlabel("$\omega/\omega_0$")
ax1.set_ylabel("$S(\omega) / S(0)$")

ax2.set_xlim(tau.min(), tau.max())
ax2.set_ylim(-1.1, 1.1)
ax2.set_xlabel("$\omega_0\,\\tau$")
ax2.set_ylabel("$k(\\tau) / k(0)$")

fig.savefig("sho.pdf", bbox_inches="tight")