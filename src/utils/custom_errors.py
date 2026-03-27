# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  custom_errors.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/27 15:20:16 by roandrie        #+#    #+#               #
#  Updated: 2026/03/27 15:21:37 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import argparse

from src.utils import print_error


class ArgumentsError(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        print_error(message)
