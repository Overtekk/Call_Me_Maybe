# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  __main__.py                                       :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/02/23 16:39:56 by roandrie        #+#    #+#               #
#  Updated: 2026/03/31 17:44:04 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import sys

from src.utils import print_error, print_log, print_rule, print_logo
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

        print_logo()
        print_rule("")
        print_log("Successfully validated "
                    f"{len(validated_data['func_def'])} function "
                    "definitions.")
        print_log("Successfully validated "
                    f"{len(validated_data['func_call'])} function calling.")

        if args.debug:
            print_rule("", "white")
            print(f"\nfunc_def:\n{validated_data['func_def']}\n")
            print(f"func_call:\n{validated_data['func_call']}")

        return 0

    except ValueError as e:
        print_error(f"{e}")
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
