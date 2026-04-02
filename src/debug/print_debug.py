# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  print_debug.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/04/02 14:02:40 by roandrie        #+#    #+#               #
#  Updated: 2026/04/02 14:06:34 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import List


def print_validated_data(data: List[str]) -> None:
    for element in data:
        print(element)
        print("")
