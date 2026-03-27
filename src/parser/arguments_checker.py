# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  arguments_checker.py                              :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/27 14:02:23 by roandrie        #+#    #+#               #
#  Updated: 2026/03/27 16:02:21 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import argparse
import sys

from src.parser.path_checker import validate_json_input, validate_json_output
from src.utils import print_error


def argument_parser() -> argparse.Namespace:
    parser = RichArgumentParser(
        prog="Call Me Maybe",
        description=("Function calling tool that translates natural "
                        "language prompts into structured function calls"),
        usage=("python -m src [--functions_definition "
                "<function_definition_file>] [--input <input_file>] "
                "[--output <output_file>]"),
        epilog=" ",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "-f", "--functions_definition",
        help=("path where function definition in json is stored.\n"
                "default: data/input/functions_definition.json)\n\n"),
        default="data/input/functions_definition.json",
        metavar="file.json",
        type=validate_json_input
    )
    parser.add_argument(
        "-i", "--input",
        help=("path where input file in json is stored.\n"
                "(default: data/input/function_calling_tests.json)\n\n"),
        default="data/input/function_calling_tests.json",
        metavar="file.json",
        type=validate_json_input
    )
    parser.add_argument(
        "-o", "--output",
        help=("path to the output file in json.\n"
                "(default: data/output/function_calling_results.json)\n\n"),
        default="data/output/function_calling_results.json",
        metavar="file.json",
        type=validate_json_output
    )
    parser.add_argument(
        "-v", "--visualizer",
        help="launch with the visualizer\n\n",
        required=False,
        action="store_true"
    )
    parser.add_argument(
        "-d", "--debug",
        help="launch with the debug mode",
        required=False,
        action="store_true"
    )

    args = parser.parse_args()
    return args


class RichArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        print_error(message)
        self.print_usage(sys.stderr)
        sys.exit(2)
