# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  parse_json_file.py                                :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/29 16:03:32 by roandrie        #+#    #+#               #
#  Updated: 2026/03/29 22:31:14 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import List, Union

import json
import pathlib

from pydantic import TypeAdapter, ValidationError
from json import JSONDecodeError

from src.parser.models.schemas import (JsonFunctionCalling,
                                       JsonFunctionDefinition)


def validate_json_content(
    file_path: pathlib.Path,
    schema_type: str) -> (Union[List[JsonFunctionDefinition],
                                List[JsonFunctionCalling]]):
    try:
        content = file_path.read_text(encoding='utf-8')
        data = json.loads(content)

        if schema_type == "func_call":
            adapter = TypeAdapter(List[JsonFunctionCalling])
            return adapter.validate_python(data)

        elif schema_type == "func_def":
            adapter = TypeAdapter(List[JsonFunctionDefinition])
            return adapter.validate_python(data)

        else:
            raise ValueError(f"Unknown schema type: {schema_type}")

    except JSONDecodeError as e:
        raise ValueError(f"Syntax error in JSON file '{file_path}': {e}")

    except ValidationError as e:
        raise ValueError(f"Validation failed for '{file_path}':\n{e}")

    except Exception as e:
        raise Exception("An unexpected error occurred while validating "
                        f"'{file_path}': {e}")

