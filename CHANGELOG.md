# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project mostly adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html). It didn't adhere to SemVer in the 1.x and 2.x range. Anything between 3.0.0 and 3.5.0 was never released.

## [Unreleased]

## [4.0.1] - 2022-10-19

### Fixed
- Changed the HTTP method of the create_social_account call, as it only takes GET and PUT on the server, but we we're using POST.

## [4.0.0] - 2022-10-01

Refactored the library to support alternative forms of authentication (OAuth soon!)
Whilst the interface is mostly the same, I plan to be adding features in upcoming minor releases.

### Added
- Add aggregations to `trainerdex.api.leaderboard.BaseLeaderboard` and it's children
- `trainerdex.api.leaderboard.Aggregations` class
- `trainerdex.api.leaderboard.CommunityLeaderboard` class
- `trainerdex.api.leaderboard.CountryLeaderboard` class
- Completely rewritten HTTP module!
- Auth framework
- Better type annotations

### Changed
- Moved the entire library from `trainerdex` to `trainerdex.api` to allow other libraries to share the `trainerdex` namespace in future.
- Removed dependency on Discord.py
- Fixed Typo in UserAgent
- Changed domain to `trainerdex.app`
- Removed several unnecessary API calls

### Removed
- Removed PartialUpdate class
- Dropped support for Python 3.7

## [3.6.2] - 2020-10-07
### Changed
- Fix aiohttp import

## [3.6.1] - 2020-09-19
### Added
- Added support for generating leaderboards for stats other than Total XP
- Add aggregations to `trainerdex.leaderboard.GuildLeaderboard`

## [3.5.0] - 2020-08-18
**Notice**: This is a major rewrite to support async python.
### Added
- [`trainerdex.abc.BaseClass`](https://github.com/TrainerDex/TrainerDex.py/blob/3.5.0/trainerdex/abc.py#L6) class
- [`trainerdex.client.Client`](https://github.com/TrainerDex/TrainerDex.py/blob/3.5.0/trainerdex/client.py#L18) class
- [`trainerdex.client.Client.get_trainer`](https://github.com/TrainerDex/TrainerDex.py/blob/3.5.0/trainerdex/client.py#L23) coro -> `trainerdex.trainer.Trainer`
- [`trainerdex.client.Client.create_trainer`](https://github.com/TrainerDex/TrainerDex.py/blob/3.5.0/trainerdex/client.py#L27) coro -> `trainerdex.trainer.Trainer`
- [`trainerdex.client.Client.get_trainers`](https://github.com/TrainerDex/TrainerDex.py/blob/3.5.0/trainerdex/client.py#L64) coro -> `List[trainerdex.trainer.Trainer]`
- [`trainerdex.client.Client.get_user`](https://github.com/TrainerDex/TrainerDex.py/blob/3.5.0/trainerdex/client.py#L72) coro -> `trainerdex.user.User`
- [`trainerdex.client.Client.get_user`](https://github.com/TrainerDex/TrainerDex.py/blob/3.5.0/trainerdex/client.py#L23) coro -> `List[trainerdex.user.User]`
- [`trainerdex.client.Client.get_update`](https://github.com/TrainerDex/TrainerDex.py/blob/3.5.0/trainerdex/client.py#L76) coro -> `trainerdex.update.Update`
- [`trainerdex.client.Client.get_social_connections`](https://github.com/TrainerDex/TrainerDex.py/blob/3.5.0/trainerdex/client.py#L80) coro -> `List[trainerdex.socialconnection.SocialConnection]`
- [`trainerdex.client.Client.get_leaderboard`](https://github.com/TrainerDex/TrainerDex.py/blob/3.5.0/trainerdex/client.py#L86) coro -> `Union[trainerdex.leaderboard.Leaderboard, trainerdex.leaderboard.GuildLeaderboard]`
- [`trainerdex.client.Client.search_trainer`](https://github.com/TrainerDex/TrainerDex.py/blob/3.5.0/trainerdex/client.py#L99) coro -> `trainerdex.trainer.Trainer`
- [`trainerdex.faction.Faction`](https://github.com/TrainerDex/TrainerDex.py/blob/3.5.0/trainerdex/faction.py#L4) class
- [`trainerdex.http.Route`](https://github.com/TrainerDex/TrainerDex.py/blob/3.5.0/trainerdex/http.py#L125) class
- [`trainerdex.http.HTTPClient`](https://github.com/TrainerDex/TrainerDex.py/blob/3.5.0/trainerdex/http.py#L140) class
- [`trainerdex.http.json_or_text`](https://github.com/TrainerDex/TrainerDex.py/blob/3.5.0/trainerdex/http.py#L118) coro
- [`trainerdex.leaderboard.LeaderboardEntry`](https://github.com/TrainerDex/TrainerDex.py/blob/3.5.0/trainerdex/leaderboard.py#L12) class
- [`trainerdex.leaderboard.BaseLeaderboard`](https://github.com/TrainerDex/TrainerDex.py/blob/3.5.0/trainerdex/leaderboard.py#L41) class
- [`trainerdex.leaderboard.Leaderboard`](https://github.com/TrainerDex/TrainerDex.py/blob/3.5.0/trainerdex/leaderboard.py#L145) class
- [`trainerdex.leaderboard.GuildLeaderboard`](hhttps://github.com/TrainerDex/TrainerDex.py/blob/3.5.0/trainerdex/leaderboard.py#L151) class
- [`trainerdex.socialconnection.SocialConnection`](https://github.com/TrainerDex/TrainerDex.py/blob/3.5.0/trainerdex/socialconnection.py#L9) class
- [`trainerdex.update.Level`](https://github.com/TrainerDex/TrainerDex.py/blob/3.5.0/trainerdex/update.py#L15) class
- [`trainerdex.update.get_level`](https://github.com/TrainerDex/TrainerDex.py/blob/3.5.0/trainerdex/update.py#L34) function
- [`trainerdex.update.BaseUpdate`](https://github.com/TrainerDex/TrainerDex.py/blob/3.5.0/trainerdex/update.py#L83) class
- [`trainerdex.update.PartialUpdate`](https://github.com/TrainerDex/TrainerDex.py/blob/3.5.0/trainerdex/update.py#L209) class


### Changed
- Refactored for aiohttp
- Refactored [`trainerdex.trainer.Trainer`](https://github.com/TrainerDex/TrainerDex.py/blob/3.5.0/trainerdex/trainer.py#L16) class
- Refactored [`trainerdex.update.Update`](https://github.com/TrainerDex/TrainerDex.py/blob/3.5.0/trainerdex/update.py#L113) class
- Refactored [`trainerdex.user.User`](https://github.com/TrainerDex/TrainerDex.py/blob/3.5.0/trainerdex/user.py#L9) class

### Removed
- `trainerdex.cached.DiscordUser` class
- `trainerdex.client.Client` has been completely rewritten
- `trainerdex.cached.LevelTuple` namedtuple
- `trainerdex.cached.TeamTuple` namedtuple
- `trainerdex.cached.level_parser` function

## [2.1.3] - 2020-07-22
### Added
- Documented `trainerdex.client.Client.create_user`

### Changed
- Fixed security bug in `trainerdex.cached.DiscordUser` where `_extra_data` was using a literal_eval
- Removed dependency on [`maya`](https://pypi.org/project/maya/) whilst keeping compatibility
- Added `detail` parameter to `trainerdex.client.Client.get_trainer`
- Fix typo on parameter of `trainerdex.leaderboard.DiscordLeaderboard.get_postion`
- Fixed data error on Level 23

## [2.1.1] - 2018-03-27
### Added
- [`trainerdex.leaderboard.LeaderboardInstance`](https://github.com/TrainerDex/TrainerDex.py/blob/2.1.1/trainerdex/leaderboard.py#L5) class
- [`trainerdex.leaderboard.DiscordLeaderboard`](https://github.com/TrainerDex/TrainerDex.py/blob/2.1.1/trainerdex/leaderboard.py#L5) class
- [`trainerdex.leaderboard.WorldwideLeaderboard`](https://github.com/TrainerDex/TrainerDex.py/blob/2.1.1/trainerdex/leaderboard.py#L5) class
- [`trainerdex.client.Client.get_discord_leaderboard`](https://github.com/TrainerDex/TrainerDex.py/blob/2.1.1/trainerdex/client.py#L223) -> `trainerdex.leaderboard.DiscordLeaderboard`
- [`trainerdex.client.Client.get_worldwide_leaderboard`](https://github.com/TrainerDex/TrainerDex.py/blob/2.1.1/trainerdex/client.py#L235) -> `trainerdex.leaderboard.WorldwideLeaderboard`

### Changed
- Add `verified=False` parameter to `trainerdex.client.Client.create_trainer`
- Refactored [`trainerdex.utils.get_team`](https://github.com/TrainerDex/TrainerDex.py/blob/2.1.1/trainerdex/utils.py#L76)
- Fixed data error on Levels 7 and 8

### Removed
- `trainerdex.client.Client.leaderboard`

## [2.0.3] - 2018-01-07
### Changed
- Fixed support for `trainerdex.client.Client.leaderboard(filterset=None)`

## [2.0.2] - 2018-01-06
### Added
- Added `identifier` parameter to `Client` - this is kinda like a UserAgent

## [2.0.1] - 2017-12-21
### Added
- `trainerdex.cached.DiscordUser._extra_data` param
- [`trainerdex.client.Client.discord_to_users`](https://github.com/TrainerDex/TrainerDex.py/blob/2.0.1/trainerdex/client.py#L37) -> `List[trainerdex.user.User]`
- [`trainerdex.client.Client.leaderboard`](https://github.com/TrainerDex/TrainerDex.py/blob/2.0.1/trainerdex/client.py#L45) -> `Dict[str, Union[str, int]]`
- [`trainerdex.utils.TeamTuple`](https://github.com/TrainerDex/TrainerDex.py/blob/2.0.1/trainerdex/utils.py#L9) namedtuple
- [`trainerdex.utils.get_team`](https://github.com/TrainerDex/TrainerDex.py/blob/2.0.1/trainerdex/utils.py#L76) -> `trainerdex.utils.TeamTuple`

### Changed
- Enabled SSL support
- Changed `trainerdex.client.Client.import_discord_user` so that it only takes discord id and trainerdex id
- Renamed `trainerdex.client.Client.get_update` to `trainerdex.client.Client.get_detailed_update` and require user id
- Changed `trainerdex.client.Client.get_discord_user` so you could use uid, user or trainer as params
- Changed API url to `https://trainerdex.app/api/v1/`

### Removed
- `trainerdex.cached.DiscordServer` class
- `trainerdex.cached.refresh_discord` class
- `trainerdex.client.Client.get_teams`
- `trainerdex.client.Client.get_team`
- `trainerdex.client.Client.import_discord_server`
- `trainerdex.client.Client.get_discord_server`
- `trainerdex.client.Client.get_all_discord_users`
- Removed `account` parameter from `trainerdex.client.Client.update_trainer`
- Removed extra stats from `trainerdex.client.Client.create_update`
- Removed extra stats from `trainerdex.update.Update`
- Removed `trainerdex.utils.Team`

## [1.4.3] - 2017-12-12
### Changed
- Fixed a bug when not supplying a `datetime.datetime` to `trainerdex.client.Client.create_update(time_updated=...)`
- Changed API domain to `trainerdex.app`

## [1.4.2] - 2017-11-08
### Added
- [`trainerdex.client.Client.get_users`](https://github.com/TrainerDex/TrainerDex.py/blob/1.4.2/trainerdex/client.py#L72) -> `Set[trainerdex.user.User]`

### Changed
- `trainerdex.cached.DiscordServer.get_users` now uses `trainerdex.client.Client.get_users`
- Explicitly set the parameters on [`trainerdex.client.Client.create_update`](https://github.com/TrainerDex/TrainerDex.py/blob/1.4.0/trainerdex/client.py#L126)
- Fixed a bug where MayaDT will crash if `trainerdex.trainer.Trainer.start_date` is `None` instead of a valid string

## [1.3.4] - 2017-10-29
### Added
- Added `start_date` parameter to `trainerdex.client.create_trainer`
- Added `start_date` parameter to `trainerdex.client.update_trainer`

### Changed
- The `has_cheated` parameter on `trainerdex.client.create_trainer` is now optional
- The `currently_cheats` parameter on `trainerdex.client.create_trainer` is now optional

## [1.3.2] - 2017-10-22
### Added
- Added `respect_privacy` parameter to `trainerdex.client.get_trainer_from_username` to pass-through to `trainerdex.trainer.Trainer`

## [1.3.1] - 2017-10-22
### Changed
- Fixed an issue which caused `Trainer` with `statistics == False` to not init
- Aliased `trainerdex.trainer.Trainer.account` to `trainerdex.trainer.Trainer.owner`

## [1.3.0] - 2017-10-16
### Added
- [`trainerdex.client.Client.get_all_users`](https://github.com/TrainerDex/TrainerDex.py/blob/1.3.0/trainerdex/client.py#L226) -> `List[trainerdex.user.User]`
- [`trainerdex.client.Client.get_all_discord_users`](https://github.com/TrainerDex/TrainerDex.py/blob/1.3.0/trainerdex/client.py#L237) -> `List[trainerdex.cached.DiscordUser]`
- [`trainerdex.cached.DiscordServer.get_users`](https://github.com/TrainerDex/TrainerDex.py/blob/1.3.0/trainerdex/cached.py#L49) -> `Set[trainerdex.user.User]`

### Changed
- Attributes which made another API call are now method. A list is included below:
  - `trainerdex.cached.DiscordUser.owner`
  - `trainerdex.cached.DiscordServer.owner`
  - `trainerdex.trainer.Trainer.team`
  - `trainerdex.trainer.Trainer.owner`
- User objects are now hashable and comparable

### Removed
- `trainerdex.client.DiscordServer.get_trainers`

## [1.2.3] - 2017-10-12
### Changed
- Fixed error preventing a user from being added to the database
- Added function to find the Trainer for an update - likely never to be used but still better than it being blind
- Fixed an error when retrieve a list of trainers from a list of server members
- Fixed an error in which the levels had the wrong value required to finish it
- Fixed an error in which a Trainer would spit out an error trying to calculate the level if there's no Update object (edge case, during creation)

### Removed
- `trainerdex.network.Network` class

## [1.2.2] - 2017-10-11
### Changed
- Fixed a bug which would cause en error when trying to retrieve the Discord ID for a user

## [1.2.1] - 2017-10-11
### Changed
- Various bug fixes
- Improved speed of the library by changing how things are parsed

### Removed
- `trainerdex.cached.DiscordMember` class

## [1.2.0] - 2017-10-08
**Notice**: This should have been a major release, however, I didn't properly understand [SemVer](https://semver.org/spec/v2.0.0.html) in 2017.
### Added
- [`trainerdex.trainer.Trainer`](https://github.com/TrainerDex/TrainerDex.py/blob/1.2.0/trainerdex/trainer.py#L10) class
- [`trainerdex.update.Update`](https://github.com/TrainerDex/TrainerDex.py/blob/1.2.0/trainerdex/update.py#L7) class
- [`trainerdex.user.User`](https://github.com/TrainerDex/TrainerDex.py/blob/1.2.0/trainerdex/user.py#L5) class
- [`trainerdex.utils.LevelTuple`](https://github.com/TrainerDex/TrainerDex.py/blob/1.2.0/trainerdex/utils.py#L6) namedtuple
- [`trainerdex.utils.Level.from_level`](https://github.com/TrainerDex/TrainerDex.py/blob/1.2.0/trainerdex/utils.py#L63) -> `LevelTuple`
- [`trainerdex.utils.Level.from_xp`](https://github.com/TrainerDex/TrainerDex.py/blob/1.2.0/trainerdex/utils.py#L69) -> `LevelTuple`
- [`trainerdex.utils.Team`](https://github.com/TrainerDex/TrainerDex.py/blob/1.2.0/trainerdex/utils.py#L74) class
- [`trainerdex.network.Network`](https://github.com/TrainerDex/TrainerDex.py/blob/1.2.0/trainerdex/network.py#L5) class
- [`trainerdex.http.request_status`](https://github.com/TrainerDex/TrainerDex.py/blob/1.2.0/trainerdex/http.py#L6) -> `str`
- [`trainerdex.cached.DiscordUser`](https://github.com/TrainerDex/TrainerDex.py/blob/1.2.0/trainerdex/cached.py#L7) class
- [`trainerdex.cached.DiscordMember`](https://github.com/TrainerDex/TrainerDex.py/blob/1.2.0/trainerdex/cached.py#L24) class
- [`trainerdex.cached.DiscordServer`](https://github.com/TrainerDex/TrainerDex.py/blob/1.2.0/trainerdex/cached.py#L39) class
- [`trainerdex.cached.refresh_discord.servers`](https://github.com/TrainerDex/TrainerDex.py/blob/1.2.0/trainerdex/cached.py#L92) -> `None`
- [`trainerdex.cached.refresh_discord.users`](https://github.com/TrainerDex/TrainerDex.py/blob/1.2.0/trainerdex/cached.py#L120) -> `None`
- [`trainerdex.client.Client`](https://github.com/TrainerDex/TrainerDex.py/blob/1.2.0/trainerdex/client.py#L13) class
- [`trainerdex.client.Client.get_trainer_from_username`](https://github.com/TrainerDex/TrainerDex.py/blob/1.2.0/trainerdex/client.py#L26) -> `trainerdex.trainer.Trainer`
- [`trainerdex.client.Client.get_teams`](https://github.com/TrainerDex/TrainerDex.py/blob/1.2.0/trainerdex/client.py#L37) -> `List[trainerdex.utils.Team]`
- [`trainerdex.client.Client.create_trainer`](https://github.com/TrainerDex/TrainerDex.py/blob/1.2.0/trainerdex/client.py#L44) -> `trainerdex.trainer.Trainer`
- [`trainerdex.client.Client.update_trainer`](https://github.com/TrainerDex/TrainerDex.py/blob/1.2.0/trainerdex/client.py#L66) -> `trainerdex.trainer.Trainer`
- [`trainerdex.client.Client.create_update`](https://github.com/TrainerDex/TrainerDex.py/blob/1.2.0/trainerdex/client.py#L81) -> `trainerdex.update.Update`
- [`trainerdex.client.Client.import_discord_user`](https://github.com/TrainerDex/TrainerDex.py/blob/1.2.0/trainerdex/client.py#L95) -> `trainerdex.cached.DiscordUser`
- [`trainerdex.client.Client.import_discord_server`](https://github.com/TrainerDex/TrainerDex.py/blob/1.2.0/trainerdex/client.py#L111) -> `trainerdex.cached.DiscordServer`
- [`trainerdex.client.Client.import_discord_server`](https://github.com/TrainerDex/TrainerDex.py/blob/1.2.0/trainerdex/client.py#L130) -> `None`
- [`trainerdex.client.Client.create_user`](https://github.com/TrainerDex/TrainerDex.py/blob/1.2.0/trainerdex/client.py#L144) -> `trainerdex.user.User`
- [`trainerdex.client.Client.update_user`](https://github.com/TrainerDex/TrainerDex.py/blob/1.2.0/trainerdex/client.py#L159) -> `trainerdex.user.User`

### Removed
- `trainerdex.Trainer` namedtuple
- `trainerdex.TrainerList` namedtuple
- `trainerdex.Team` namedtuple
- `trainerdex.Update` namedtuple
- `trainerdex.User` namedtuple
- `trainerdex.DiscordMember` namedtuple
- `trainerdex.Server` namedtuple
- `trainerdex.Level` namedtuple
- `trainerdex.Requests` class

## [1.1.2] - 2017-10-06
### Added
- Added `trainerdex.TrainerList.xp` and `trainerdex.TrainerList.xp_time`

### Changed
- `trainerdex.Requests.token` is now optional
- Fixed a bug in `trainerdex.Requests.listTrainers` which caused the wrong association of a discord user to a trainer

## [1.1.1] - 2017-09-18
### Docs
- Documented `trainerdex.Requests`

### Changed
- Solved an issue in `trainerdex.Requets.patchTrainer` where self was being passed to the payload.

## [1.1.0] - 2017-09-18
### Added
- [`trainerdex.Requests.patchTrainer`](https://github.com/TrainerDex/TrainerDex.py/blob/1.1/TrainerDex.py#L472) -> `int`

### Changed
- Better logging
- Removed `start_date` parameter from `trainerdex.Requests.addTrainer`

## [1.0.0] - 2017-09-16
### Added
- `trainerdex.Trainer` namedtuple
- `trainerdex.TrainerList` namedtuple
- `trainerdex.Team` namedtuple
- `trainerdex.Update` namedtuple
- `trainerdex.User` namedtuple
- `trainerdex.DiscordMember` namedtuple
- `trainerdex.Server` namedtuple
- `trainerdex.Level` namedtuple
- `trainerdex.Requests` class which works as a client.
- [`trainerdex.Requests.getTrainer`](https://github.com/TrainerDex/TrainerDex.py/blob/1.0/TrainerDex.py#L182) -> `trainerdex.Trainer`
- [`trainerdex.Requests.getDiscordUser`](https://github.com/TrainerDex/TrainerDex.py/blob/1.0/TrainerDex.py#L241) -> `trainerdex.DiscordMember`
- [`trainerdex.Requests.listDiscordUsers`](https://github.com/TrainerDex/TrainerDex.py/blob/1.0/TrainerDex.py#L258) -> `List[trainerdex.DiscordMember]`
- [`trainerdex.Requests.listTrainers`](https://github.com/TrainerDex/TrainerDex.py/blob/1.0/TrainerDex.py#L276) -> `List[trainerdex.TrainerList]`
- [`trainerdex.Requests.getTeams`](https://github.com/TrainerDex/TrainerDex.py/blob/1.0/TrainerDex.py#L299) -> `List[trainerdex.Team]`
- [`trainerdex.Requests.getUpdates`](https://github.com/TrainerDex/TrainerDex.py/blob/1.0/TrainerDex.py#L322) -> `List[trainerdex.Update]`
- [`trainerdex.Requests.getUser`](https://github.com/TrainerDex/TrainerDex.py/blob/1.0/TrainerDex.py#L974) -> `trainerdex.User`
- [`trainerdex.Requests.getUserByDiscord`](https://github.com/TrainerDex/TrainerDex.py/blob/1.0/TrainerDex.py#L401) -> `trainerdex.User`
- [`trainerdex.Requests.getServerInfo`](https://github.com/TrainerDex/TrainerDex.py/blob/1.0/TrainerDex.py#L410) -> `trainerdex.Server`
- `trainerdex.Requests.getNetwork` -> `None`
- `trainerdex.Requests.getBanList` -> `None`
- `trainerdex.Requests.getReports` -> `None`
- [`trainerdex.Requests.addTrainer`](https://github.com/TrainerDex/TrainerDex.py/blob/1.0/TrainerDex.py#L436) -> `int`
- [`trainerdex.Requests.addUpdate`](https://github.com/TrainerDex/TrainerDex.py/blob/1.0/TrainerDex.py#L460) -> `int`
- [`trainerdex.Requests.patchDiscordUser`](https://github.com/TrainerDex/TrainerDex.py/blob/1.0/TrainerDex.py#L476) -> `int`
- [`trainerdex.Requests.addDiscordUser`](https://github.com/TrainerDex/TrainerDex.py/blob/1.0/TrainerDex.py#L494) -> `int`
- [`trainerdex.Requests.addDiscordServer`](https://github.com/TrainerDex/TrainerDex.py/blob/1.0/TrainerDex.py#L512) -> `int`
- `trainerdex.Requests.addDiscordMember` -> `None`
- [`trainerdex.Requests.addUserAccount`](https://github.com/TrainerDex/TrainerDex.py/blob/1.0/TrainerDex.py#L544) -> `int`
- [`trainerdex.Requests.patchUserAccount`](https://github.com/TrainerDex/TrainerDex.py/blob/1.0/TrainerDex.py#L561) -> `int`

[Unreleased]: https://github.com/TrainerDex/TrainerDex.py/compare/4.0.0...HEAD
[4.0.0]: https://github.com/TrainerDex/TrainerDex.py/compare/3.6.2...4.0.0
[3.6.2]: https://github.com/TrainerDex/TrainerDex.py/compare/3.6.1...3.6.2
[3.6.1]: https://github.com/TrainerDex/TrainerDex.py/compare/3.5.0...3.6.1
[3.5.0]: https://github.com/TrainerDex/TrainerDex.py/compare/2.1.3...3.5.0
[2.1.3]: https://github.com/TrainerDex/TrainerDex.py/compare/2.1.1...2.1.3
[2.1.1]: https://github.com/TrainerDex/TrainerDex.py/compare/2.0.3...2.1.1
[2.0.3]: https://github.com/TrainerDex/TrainerDex.py/compare/2.0.2...2.0.3
[2.0.2]: https://github.com/TrainerDex/TrainerDex.py/compare/2.0.1...2.0.2
[2.0.1]: https://github.com/TrainerDex/TrainerDex.py/compare/1.4.3...2.0.1
[1.4.3]: https://github.com/TrainerDex/TrainerDex.py/compare/1.4.2...1.4.3
[1.4.2]: https://github.com/TrainerDex/TrainerDex.py/compare/1.3.4...1.4.2
[1.3.4]: https://github.com/TrainerDex/TrainerDex.py/compare/1.3.2...1.3.4
[1.3.2]: https://github.com/TrainerDex/TrainerDex.py/compare/1.3.1...1.3.2
[1.3.1]: https://github.com/TrainerDex/TrainerDex.py/compare/1.3.0...1.3.1
[1.3.0]: https://github.com/TrainerDex/TrainerDex.py/compare/1.2.3...1.3.0
[1.2.3]: https://github.com/TrainerDex/TrainerDex.py/compare/1.2.2...1.2.3
[1.2.2]: https://github.com/TrainerDex/TrainerDex.py/compare/1.2.1...1.2.2
[1.2.1]: https://github.com/TrainerDex/TrainerDex.py/compare/1.2.0...1.2.1
[1.2.0]: https://github.com/TrainerDex/TrainerDex.py/compare/1.1.2...1.2.0
[1.1.2]: https://github.com/TrainerDex/TrainerDex.py/compare/1.1.1...1.1.2
[1.1.1]: https://github.com/TrainerDex/TrainerDex.py/compare/1.1...1.1.1
[1.1.0]: https://github.com/TrainerDex/TrainerDex.py/compare/1.0...1.1
[1.0.0]: https://github.com/TrainerDex/TrainerDex.py/releases/tag/1.0
