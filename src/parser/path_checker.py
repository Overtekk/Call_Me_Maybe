# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  path_checker.py                                   :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/27 14:27:44 by roandrie        #+#    #+#               #
#  Updated: 2026/03/27 15:11:37 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import pathlib
import os
import argparse

from src.utils import is_file_exist, is_folder_exist, is_file_json


def validate_json_input(path_str: str) -> pathlib.Path:
    path = pathlib.Path(path_str)

    if not is_file_exist(path):
        raise argparse.ArgumentTypeError
    if not is_file_json(path):
        raise argparse.ArgumentTypeError
    if not os.access(path, os.R_OK):
        raise argparse.ArgumentTypeError

    return path


def validate_json_output(path_str: str) -> pathlib.Path:
    path = pathlib.Path(path_str)

    if not is_file_json(path):
        raise argparse.ArgumentTypeError

    folder_parent = path.parent()
    if not is_folder_exist(folder_parent):
        raise argparse.ArgumentTypeError
    if not os.access(folder_parent, os.W_OK):
        raise argparse.ArgumentTypeError

    return path
