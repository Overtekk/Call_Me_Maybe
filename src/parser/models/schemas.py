# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  schemas.py                                        :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/29 20:55:21 by roandrie        #+#    #+#               #
#  Updated: 2026/03/29 21:02:28 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from enum import Enum
from pydantic import BaseModel


class JsonFunctionCalling(BaseModel):
    prompt: str


class JsonFunctionDefinition(BaseModel):
    name: str
    description: str
    parameters: dict[str, dict["type", 'Type']]
    returns: dict["type", 'Type']


class Type(Enum):
    NUMBER = "number"
    STRING = "string"
