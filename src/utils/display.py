# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  display.py                                        :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/27 09:46:37 by roandrie        #+#    #+#               #
#  Updated: 2026/03/27 11:04:37 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #
"""Terminal output management utilities.

This module provides a centralized interface for displaying formatted
messages using the Rich library. It manages distinct output streams
(stdout and stderr) to ensure that logs and errors do not interfere with
potential structured outputs.

Attributes:
    standard_console (Console): The default console instance for standard
                                output.
    error_console (Console): A console instance configured specifically for
                             stderr.
"""

from rich.console import Console


standard_console = Console()
error_console = Console(stderr=True)


def print_error(message: str) -> None:
    """
    Displays a formatted error message on the standard error stream.

    Args:
        message (str): The specific error description to be displayed.
    """
    prefix = "Error: "
    content = f"{message}"
    error_console.print(f"[bold red]{prefix + content}[/bold red]")
