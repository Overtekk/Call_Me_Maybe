# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  CallMeMaybe.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/31 17:19:16 by roandrie        #+#    #+#               #
#  Updated: 2026/03/31 17:35:35 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from llm_sdk.llm_sdk import Small_LLM_Model
from pydantic import BaseModel, PrivateAttr


class CallMeMaybe(BaseModel):
    _model = Small_LLM_Model = PrivateAttr()
