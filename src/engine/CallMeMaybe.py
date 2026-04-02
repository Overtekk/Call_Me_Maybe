# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  CallMeMaybe.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/31 17:19:16 by roandrie        #+#    #+#               #
#  Updated: 2026/04/02 11:42:32 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import List

from pathlib import Path
from llm_sdk import Small_LLM_Model
from pydantic import BaseModel, Field, PrivateAttr


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
