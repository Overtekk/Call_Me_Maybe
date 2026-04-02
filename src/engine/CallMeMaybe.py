# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  CallMeMaybe.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/31 17:19:16 by roandrie        #+#    #+#               #
#  Updated: 2026/04/02 14:36:09 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Any, List

from pathlib import Path
from llm_sdk import Small_LLM_Model
from pydantic import BaseModel, Field, PrivateAttr

from src.utils import print_log


class CallMeMaybe(BaseModel):
    functions_definition_path: List = Field(
        description='Path where functions are stored (json files)'
    )
    output_file_path: Path = Field(
        description='Path where the output will be writted'
    )
    visualizer: bool = Field(
        description="The state of the visualizer",
        default=False
    )
    debug: bool = Field(
        description="The state of the debug mode",
        default=False
    )

    _model: Small_LLM_Model = PrivateAttr()

    def model_post_init(self, _: Any) -> None:
        try:
            if self.debug or self.visualizer:
                print_log("Initializing LLM...")
            self._model = Small_LLM_Model()
        except Exception as e:
            raise ValueError(f"error while initializing model: {e}")

    def run(self, prompt: str) -> None:
        self._model.encode(prompt)
