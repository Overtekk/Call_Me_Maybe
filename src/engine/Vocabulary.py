# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  Vocabulary.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/04/13 11:41:33 by roandrie        #+#    #+#               #
#  Updated: 2026/04/13 16:46:27 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from pydantic import BaseModel, Field, PrivateAttr


class Vocabulary(BaseModel):
    visualizer: bool = Field(
        description="The state of the visualizer",
        default=False
    )
    debug: bool = Field(
        description="The state of the debug mode",
        default=False
    )

    _vocab_path: str = PrivateAttr()
