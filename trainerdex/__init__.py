# -*- coding: utf-8 -*-

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
__version__ = '1.4.3.1'

from .client import Client
from .trainer import Trainer
from .utils import Level, Team
from .update import Update
from .cached import DiscordUser, DiscordServer, refresh_discord
from .user import User