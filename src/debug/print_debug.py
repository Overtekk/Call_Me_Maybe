# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  print_debug.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/04/02 14:02:40 by roandrie        #+#    #+#               #
#  Updated: 2026/04/17 09:58:03 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #
"""
Debug utilaty tool to show validated data. Only showed in the debug mode
state.
"""

from src.parser.models.schemas import (JsonFunctionCalling,
                                       JsonFunctionDefinition)


def print_validated_data(data: list[JsonFunctionDefinition] |
                         list[JsonFunctionCalling]) -> None:
    """Print all validated data to the standard stdout.

    Args:
        data (list[JsonFunctionDefinition] | list[JsonFunctionCalling]): a list
        containing a list of Json Function.
    """
    for element in data:
        print(element)
        print("")
