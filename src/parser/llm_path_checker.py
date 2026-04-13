# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  llm_path_checker.py                               :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/04/13 08:50:14 by roandrie        #+#    #+#               #
#  Updated: 2026/04/13 09:20:59 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import pathlib
import os

from src.utils import is_folder_exist, is_file_exist


qwen_model_path = {
    "init": "llm_sdk/llm_sdk/__init__.py",
    "pyproject": "llm_sdk/pyproject.toml"
}
llm_folder_path = {
    "folder": "llm_sdk",
    "sub_folder": "llm_sdk/llm_sdk"
}


def check_llm_available() -> None:
    for folder_path in llm_folder_path.values():
        path = pathlib.Path(folder_path)

        if not is_folder_exist(path):
            raise ValueError(f"Missing '{path}' folder.")
        if not os.access(path, os.R_OK):
            raise ValueError(f"Path  '{path}' can't be read.")

    for file_path in qwen_model_path.values():
        path = pathlib.Path(file_path)

        if not is_file_exist(path):
            raise ValueError(f"Missing '{path}' from llm_sdk.")
        if not os.access(path, os.R_OK):
            raise ValueError(f"Can't read '{path}' from llm_sdk.")
