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
__version__ = '3.0.0 alpha'

from trainerdex.client import Client
from trainerdex.trainer import Trainer
from trainerdex.utils import level_parser, get_team
from trainerdex.update import Update
from trainerdex.cached import DiscordUser
from trainerdex.user import User
from trainerdex.leaderboard import DiscordLeaderboard, WorldwideLeaderboard
from trainerdex.exceptions import *
