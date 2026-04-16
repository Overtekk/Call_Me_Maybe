# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  llm_instructions_model.py                         :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/04/04 11:02:48 by roandrie        #+#    #+#               #
#  Updated: 2026/04/16 20:17:26 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import List


def get_instructions(func_def: List[str], user_prompt: str) -> str:
    # Task for the model
    task = ("Task: You are a function selector. Given a user request, output "
            "the name of the best matching function.\n")

    if not isinstance(func_def, List):
        raise ValueError("function_definition not a list.")

    # List of all functions available
    function_def_str = "Available functions:\n"
    for function in func_def:
        function_def_str += (
            f"- {function.name}: {function.description}\n"
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

    user_formated_prompt = f"User request: {user_prompt}"


    return (
        task + function_def_str + model + user_formated_prompt
    )
