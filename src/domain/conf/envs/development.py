# coding utf-8

import logging

from ...entities import IConfEnv


class DevConfEnv(IConfEnv):
    logging_level: int = logging.DEBUG
