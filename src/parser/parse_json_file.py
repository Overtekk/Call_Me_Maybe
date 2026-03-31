# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  parse_json_file.py                                :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/29 16:03:32 by roandrie        #+#    #+#               #
#  Updated: 2026/03/31 17:01:41 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #
"""
Validate the content of a json file.

This module provides utilities to read JSON files and validate their internal
structure against specific Pydantic models. It ensures that both function
definitions and test prompts are strictly compliant before being processed
by the LLM.
"""

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
    """
    Load and validate the content of a JSON file against a specific schema.

    This function reads the raw text from the provided path, parses it into
    a Python object, and uses Pydantic TypeAdapters to verify that the data
    matches the expected structure for either function definitions or
    calling tests.

    Args:
        file_path (pathlib.Path): The path to the JSON file to be validated.
        schema_type (str): The identifier for the schema to use
                           ('func_call' or 'func_def').

    Raises:
        ValueError: If the JSON is malformed, if the schema validation fails,
                    or if an unknown schema type is provided.
        Exception: If an unexpected error occurs during file I/O or processing.

    Returns:
        Union[List[JsonFunctionDefinition], List[JsonFunctionCalling]]:
            A list of validated Pydantic model instances representing the file
            content.
    """
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
