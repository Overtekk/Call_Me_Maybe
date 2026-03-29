# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  __main__.py                                       :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/02/23 16:39:56 by roandrie        #+#    #+#               #
#  Updated: 2026/03/29 22:21:20 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import sys

from src.utils.display import print_error
from src.parser import argument_parser, validate_json_content


def main() -> int:
    try:
        args = argument_parser()

        validation_map = {
            "func_call": args.func_call,
            "func_def": args.func_def
        }

        validated_data = {}
        for schema_type, path in validation_map.items():
            validated_data[schema_type] = validate_json_content(path,
                                                                schema_type)
        print(f"Successfully validated {len(validated_data['func_def'])} function definitions.")
        return 0

    except ValueError as e:
        print_error(e)
        return 1
    except Exception as e:
        print_error(f"Critical error: {e}")
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())

    except KeyboardInterrupt:
        print_error("\nProgram interrupted by user.")
        sys.exit(130)
