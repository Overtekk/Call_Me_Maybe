# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  path_checker.py                                   :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/27 14:27:44 by roandrie        #+#    #+#               #
#  Updated: 2026/03/27 14:59:44 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import pathlib
import os
import argparse

from src.utils import is_file_exist, is_folder_exist, is_file_json


def validate_json_input(path_str: str) -> pathlib.Path:
    try:
        path = pathlib.Path(path_str)

        if not is_file_exist(path) and not is_file_json(path):
            raise argparse.ArgumentTypeError
        if not os.access(path, os.R_OK):
            raise argparse.ArgumentTypeError

        return path
    except argparse.ArgumentTypeError:
        raise argparse.ArgumentTypeError


def validate_json_output(path_str: str) -> pathlib.Path:
    try:
        path = pathlib.Path(path_str)

        if not is_folder_exist(path) or not is_file_exist(path):
            path.mkdir(parents=True, exist_ok=True)

        return path
    except argparse.ArgumentTypeError:
        raise argparse.ArgumentTypeError
