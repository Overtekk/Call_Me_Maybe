# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  llm_instructions_model.py                         :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/04/04 11:02:48 by roandrie        #+#    #+#               #
#  Updated: 2026/04/14 14:44:42 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import List


def get_instructions(func_def: List[str], user_prompt: str) -> str:
    # Task for the model
    task = ("Task: Choose the best fonction to solve the user prompt. "
            "Return in JSON format.\n")

    if not isinstance(func_def, List):
        raise ValueError("function_definition not a list.")

    # List of all functions available
    function_def_str = "List of all availables functions: "
    for function in func_def:
        function_def_str += (
            '{\n'
            f'  "name": "{function.name}",\n'
            f'  "description": "{function.description}",\n'
            '  "parameters": {\n'
            f'  {function.parameters}\n'
            '  "returns": {\n'
            f'  {function.returns}\n'
            '}\n'
        )

    # Task model
    model = ('Task Model\n:'
             '{\n'
             '  "prompt": "Write "koala",\n'
             '  "name": "fn_write",\n'
             '  "parameters": {"s": "koala"}\n'
             '}\n'
        )

    if not isinstance(user_prompt, str):
        raise ValueError("user prompt not a string.")

    return task + function_def_str + model + user_prompt
