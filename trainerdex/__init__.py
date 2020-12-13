"""
Official TrainerDex API Wrapper
-------------------------------

A basic wrapper for the TrainerDex API.

:copyright: (c) 2020 TurnrDev
:licence: GNU-GPL3, see LICENSE for more details

"""

__title__ = "trainerdex"
__author__ = "JayTurnr"
__licence__ = "GNU-GPL"
__copyright__ = "Copyright 2020 TurnrDev"
__version__ = "3.7.0a1"

from .client import Client
from .faction import Faction
from .http import HTTPClient, Route
from .leaderboard import GuildLeaderboard, Leaderboard
from .socialconnection import SocialConnection
from .trainer import Trainer
from .update import Level, Update
from .user import User
