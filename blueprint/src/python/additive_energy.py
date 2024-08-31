# code implementation for large value additive energy region theorems

import copy 
from constants import Constants
import exponent_pair as ep
from fractions import Fraction as frac
from functions import *
from hypotheses import Hypothesis
from polytope import Polytope
from reference import Reference
from region import Region, Region_Type
from transform import Transform

class Large_Value_Energy_Region:
    
    # Construct a valid large value energy region represented as a union of 
    # 5-dimensional polytopes 
    # Parameters: region (Region) an object of type Region which represents the 
    # large value energy region
    def __init__(self, region):
        # Should this be a set instead of a list?
        if not isinstance(region, Region):
            raise ValueError("Parameter region must be of type Region.")
        self.region = region
    
    
    def __repr__(self):
        return str(self.region)
        
    def __copy__(self):
        return Large_Value_Energy_Region(copy.copy(self.region))
    
    # Static methods ---------------------------------------------------------

    # The default bounds on the tuple (sigma, tau, rho, rho*, s). This is to ensure
    # that all large value regions are finite regions. 
    def default_limits():
        return [
            (frac(1,2), frac(1)),
            (0, Constants.TAU_UPPER_LIMIT),
            (0, Constants.LV_DEFAULT_UPPER_BOUND),
            (0, Constants.LV_DEFAULT_UPPER_BOUND),
            (0, Constants.LV_DEFAULT_UPPER_BOUND)]

    # Computes the union of n large value energy regions
    def union(*regions):
        return Large_Value_Energy_Region(Region.union([r.region for r in regions]))
        
    # ------------------------------------------------------------------------
    
    # Returns whether the region contains a 5-dimensional point 
    def contains(self, point):
        if len(point) != 5: 
            raise ValueError("point must be 5-dimensional")
        return self.region.contains(point)
    
    # Raise this region to the kth power
    # (sigma, tau, rho, rho*, s) -> (sigma, tau / k, rho / k, rho* / k, s / k) 
    # TODO implement 
    def raise_to_power(self, k):
        if not isinstance(k, int) or k < 2:
            raise ValueError("Parameter k must be an integer and >= 2.")
        raise NotImplementedError("TODO") # TODO


def derived_large_value_energy_region(data, proof, deps):
    year = Reference.max_year(tuple(d.reference for d in deps))
    bound = Hypothesis(
        "Derived large value energy region",
        "Large value energy region",
        data,
        proof,
        Reference.derived(year),
    )
    bound.dependencies = deps
    return bound

# Returns a Hypothesis object representing raising the large value energy region 
# to a integer power k. 
def get_raise_to_power_hypothesis(k):
    # name, hypothesis_type, data, proof, reference
    name = f"Large value energy region raise to power hypothesis with k = {k}"
    
    def f(h):
        region = copy.copy(h.data)
        region.raise_to_power(k)
        return derived_large_value_energy_region(
            region, 
            f"Follows from raising {h} to the k = {k} power",
            {h}
            )
    
    return Hypothesis(
        name,
        "Large value energy region transform",
        Transform(name, f),
        "Classical",
        Reference.classical(),
        )

# Convert an exponent pair (k, l) to a large value energy region 
# Lemma 10.15 
# s \leq 1 + max(
# rho + 1,
# 5/3 rho + tau / 3
# (2 + 3k + 4l) / (1 + 2k + 2l) rho + (k + l) / (1 + 2k + 2l) tau
# )
def ep_to_lver(eph):

    k, l = eph.data.k, eph.data.l
    
    # Construct Polytope of (rho, tau, s)
    limits = Large_Value_Energy_Region.default_limits()
    rho_limits, tau_limits, s_limits = limits[2], limits[1], limits[4]
    polys = []

    # default limits 
    rect = [
        [-rho_limits[0], 1, 0, 0],
        [rho_limits[1], -1, 0, 0],
        [-tau_limits[0], 0, 1, 0],
        [tau_limits[1], 0, -1, 0],
        [-s_limits[0], 0, 0, 1],
        [s_limits[1], 0, 0, -1]
        ]

    # 2 + rho - s >= 0
    polys.append(Polytope(rect + [[2, 1, 0, -1]]))

    # 1 + 5/3 * rho + 1/3 * tau - s >= 0
    polys.append(Polytope(rect + [[1, frac(5,3), frac(1,3), -1]]))

    # 1 + (2 + 3k + 4l) / (1 + 2k + 2l) rho + (k + l) / (1 + 2k + 2l) tau - s >= 0
    polys.append(Polytope(rect + [
        [
            1, 
            frac(2 + 3 * k + 4 * l, 1 + 2 * k + 2 * l),
            frac(k + l, 1 + 2 * k + 2 * l),
            -1
        ]]))

    region = Region.union([Region(Region_Type.POLYTOPE, p) for p in polys])
    return derived_large_value_energy_region(
        Large_Value_Energy_Region(region),
        f"Follows from {eph.data}",
        {eph})
    
print(ep_to_lver(ep.trivial_exp_pair).data)







