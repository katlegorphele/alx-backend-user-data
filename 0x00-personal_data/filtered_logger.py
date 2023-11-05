#!/usr/bin/env python3
"""Filtered logger"""

import logging
import re
from typing import List


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        message = super().format(record)
        return filter_datum(self.fields,
                            self.REDACTION, message, self.SEPARATOR)


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """returns the log message obfuscated
    Args:
        fields:
        redaction:
        message:
        seperator:

    """
    for field in fields:
        message = re.sub(
            f"{field}=.+?{separator}",
            f"{field}={redaction}{separator}", message
        )
    return message


# def get_logger() -> logging.Logger:
#     """returns a logging.Logger object"""
#     logger = logging.getLogger('user_data')
#     logger.setLevel(logging.INFO)
#     logger.propagate = False
#     handler = logging.StreamHandler()
#     formatter = logging.Formatter(
#         f"{'(name)s'}:{'(message)s'}")
#     handler.setFormatter(formatter)
#     logger.addHandler(handler)
#     return logger
