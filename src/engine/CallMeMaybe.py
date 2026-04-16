# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  CallMeMaybe.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/31 17:19:16 by roandrie        #+#    #+#               #
#  Updated: 2026/04/16 11:56:35 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Any, Dict, List

from pathlib import Path
from llm_sdk import Small_LLM_Model
from pydantic import BaseModel, Field, PrivateAttr

from src.utils import print_log
from src.engine.llm_instructions_model import get_instructions
from src.engine.Vocabulary import Vocabulary


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
    _vocab: Vocabulary = PrivateAttr()

    def model_post_init(self, context: Any) -> None:
        try:
            if self.debug or self.visualizer:
                print_log("Initializing LLM...")

            # Init the LLM Model
            self._model = Small_LLM_Model()

            # Init the Vocabulary Class
            self._vocab = Vocabulary(
                path_file=self._model.get_path_to_vocab_file(),
                debug=self.debug
            )

        except Exception as e:
            raise ValueError(f"error while initializing model: {e}")

        return super().model_post_init(context)

    def run(self, prompt: str) -> None:
        # Get the formatted instructions for the LLM
        instructions: str = get_instructions(self.functions_definition_path, prompt)

        if self.debug:
            print_log(f"-DEBUG-\nInstructions:\n{instructions}")

        token_id: list[int] = []

        input_ids: list = self._model.encode(instructions)[0].tolist()

        self.get_function_name(instructions)

        # while (True):
        #     probabilities: list[float] = self._model.get_logits_from_input_ids(input_ids + token_id)
        #     next_token: float = max(probabilities)
        #     next_token_id: int = probabilities.index(next_token)
        #     token_id.append(next_token_id)
        #     valid_token: str = self._model.decode([next_token_id])
        #     print(valid_token, end="", flush=True)
        #     if next_token_id in ["<|endoftext|>", "<|im_end|>"]:
        #         break

    def get_function_name(self, prompt: str) -> None:
        token_sequences: Dict[str, List[int]] = {}

        for func in self.functions_definition_path:
            input_ids: list[int] = self._model.encode(func.name)[0].tolist()
            token_sequences[func.name] = input_ids

        prompt_input_ids: list[int] = self._model.encode(prompt)[0].to_list()

