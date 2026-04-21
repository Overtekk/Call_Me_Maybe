# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  func_timer.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/04/21 13:32:36 by roandrie        #+#    #+#               #
#  Updated: 2026/04/21 13:56:23 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #
"""
Performance profiling utilities.

This module provides decorators and tools to measure and log
the execution time of specific functions or methods within the tool.
"""

from functools import wraps
from time import perf_counter

from src.utils import print_log


def func_timer(f):
    """
    Decorator to measure and log the execution time of a function.

    Wraps the target function to calculate the exact time elapsed
    during its execution using a high-resolution performance counter.
    The duration is logged using the project's standard logger.

    Args:
        f (Callable): The function or method to be timed.

    Returns:
        Callable: The wrapped function, which executes the original
        function and returns its unmodified result.
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        time_start = perf_counter()
        func_result = f(*args, **kwargs)
        time_end = perf_counter()

        execution_time = time_end - time_start
        print_log(f"\nAction took {execution_time:.4f} seconds.\n")

        return func_result
    return wrap
