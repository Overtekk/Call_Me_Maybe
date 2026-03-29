# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  __main__.py                                       :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/02/23 16:39:56 by roandrie        #+#    #+#               #
#  Updated: 2026/03/29 21:18:07 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import sys

from json import JSONDecodeError
from pydantic import ValidationError

from src.utils.display import print_error
from src.parser import argument_parser, files_validator


def main() -> int:
    try:
        args = argument_parser()

        input_func = {
            "func_calling_tests": args.func_call,
            "func_def": args.func_def
        }

        try:
            for type, func in input_func.items():
             with open(func, 'r', encoding='utf-8') as f:
                 files_validator(type, f)
        except (ValidationError, JSONDecodeError) as e:
            print_error(e)

    except Exception as e:
        print_error(e)


if __name__ == "__main__":
    try:
        sys.exit(main())

    except KeyboardInterrupt:
        print_error("\nProgram interrupted by user.")
        sys.exit(130)
