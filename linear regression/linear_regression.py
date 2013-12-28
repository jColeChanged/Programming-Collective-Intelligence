# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 14:42:27 2013

@author: joshua
"""
import numpy

# The least squares regression line minimizes the residual squared. The 
# residual is the error. It is the distance between the prediction and the 
# observed value.
#
# The line is described by:
#
#          std(x)                     std(x)
# y^ = r ------- x + avg(y) - avg(x) -------
#          std(y)                     std(y)
#
# This line becomes unreliable when estimating when there is little linear
# corellation in the dataset and when estimating ranges that it has not seen
# before.

def least_squares(x, r, std_x, std_y, avg_x, avg_y):
    slope = r * std_y / std_x
    y_intercept = avg_y - avg_x * slope
    return slope * x + y_intercept
    