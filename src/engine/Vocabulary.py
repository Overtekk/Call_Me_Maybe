# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  Vocabulary.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/04/13 11:41:33 by roandrie        #+#    #+#               #
#  Updated: 2026/04/16 09:07:23 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Any, Dict, List

import json

from pydantic import BaseModel, Field, PrivateAttr

from src.utils import print_log


class Vocabulary(BaseModel):
    path_file: str = Field(
        description="Path to the vocabulary file"
    )
    debug: bool = Field(
        description="The state of the debug mode",
        default=False
    )

    _vocab_path: str = PrivateAttr()
    _vocab_data: Dict = PrivateAttr()

    def model_post_init(self, context: Any) -> None:
        self.load_vocab(self.path_file)
        return super().model_post_init(context)

    def load_vocab(self, path: str) -> None:
        try:
            with open(path, 'r') as f:
                vocab = json.load(f)

            if self.debug:
                print_log("Vocabulary loaded without problem!")

            self._vocab_data = vocab

        except Exception as e:
            raise ValueError(f"error while loading vocab path {e}")

    def get_id_to_token_vocab(self) -> Dict[int, str]:
        reverse_vocab = {}

        for key, value in self._vocab_data.items():
            reverse_vocab[value] = key

        return reverse_vocab

    def get_valid_token_ids(self, current_output: str,
                            valid_names: List[str]) -> List[int]:
        valid_id = []
        reverse_vocab = self.get_id_to_token_vocab()

        for key, item in reverse_vocab.items():
            candidat = current_output + item

            for name in valid_names:
                if name.startswith(candidat):
                    valid_id.append(key)
                    break

        return valid_id
