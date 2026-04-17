# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  CallMeMaybe.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/31 17:19:16 by roandrie        #+#    #+#               #
#  Updated: 2026/04/17 10:25:48 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Any, Dict, List
from numpy.typing import NDArray

import numpy

from pathlib import Path
from llm_sdk import Small_LLM_Model
from pydantic import BaseModel, Field, PrivateAttr

from src.parser.models.schemas import JsonFunctionDefinition
from src.utils import print_log, print_rule
from src.engine.llm_instructions_model import get_instructions
from src.engine.Vocabulary import Vocabulary


class CallMeMaybe(BaseModel):
    functions_definition_path: List[JsonFunctionDefinition] = Field(
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
            if self.debug:
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
        instructions: str = get_instructions(
            self.functions_definition_path, prompt
            )

        dict_vocab: dict[int, str] = self._vocab.get_id_to_token_vocab()

        if self.debug:
            print_rule("Generation Process")
            print_log(f"-DEBUG-\nInstructions:\n\n'{instructions}'\n")

        self.generate_function_name(instructions, dict_vocab)

    def generate_function_name(self, prompt: str,
                               dict_vocab: Dict[int, str]) -> str:
        token_sequences: Dict[str, List[int]] = {}

        # Get functions name to token
        for func in self.functions_definition_path:
            input_ids: list[int] = self._model.encode(func.name)[0].tolist()
            token_sequences[func.name] = input_ids

        # Get prompts token
        prompt_input_ids: list[int] = self._model.encode(prompt)[0].tolist()

        # Generation
        current_ouput: str = ""
        current_token: list[int] = []

        while (True):
            # Combined all tokens
            all_token: list[int] = prompt_input_ids + current_token

            # Get the logits token
            logits: list[float] = self._model.get_logits_from_input_ids(
                all_token
            )

            # Identifiate valid tokens
            valid_tokens: set[int] = set()
            for func in self.functions_definition_path:

                if func.name.startswith(current_ouput):
                    name_encoding = token_sequences[func.name]
                    next_position = len(current_token)

                    if next_position < len(name_encoding):
                        valid_tokens.add(name_encoding[next_position])

            # Security if token is not valid
            if not valid_tokens:
                if self.debug:
                    print_log(
                        f"[dark_red]Invalid token {valid_tokens}[/dark_red]\n"
                    )
                break

            # Mask token we don't want
            logits_masked: NDArray[Any] = numpy.full_like(
                logits, -numpy.inf, dtype=float
            )
            for token_id in valid_tokens:
                logits_masked[token_id] = logits[token_id]

            # Select best token
            best_token_id: int = int(numpy.argmax(logits_masked))
            current_token.append(best_token_id)

            # Convert token in string
            token_string = dict_vocab.get(best_token_id, "")
            current_ouput += token_string

            # Avoid infinite loop if token is empty
            if not token_string:
                if self.debug:
                    print_log("[dark_red]Didn't find token![/dark_red]\n")
                break

            # Stop the loop if the name have been found
            if any(func.name == current_ouput
                   for func in self.functions_definition_path):
                break

        if self.debug:
            print_log(f"[green]Generated name: '{current_ouput}'[/green]\n")

        return current_ouput
