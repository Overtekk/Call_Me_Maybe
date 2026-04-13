# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  CallMeMaybe.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/31 17:19:16 by roandrie        #+#    #+#               #
#  Updated: 2026/04/13 11:41:27 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Any, List

from pathlib import Path
from llm_sdk import Small_LLM_Model
from pydantic import BaseModel, Field, PrivateAttr

from src.utils import print_log
from src.engine.llm_instructions_model import get_instructions


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
        instructions = get_instructions(self.functions_definition_path, prompt)

        if self.debug:
            print_log(f"-DEBUG-\nInstructions:\n{instructions}")

        tensors = self._model.encode(instructions)
        probabilities = self._model.get_logits_from_input_ids(tensors.tolist()[0])
        sorted_tokens = sorted(probabilities, reverse=True)
        vocab_path = self._model.get_path_to_vocab_file()
