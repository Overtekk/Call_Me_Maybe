# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  prompt.py                                         :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/04/04 12:04:02 by roandrie        #+#    #+#               #
#  Updated: 2026/04/17 13:23:48 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Any, List

import json

from pydantic import BaseModel, Field, PrivateAttr

from src.models import JsonFunctionCalling
from src.utils import print_log


class Prompt(BaseModel):
    functions_calling: List[JsonFunctionCalling] = Field(
        description='Path where promps are stored (json files)'
    )
    visualizer: bool = Field(
        description="The state of the visualizer",
        default=False
    )
    debug: bool = Field(
        description="The state of the debug mode",
        default=False
    )

    _list_prompts: List[str] = PrivateAttr()

    def model_post_init(self, _: Any) -> None:
        self._list_prompts: List[str] = []

        self._format_prompt()

    def get_next_prompt(self) -> str:
        if self._list_prompts:
            return self._list_prompts.pop(-1)
        else:
            return "empty"

    def _format_prompt(self) -> None:
        for prompt in self.functions_calling:
            formatted_prompt = json.dumps({"prompt": prompt.prompt})

            if self.debug:
                print_log(f"-DEBUG-\nNew prompt added: {formatted_prompt}")

            self._list_prompts.append(formatted_prompt)
