"""Exploring continued fraction, to build up an intuition.
For now we'll assume that the numerator = 1,
    i.e. we're dealing with simple continued fraction,
    not the generalized version."""
# import numpy as np
import math
from decimal import Decimal

def cf_sum(l):
    """In: a list of continued fraction coefficients
    Out: the sum

    sums the continued fraction recursively."""

    if len(l)==1:
        return l[0]
    elif len(l)>1:
        return Decimal(l[0]) + 1/Decimal(cf_sum(l[1:]))

def approximate(exact, num_terms, verbose=False):
    """Approximate x using num_terms-long continued fraction"""
    x = Decimal(exact)
    one = Decimal(1.0)
    terms = []
    for step in range(num_terms):
        terms.append(int(x//1)) # find the integer part
        x = x%one
        if verbose:
            print(f"{step=}, residual={x}")
            print(f"Reconstructed number differs by ={cf_sum(terms) - exact}")
        if x == 0.0:
            return terms
        x = 1/x
    return terms

def format_series(l):
    """In: a list of integers (representing the coefficients in the continued fraction)
    Out: a string output that, when printed, looks like the algebraic continued fraction expression."""
    if len(l)==1:
        coef = str(l[0])
        return "\n".join([coef])
    elif len(l)>1:
        right_denom = format_series(l[1:])
        right_denom = right_denom.split("\n")
        coef = str(l[0])

        frac_width = len(right_denom[0])
        new_width = len(coef)+3+frac_width # calculate the width of the resultant

        fraction = [str(1).center(frac_width), "-"*frac_width] + right_denom

        added_coef_line = coef + " + " + fraction[1]
        return "\n".join([fraction[0].rjust(new_width), added_coef_line, *[line.rjust(new_width) for line in fraction[2:]]])

def series_to_simple_fraction(l):
    """Turn a series representation of a continued fraction (i.e. a series of ints)
    into a simple `integer p over integer q` expression.
    """
    if isinstance(l[-1], int):
        new_l = l[:-1]
        new_l.append( (int(l[-1]), 1) ) # a tuple!
        return series_to_simple_fraction(new_l)
    if len(l)==1:
        old_numin, old_denom = l[0]
        gcd = math.gcd(old_numin, old_denom)
        new_numin, new_denom = int(old_numin/gcd), int(old_denom/gcd)
        frac_width = max(len(str(old_numin)), len(str(old_denom)))
        return "\n".join([str(new_numin).center(frac_width),
                          "-"*frac_width,
                          str(new_denom).center(frac_width)])
    else:
        new_l = l[:-2]
        old_numin, old_denom = l[-1]

        # flip the fraction upside down, and then add.
        new_numin = l[-2] * old_numin + old_denom
        new_denom = old_numin
        new_l.append( (new_numin, new_denom) )
        return series_to_simple_fraction(new_l)

mode = None
if __name__=="__main__":
    modes_of_op = ["approximation", "format"]
    choice = -1
    while choice<0:
        print("Please choose your mode of operation (enter the number:)")
        for i, m_o_p in enumerate(modes_of_op):
            print(f"{i}:{m_o_p}")
        choice = int(input())
    mode = modes_of_op[choice]
    print(mode)

if mode=="approximation":
    # let's use a few simple series:
    exact = Decimal(input("Please enter a float number: "))
    max_terms = 29
    for i in range(1,max_terms):
        series = approximate(exact, i, i>max_terms)
        print("{:2d}: {:30f}= {}".format(i, cf_sum(series) - exact, series))
if mode=="format":
    series = input("Please input the series: ").strip("[]()").replace(',', ' ').split()
    print(format_series(series))
    print("Result =")
    print(series_to_simple_fraction([int(i) for i in series]))