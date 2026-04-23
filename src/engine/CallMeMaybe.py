# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  CallMeMaybe.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/31 17:19:16 by roandrie        #+#    #+#               #
#  Updated: 2026/04/23 13:57:17 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Any, Dict, List
from numpy.typing import NDArray

import numpy

from llm_sdk import Small_LLM_Model
from pydantic import BaseModel, Field, PrivateAttr

from src.utils import print_log, print_vizualizer, print_rule
from src.engine.llm_instructions_model import (get_instructions,
                                               get_param_instructions)
from src.engine.Vocabulary import Vocabulary
from src.models import DataType, JsonFunctionDefinition
from src.debug import debug_print_generating_process


class CallMeMaybe(BaseModel):
    model_name: str = Field(
        description="Name of the model"
    )
    functions_definition_path: List[JsonFunctionDefinition] = Field(
        description="Path where functions are stored (json files)"
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
    _functions_def_dict: dict[str, JsonFunctionDefinition] = (
        PrivateAttr(default_factory=dict)
    )

    def model_post_init(self, context: Any) -> None:
        try:
            if self.debug:
                print_log("Initializing LLM...")

            # Init the LLM Model
            self._model = Small_LLM_Model(
                model_name=self.model_name
            )

            # Init the Vocabulary Class
            self._vocab = Vocabulary(
                path_file=self._model.get_path_to_tokenizer_file(),
                debug=self.debug
            )

            # Convert the JSON object to a dict
            for func in self.functions_definition_path:
                self._functions_def_dict[func.name] = func

            if self.visualizer:
                print_log("LLM loaded! Starting generation...\n")

        except Exception as e:
            raise ValueError(f"error while initializing model: {e}")

        return super().model_post_init(context)

    def run(self, prompt: str) -> dict[Any, Any]:
        dict_vocab: dict[int, str] = self._vocab.get_id_to_token_vocab()
        output_result: dict[Any, Any] = {}

        # Function name
        # Get the formatted instructions for the LLM
        instructions_func_name: str = get_instructions(
            self.functions_definition_path, prompt
            )

        # Show generation process for debug only
        if self.debug:
            debug_print_generating_process(instructions_func_name, 'Name')

        if self.visualizer:
            print_log(
                "User prompt request: "
                "[light_blue]"
                f"{prompt}\n\n"
                "[/light_blue]"
                "Generating function name...\n"
            )

        # Generation
        func_name: str = self.generate_function_name(
            instructions_func_name, dict_vocab
        )
        output_result['name'] = func_name

        # Function parameters
        # Get the formatted instructions for the LLM
        func_def: JsonFunctionDefinition | None = (
            self._functions_def_dict.get(func_name)
        )

        if func_def is None:
            raise ValueError(
                f"Function definition for '{func_name}' not found."
            )

        if self.visualizer:
            print_log(
                "Generating function parameters...\n"
            )

        instructions_func_param: str = get_param_instructions(
            func_def, prompt
        )

        # Show generation process for debug only
        if self.debug:
            debug_print_generating_process(
                instructions_func_param, 'Parameters'
            )

        # Generation
        func_param: dict[Any, Any] = self.generate_function_param(
            instructions_func_param, func_name, dict_vocab
        )
        output_result['parameters'] = func_param

        if self.visualizer:
            print_log("✅ Generation finished.")
            print_rule("")

        return output_result

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
        current_output: str = ""
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

                if func.name.startswith(current_output):
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
            token_string = (
                token_string.replace('\u2581', '').replace('\u0120', '')
            )
            current_output += token_string

            if self.visualizer:
                print_vizualizer(f'\r{current_output}')

            # Avoid infinite loop if token is empty
            if not token_string:
                if self.debug:
                    print_log("[dark_red]Didn't find token![/dark_red]\n")
                break

            # Stop the loop if the name have been found
            if any(func.name == current_output
                   for func in self.functions_definition_path):
                break

        if self.debug:
            print_log(f"[green]Generated name: '{current_output}'[/green]\n")

        if self.visualizer:
            print_log(
                f"\nGenerated name: {current_output}.\n"
            )

        return current_output

    def generate_function_param(self, prompt: str, func_name: str,
                                dict_vocab: Dict[int, str]) -> Dict[Any, Any]:

        func_def = self._functions_def_dict.get(
            func_name
        )

        if func_def:
            func_param: dict[str, Any] = func_def.parameters
        else:
            return {}

        # Generation
        output_result: dict[Any, Any] = {}

        for param_name in func_param:
            # Construct the output string for the LLM instructions
            output_generation: str = ""
            for name_result in output_result.keys():
                output_generation = output_generation + name_result + '='
                output_generation += str(output_result[name_result]) + '\n'

            if func_param[param_name].type == DataType.STRING:
                output_result[param_name] = self.gen_type_str_param(
                    prompt, output_generation, param_name, dict_vocab
                )

            elif func_param[param_name].type == DataType.NUMBER:
                output_result[param_name] = self.gen_type_number_param(
                    prompt, output_generation, param_name, dict_vocab
                )

            if self.visualizer:
                print_vizualizer(f'\n{output_result[param_name]}\n')

        if self.debug:
            print_log(f"[green]Generated params: '{output_result}'[/green]\n")

        if self.visualizer:
            print_log(f"Generated parameters: {output_result}\n")

        return output_result

    def gen_type_str_param(self, prompt: str, output_generation: str,
                           func_param_name: str,
                           dict_vocab: Dict[int, str]) -> str:
        # Get prompts token
        prompt_input_ids: list[int] = self.get_prompt_input_ids(
            prompt, output_generation, func_param_name
        )

        # Generation
        current_output: str = ""
        current_tokens: list[int] = []
        max_tokens: int = 100

        while len(current_tokens) < max_tokens:
            # Combined all tokens
            all_token: list[int] = prompt_input_ids + current_tokens

            # Get the logits token
            logits: list[float] = self._model.get_logits_from_input_ids(
                all_token
            )

            # Select best token
            best_token_id: int = int(numpy.argmax(logits))
            current_tokens.append(best_token_id)

            # Convert token to string
            token_string: str = dict_vocab.get(best_token_id, "")

            # If token is empty, break the loop
            if not token_string:
                break

            # Add the string to the current output
            current_output += token_string

            if self.visualizer:
                print_vizualizer(f'\r{current_output}')

            # If end a line detected, break the loop
            if '\n' in current_output:
                current_output = current_output.split('\n')[0]
                break

            # If '\u010a' (special character for '\n' used by the LLM), break
            # the loop
            if '\u010a' in current_output:
                current_output = current_output.split('\u010a')[0]
                break

            # Special characters from LLama models
            if '<0x0A>' in current_output:
                current_output = current_output.split('<0x0A>')[0]
                break

            if '</s>' in current_output:
                current_output = current_output.split('</s>')[0]
                break

            if '<|user|>' in current_output:
                current_output = current_output.split('<|user|>')[0]
                break

            # If multiples spaces detected, break the loop
            if '  ' in current_output:
                current_output = current_output.split('  ')[0]
                break

        # Clear the output from special characters generated by the LLM
        # and from space and quotes
        clean_ouput: str = (
            current_output.replace('\u0120', ' ').replace('\u2581', ' ').
            strip()
        )

        if (clean_ouput.startswith(('"', "'")) and
                clean_ouput.endswith(('"', "'")) and
                len(clean_ouput) >= 2):
            clean_ouput = clean_ouput[1:-1]

        return clean_ouput

    def gen_type_number_param(self, prompt: str, output_generation: str,
                              func_param_name: str,
                              dict_vocab: Dict[int, str]) -> float | None:
        # Get prompts token
        prompt_input_ids: list[int] = self.get_prompt_input_ids(
            prompt, output_generation, func_param_name
        )

        # Generation
        current_output: str = ""
        current_tokens: list[int] = []
        max_tokens: int = 42
        valid_chars = {
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', '\n', '-'
        }

        # Create a set to have all validate tokens from the dict_vocab
        valid_tokens: set[int] = set()
        for token_id, token_str in dict_vocab.items():
            # Clean the string to check more easily
            clean_token_str = (
                token_str.replace('Ġ', '').replace('Ċ', '\n').
                replace('\u2581', '')
            )

            if not clean_token_str:
                continue

            # Check if all char of the token are autorised
            if all(char in valid_chars for char in clean_token_str):
                valid_tokens.add(token_id)

        while len(current_tokens) < max_tokens:
            # Combined all tokens
            all_token: list[int] = prompt_input_ids + current_tokens

            # Get the logits token
            logits: list[float] = self._model.get_logits_from_input_ids(
                all_token
            )

            # Mask token we don't want
            logits_masked: NDArray[Any] = numpy.full_like(
                logits, -numpy.inf, dtype=float
            )
            for token_id in valid_tokens:
                logits_masked[token_id] = logits[token_id]

            # Select best token
            best_token_id: int = int(numpy.argmax(logits_masked))
            current_tokens.append(best_token_id)

            # Convert token to string
            token_string: str = dict_vocab.get(best_token_id, "")

            # Clear the output
            token_string = (
                token_string.replace('Ġ', '').replace('Ċ', '\n').
                replace('\u2581', '').strip()
            )

            # If token is empty, break the loop
            if not token_string:
                break

            output_to_verify: str = current_output + token_string

            # Validation rules
            is_valid: bool = True

            if output_to_verify.count('.') >= 2:
                is_valid = False

            elif output_to_verify.count('-') >= 2:
                is_valid = False

            elif (output_to_verify.count('-') == 1 and
                  output_to_verify[0] != '-'):
                is_valid = False

            if not is_valid:
                break

            # Add the verified output to the true output
            current_output = output_to_verify

            if self.visualizer:
                print_vizualizer(f'\r{current_output}')

            # Verification: if the number if complete
            try:
                float(current_output)
                if token_string not in valid_chars:
                    break
            except ValueError:
                pass

            # Verification: if '\n' is found, extract and return it
            if '\n' in current_output:
                current_output = current_output.split('\n')[0]
                try:
                    return float(current_output)
                except ValueError:
                    return None

        # Clean the output
        clean_output: str = ""
        for char in current_output:
            if char in ('-0123456789.'):
                clean_output += char

        try:
            return float(clean_output)
        except ValueError:
            return None

    def get_prompt_input_ids(self, prompt: str, output_generation: str,
                             func_param_name: str) -> list[int]:
        # Add the previous output_generation to the prompt and the func
        # parameter name
        new_prompt: str = (
            prompt + f'{output_generation}\n' + f'{func_param_name}='
        )

        # Get prompts token
        prompt_input_ids: list[int] = (
            self._model.encode(new_prompt)[0].tolist()
        )

        return prompt_input_ids
