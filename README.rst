TrainerDex
==========

.. image:: https://badges.gitter.im/TrainerDex/PythonLibrary.svg
    :target: https://gitter.im/TrainerDex/PythonLibrary?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge
.. image:: https://api.codacy.com/project/badge/Grade/69d9bdae805b403291ad42ce3ba0381d
    :target: https://www.codacy.com/app/JayTurnr/TrainerDex.py?utm_source=github.com&utm_medium=referral&utm_content=JayTurnr/TrainerDex.py&utm_campaign=badger)
.. image:: https://travis-ci.org/TrainerDex/TrainerDex.py.svg?branch=master
    :target: https://travis-ci.org/TrainerDex/TrainerDex.py

A python library for interacting with the API of TrainerDex

Installation
------------
::

    pip install trainerdex

Update Notes
------------

1.3.0
^^^^^
* Attributes which made another API call are now methods. For example, `Trainer().owner` is now `Trainer().owner()`
* User objects are now hashable and comparable
* Two new methods have been introduced to Client() - get_all_users and get_all_discord_users

1.2.3
^^^^^
* Fixed error preventing a user from being added to the database
* Added function to find the Trainer for an update - likely never to be used but still better than it being blind
* Fixed an error when retrieveing a list of trainers from a list of server members
* Fixed an error in which the levels had the wrong value required to finish it
* Fixed an error in which a Trainer would spit out an error trying to calculate the level if theres no Update object (edge case, during creation)

1.2.2
^^^^^
* Fixed a bug which would cause en error when trying to retreive the Discord ID for a user
* Minor cleanup of source-code

1.2.1
^^^^^
* Improved speed of the library by changing how things are parsed

1.2.0
^^^^^
* Initial upload to PyPi
* A major rewrite. This should have been called version 2.0.0, but it's too late now.
