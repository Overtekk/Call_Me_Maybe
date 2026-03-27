# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  files.py                                          :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/27 14:15:34 by roandrie        #+#    #+#               #
#  Updated: 2026/03/27 14:27:04 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import pathlib


def is_folder_exist(path_to_folder: pathlib.Path) -> bool:
    if path_to_folder.exists() and path_to_folder.is_dir():
        return True
    return False

def is_file_exist(file: pathlib.Path) -> bool:
    if file.exists() and file.is_file():
        return True
    return False

def is_file_json(file: pathlib.Path) -> bool:
    if file.suffix == ".json":
        return True
    return False
