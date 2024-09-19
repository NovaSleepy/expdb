import numpy as np
import math
import matplotlib.pyplot as plt
from literature import *


def van_der_corput(k, alpha):
    return max(
        alpha + (1 - k * alpha) / (2**k - 2),
        (1 - 2 ** (2 - k)) * alpha - (1 - k * alpha) / (2**k - 2),
    )


def optimized_van_der_corput(alpha):
    bound = 1
    for k in range(2, 30):
        bound = min(bound, van_der_corput(k, alpha))
    return bound


def conjectured_bound(alpha):
    if alpha <= 1:
        return alpha / 2
    else:
        return alpha - 1


def van_der_corput_plot():
    alpha_range = np.linspace(0, 1, 500)
    plt.figure(figsize=(10, 6))

    plt.plot(
        alpha_range,
        [van_der_corput(2, alpha) for alpha in alpha_range],
        label=r"$k=2$ van der Corput",
    )
    plt.plot(
        alpha_range,
        [van_der_corput(3, alpha) for alpha in alpha_range],
        label=r"$k=3$ van der Corput",
    )
    plt.plot(
        alpha_range,
        [van_der_corput(4, alpha) for alpha in alpha_range],
        label=r"$k=4$ van der Corput",
    )
    plt.plot(
        alpha_range,
        [van_der_corput(5, alpha) for alpha in alpha_range],
        label=r"$k=5$ van der Corput",
    )
    plt.plot(
        alpha_range,
        [optimized_van_der_corput(alpha) for alpha in alpha_range],
        label=r"Optimized van der Corput",
    )
    plt.plot(
        alpha_range, [alpha / 2 for alpha in alpha_range], label=r"Conjectured value"
    )
    plt.xlabel(r"$\alpha$")
    plt.ylabel(r"$\beta(\alpha)$")
    plt.title(r"Classical bounds on $\beta(\alpha)$")
    plt.legend()
    plt.grid(True)
    plt.ylim(0, 1)
    plt.show()


def van_der_corput_plot2():
    alpha_range = np.linspace(0, 1, 500)
    alpha_full_range = np.linspace(0, 2, 1000)

    plt.figure(figsize=(10, 6))

    plt.plot(
        alpha_full_range,
        [optimized_van_der_corput(alpha) for alpha in alpha_full_range],
        label=r"Optimized van der Corput",
    )
    plt.plot(
        alpha_range, [alpha for alpha in alpha_range], label=r"Trivial upper bound"
    )
    plt.plot(
        alpha_full_range,
        [conjectured_bound(alpha) for alpha in alpha_full_range],
        label=r"Conjectured value",
    )
    plt.xlabel(r"$\alpha$")
    plt.ylabel(r"$\beta(\alpha)$")
    plt.title(r"Classical bounds on $\beta(\alpha)$")
    plt.legend()
    plt.grid(True)
    plt.ylim(0, 1)
    plt.show()


def beta_bound_plot():
    hypotheses = Hypothesis_Set()  # Start with an empty hypothesis set
    hypotheses.add_hypothesis(trivial_beta_bound_1)
    hypotheses.add_hypotheses(
        literature.list_hypotheses(hypothesis_type="Upper bound on beta")
    )
    best_beta_bounds = compute_best_beta_bounds(hypotheses)

    alpha_range = np.linspace(0, 1 / 2, 500)
    plt.figure(figsize=(10, 6))
    plt.plot(
        alpha_range,
        [
            min(
                b.data.bound.at(alpha)
                for b in best_beta_bounds
                if b.data.bound.domain.contains(alpha)
            )
            for alpha in alpha_range
        ],
        label=r"Computed best upper bound on $\beta$",
    )
    plt.plot(
        alpha_range,
        [optimized_van_der_corput(alpha) for alpha in alpha_range],
        label=r"van der Corput bound on $\beta$",
    )
    plt.xlabel(r"$\alpha$")
    plt.ylabel(r"$\beta(\alpha)$")
    plt.title(r"Best bounds on $\beta(\alpha)$")
    plt.legend()
    plt.grid(True)
    plt.ylim(0, 1 / 2)
    plt.show()

    for b in best_beta_bounds:
        print(b.data)
    print(
        min(
            b.data.bound.at(0)
            for b in best_beta_bounds
            if b.data.bound.domain.contains(0)
        )
    )

# Compare the best literature zero-density estimates against the 
# best-known zero-density estimate
def zero_density_plot():
    # plot zero-density estimate
    N = 500
    sigmas = []
    literature_zd = []
    best_zd = []
    
    hs = Hypothesis_Set()
    hs.add_hypotheses(literature)
    
    # Add the new zero-density estimates (not part of the literature yet!)
    zd.add_zero_density(hs, "2/(9*x - 6)", Interval("[17/22, 38/49]"), Reference.make("Tao--Trudgian--Yang", 2024))
    zd.add_zero_density(hs, "9/(8*(2*x - 1))", Interval("[38/49, 4/5]"), Reference.make("Tao--Trudgian--Yang", 2024))
    zd.add_zero_density(hs, "3/(10 * x - 7)", Interval("[701/1000, 1]"), Reference.make("Tao--Trudgian--Yang", 2024))
    hs.add_hypotheses(zd.bourgain_ep_to_zd())
    # New Pintz-type estimates 
    zd.add_zero_density(hs, "3/(40 * x - 35)", Interval("[39/40, 40/41)"), Reference.make("Tao--Trudgian--Yang", 2024))
    zd.add_zero_density(hs, "2/(13 * x - 10)", Interval("[40/41, 41/42)"), Reference.make("Tao--Trudgian--Yang", 2024))
    
    def best_zd_at(hypotheses, sigma):
        min_ = 1000000
        for h in hypotheses:
            if h.hypothesis_type == "Zero density estimate":
                if h.data.interval.contains(sigma):
                    q = h.data.at(sigma)
                    if q.is_real and math.isfinite(q) and min_ > q:
                        min_ = q
        return min_
    
    print(len(literature), len(hs))
    for i in range(N):
        sigma = 1 / 2 + 1 / 2 * i / N
        sigmas.append(sigma)
        literature_zd.append(best_zd_at(literature, sigma))
        best_zd.append(best_zd_at(hs, sigma))
    
    for i in range(len(sigmas)):
        print(sigmas[i], literature_zd[i], best_zd[i])
        
    plt.figure(figsize=(10, 6))
    plt.xlabel(r"$\sigma$")
    plt.ylabel(r"$A(\sigma)$")
    plt.plot(sigmas, best_zd, linewidth=0.5, label="Best zero-density estimate")
    plt.plot(sigmas, literature_zd, linewidth=0.5, label="Literature zero-density estimate")
    plt.title("Zero density estimates")
    plt.legend(loc="lower left")
    plt.show()

# Plot the best zero-density energy estimates known trivially, in the literature, and under the 
# Lindelof hypothesis
def zero_density_energy_plot():
    hypotheses = Hypothesis_Set()
    hypotheses.add_hypotheses(literature.list_hypotheses(hypothesis_type="Zero density estimate"))
    hypotheses.add_hypotheses(literature.list_hypotheses(hypothesis_type="Zero density energy estimate"))

    # add trivial bounds - this uses literature zero-density estimates
    ze.add_trivial_zero_density_energy_estimates(hypotheses)

    # as an example, plot the trivial bound and the literature bound 
    sigmas = np.linspace(1/2, 0.999, 1000)
    trivial_bound = []
    lit_bound = []
    lindelof_bound = []
    for sigma in sigmas:
        trivial = min(
                    h.data.at(sigma) 
                    for h in hypotheses 
                    if h.name == "Trivial zero density energy estimate" and h.data.interval.contains(sigma)
                )
        trivial_bound.append(trivial)
        
        lit = min(
                h.data.at(sigma)
                for h in literature
                if h.hypothesis_type == "Zero density energy estimate" and h.data.interval.contains(sigma)
            )
        lit_bound.append(min(lit, trivial))
        
        if sigma > 3/4:
            lindelof_bound.append(0)
        else:
            lindelof_bound.append(8 - 4 * sigma)
    
    plt.figure(figsize=(10, 6))
    plt.xlabel(r"$\sigma$")
    plt.ylabel(r"$A^*(\sigma)$")
    plt.plot(sigmas, lit_bound, linewidth=1, label="Literature zero-density energy estimate")
    plt.plot(sigmas, trivial_bound, linewidth=1, label="\"Trivial\" zero-density energy estimate")
    plt.plot(sigmas, lindelof_bound, linewidth=1, label="Lindelof zero-density energy estimate")
    plt.title("Zero density energy estimates")
    plt.legend()
    plt.grid(True)
    plt.show()


# van_der_corput_plot2()
# beta_bound_plot()
#zero_density_plot()
zero_density_energy_plot()

