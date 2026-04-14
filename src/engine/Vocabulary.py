# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  Vocabulary.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/04/13 11:41:33 by roandrie        #+#    #+#               #
#  Updated: 2026/04/14 09:59:02 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Any

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

    def model_post_init(self, context: Any) -> None:
        self._load_vocab(self.path_file)
        return super().model_post_init(context)

    def _load_vocab(self, path: str) -> None:
        try:
            with open(path, 'r') as f:
                vocab = json.load(f)

            if self.debug:
                print_log("Vocabulary loaded without problem!")

            return vocab

        except Exception as e:
            raise ValueError(f"error while loading vocab path {e}")
