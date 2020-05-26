"""
Official TrainerDex API Wrapper
-------------------------------

A basic wrapper for the TrianerDex API.

:copyright: (c) 2020 JayTurnr
:licence: GNU-GPL3, see LICENSE for more details

"""

__title__ = 'trainerdex'
__author__ = 'JayTurnr'
__licence__ = 'GNU-GPL'
__copyright__ = 'Copyright 2020 JayTurnr'
__version__ = '3.0.0 alpha'

from trainerdex.cached import DiscordUser
from trainerdex.client import Client
from trainerdex.exceptions import *
from trainerdex.http import Route, HTTPClient
from trainerdex.leaderboard import DiscordLeaderboard, WorldwideLeaderboard
from trainerdex.models import Trainer, Update, User
from trainerdex.utils import level_parser, get_team
