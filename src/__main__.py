# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  __main__.py                                       :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/02/23 16:39:56 by roandrie        #+#    #+#               #
#  Updated: 2026/03/27 15:22:47 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import sys

from src.utils.display import print_error
from src.parser import argument_parser
from src.utils.custom_errors import ArgumentsError


def main() -> int:
    try:

        args = argument_parser()
        print(args)

    except ArgumentsError as e:
        print_error(e)
    except Exception as e:
        print_error(e)


if __name__ == "__main__":
    try:
        sys.exit(main())

    except KeyboardInterrupt:
        print_error("\nProgram interrupted by user.")
        sys.exit(130)
