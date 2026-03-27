# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  files.py                                          :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/27 14:15:34 by roandrie        #+#    #+#               #
#  Updated: 2026/03/27 15:08:15 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import pathlib


def is_folder_exist(path_to_folder: pathlib.Path) -> bool:
    return path_to_folder.exists() and path_to_folder.is_dir()

def is_file_exist(file: pathlib.Path) -> bool:
    return file.exists() and file.is_file()

def is_file_json(file: pathlib.Path) -> bool:
    return file.suffix == ".json"
