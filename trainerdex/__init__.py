"""
Official TrainerDex API Wrapper
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A basic wrapper for the TrianerDex API.

:copyright: (c) 2017 JayTurnr
:licence: GNU-GPL3, see LICENSE for more details

"""

__title__ = 'trainerdex'
__author__ = 'JayTurnr'
__licence__ = 'GNU-GPL'
__copyright__ = 'Copyright 2017 JayTurnr'
__version__ = '2.1.0.2'

from .client import Client
from .trainer import Trainer
from .utils import level_parser, get_team
from .update import Update
from .cached import DiscordUser
from .user import User
from .leaderboard import DiscordLeaderboard
