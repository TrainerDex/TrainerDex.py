TrainerDex
==========

.. image:: https://badge.fury.io/py/trainerdex.svg
    :target: https://badge.fury.io/py/trainerdex

A python library for interacting with the API of TrainerDex

Installation
------------
::

    pip install trainerdex

Update Notes
------------

2.0.3
^^^^^
Support for blank leaderboard command

2.0.2
^^^^^
* Indentifier for updates

2.0.1
^^^^^
* Rewrite for website upgrade

1.4.3.1
^^^^^^^

* Enabled SSL
* Fixed issue with not supplying a datetime when creating a update

1.4.2
^^^^^
* To suppliment 1.3.4, you can now add medals to the updates. 
* Fixed a bug when start_date is null
* Fixed a major bug
* Replaces 1.4.1 and 1.4.0 which will be removed from PyPi

1.3.4
^^^^^
* Added more fields to update_trainer
* Replaced 1.3.3 which introduced a bug

1.3.2
^^^^^
* Added respect_privacy flag passthrough to get_trainer_by_username

1.3.1
^^^^^
* Fixed an issue which caused Trainers with statistics disabled to not load

1.3.0
^^^^^
* Attributes which made another API call are now methods. For example, `Trainer().owner` is now `Trainer().owner()`
* User objects are now hashable and comparable
* Two new methods have been introduced to Client() - get_all_users and get_all_discord_users

1.2.3
^^^^^
* Fixed error preventing a user from being added to the database
* Added function to find the Trainer for an update - likely never to be used but still better than it being blind
* Fixed an error when retrieving a list of trainers from a list of server members
* Fixed an error in which the levels had the wrong value required to finish it
* Fixed an error in which a Trainer would spit out an error trying to calculate the level if there's no Update object (edge case, during creation)

1.2.2
^^^^^
* Fixed a bug which would cause an error when trying to retrieve the Discord ID for a user
* Minor cleanup of source-code

1.2.1
^^^^^
* Improved speed of the library by changing how things are parsed

1.2.0
^^^^^
* Initial upload to PyPi
* A major rewrite. This should have been called version 2.0.0, but it's too late now.
