# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  llm_instructions_model.py                         :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/04/04 11:02:48 by roandrie        #+#    #+#               #
#  Updated: 2026/04/16 22:14:11 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import List

import json
import random


def get_instructions(func_def: List[str], user_prompt: str) -> str:
    # Instructions for the model
    task: str = ("Task: You are a function selector. Given a user request, "
                 "output the name of the best matching function.\n")

    # List of all functions available
    if not isinstance(func_def, List):
        raise ValueError("function_definition not a list.")

    function_def_str: str = "Available functions:\n"
    for function in func_def:
        function_def_str += (
            f"- {function.name}: {function.description}\n"
        )

    # Model for the output
    example_func: list[str] = random.choice(func_def)
    example_param: str = list(example_func.parameters.keys())[0]

    task_model_data: dict[str, str] = {
        "prompt": f"Use {example_func.name}",
        "name": f"{example_func.name}",
        "parameters": {
            "param": f"{example_param}"
        }
    }

    formatted_json: str = json.dumps(task_model_data, indent=2)

    model: str = f"Task Model:\n{formatted_json}\n"

    # User prompt
    if not isinstance(user_prompt, str):
        raise ValueError("user prompt not a string.")

    user_formated_prompt: str = (f"User request: {user_prompt}\n"
                                 "The best matching function name is: "
                        )


    return (
        task + function_def_str + model + user_formated_prompt
    )
