# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  parse_json_file.py                                :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/29 16:03:32 by roandrie        #+#    #+#               #
#  Updated: 2026/03/29 21:16:31 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import json
import pathlib

from pydantic import ValidationError
from json import JSONDecodeError

from src.parser.models.schemas import (JsonFunctionCalling,
                                       JsonFunctionDefinition)


def files_validator(type: str, file: pathlib.__file__) -> None:
    try:
        json.load(file)

        if type == "func_calling_tests":
            JsonFunctionCalling(file)
        else:
            JsonFunctionDefinition(file)

    except JSONDecodeError:
        raise JSONDecodeError(f"malformated json file for {file}")
    except ValidationError:
        raise ValidationError(f"bad writing for {file}")
    except Exception:
        raise Exception(f"an error have occured for {file}")

