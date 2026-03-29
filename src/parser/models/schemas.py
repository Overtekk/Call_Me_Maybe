# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  schemas.py                                        :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/29 20:55:21 by roandrie        #+#    #+#               #
#  Updated: 2026/03/29 22:09:39 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Dict

from enum import Enum
from pydantic import BaseModel


class DataType(str, Enum):
    NUMBER = "number"
    STRING = "string"


class TypeInfo(BaseModel):
    type: DataType


class JsonFunctionCalling(BaseModel):
    prompt: str


class JsonFunctionDefinition(BaseModel):
    name: str
    description: str
    parameters: Dict[str, TypeInfo]
    returns: TypeInfo
