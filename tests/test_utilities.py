#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""Utilities for tests."""

import string
import random
import ROOT

def float_compare(x_val, y_val, precision=1e-6):
    '''Helper function to check that two numbers are equal within float precision.'''
    if y_val == 0:
        return x_val == 0
    if abs((x_val - y_val) / y_val) < precision:
        return True
    return False


def tuple_compare(x_tup, y_tup):
    '''Helper function to check that two tuples are equal within float precision.'''
    same = True
    for pair in zip(x_tup, y_tup):
        same &= float_compare(pair[0], pair[1])
    return same

def histogram_compare_1d(hist1, hist2):
    '''
    Helper function to check that two 1D histograms are equivalent.

    Will check:
        * Number of bins
        * Bin edges
        * Bin contents
        * Bin errors
    '''
    bin_functions_to_check = [
        "GetBinContent",
        "GetBinErrorUp",
        "GetBinErrorLow"
    ]
    try:
        assert(hist1.GetNbinsX() == hist2.GetNbinsX())

        for ibin in range(0,hist1.GetNbinsX()+2):
            for function in bin_functions_to_check:
                val1 = getattr(hist1, function)(ibin)
                val2 = getattr(hist2, function)(ibin)
                assert(float_compare(val1, val2))
    except AssertionError:
        return False

    return True


def get_random_id(length=12):
    """
    Return random ID string of given length.

    Useful for temporary files, etc.
    """
    return "".join(random.sample(string.ascii_uppercase+string.digits,length))

def make_tmp_root_file(
                       path_to_file='tmp_{}.root'.format(get_random_id()),
                       mode="RECREATE",
                       close=False
                       ):
    """
    Create a temporary ROOT file.

    :param path_to_file: path where the file should be created.
                         Can be absolute or relative.
    :type path_to_file: string

    :param mode: File creation mode to use (must be valid ROOT file mode)
    :type mode: string

    :param close: If True, close the file immediately and return only the path to the file.
    :type close: bool
    """

    # if not path_to_file:
        # path_to_file = "{}.root".format(get_random_id())
    rfile = ROOT.TFile(path_to_file, mode)

    if not rfile:
        raise RuntimeError("Failed to create temporary file: {}".format(path_to_file))

    if(close):
        rfile.Close()
        return path_to_file
    else:
        return rfile
