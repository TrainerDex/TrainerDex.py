from collections import namedtuple

LevelTuple = namedtuple('LevelTuple', [
	'level',
	'total_xp',
	'xp_required'
])

TeamTuple = namedtuple('TeamTuple', [
	'id',
	'name',
	'colour'
])

def level_parser(xp=None, level=None):
	"""
	Takes either xp OR level and returns the value for the other
	"""
	
	LevelTuple = namedtuple('LevelTuple', ['level','total_xp','xp_required'])
	LevelTuples = [
	LevelTuple(level=1,total_xp=0,xp_required=1000),
	LevelTuple(level=2,total_xp=1000,xp_required=2000),
	LevelTuple(level=3,total_xp=3000,xp_required=3000),
	LevelTuple(level=4,total_xp=6000,xp_required=4000),
	LevelTuple(level=5,total_xp=10000,xp_required=5000),
	LevelTuple(level=6,total_xp=15000,xp_required=6000),
	LevelTuple(level=7,total_xp=18000,xp_required=7000),
	LevelTuple(level=8,total_xp=21000,xp_required=8000),
	LevelTuple(level=9,total_xp=36000,xp_required=9000),
	LevelTuple(level=10,total_xp=45000,xp_required=10000),
	LevelTuple(level=11,total_xp=55000,xp_required=10000),
	LevelTuple(level=12,total_xp=65000,xp_required=10000),
	LevelTuple(level=13,total_xp=75000,xp_required=10000),
	LevelTuple(level=14,total_xp=85000,xp_required=15000),
	LevelTuple(level=15,total_xp=100000,xp_required=20000),
	LevelTuple(level=16,total_xp=120000,xp_required=20000),
	LevelTuple(level=17,total_xp=140000,xp_required=20000),
	LevelTuple(level=18,total_xp=160000,xp_required=25000),
	LevelTuple(level=19,total_xp=185000,xp_required=25000),
	LevelTuple(level=20,total_xp=210000,xp_required=50000),
	LevelTuple(level=21,total_xp=260000,xp_required=75000),
	LevelTuple(level=22,total_xp=335000,xp_required=100000),
	LevelTuple(level=23,total_xp=456000,xp_required=125000),
	LevelTuple(level=24,total_xp=560000,xp_required=150000),
	LevelTuple(level=25,total_xp=710000,xp_required=190000),
	LevelTuple(level=26,total_xp=900000,xp_required=200000),
	LevelTuple(level=27,total_xp=1100000,xp_required=250000),
	LevelTuple(level=28,total_xp=1350000,xp_required=300000),
	LevelTuple(level=29,total_xp=1650000,xp_required=350000),
	LevelTuple(level=30,total_xp=2000000,xp_required=500000),
	LevelTuple(level=31,total_xp=2500000,xp_required=500000),
	LevelTuple(level=32,total_xp=3000000,xp_required=750000),
	LevelTuple(level=33,total_xp=3750000,xp_required=1000000),
	LevelTuple(level=34,total_xp=4750000,xp_required=1250000),
	LevelTuple(level=35,total_xp=6000000,xp_required=1500000),
	LevelTuple(level=36,total_xp=7500000,xp_required=2000000),
	LevelTuple(level=37,total_xp=9500000,xp_required=2500000),
	LevelTuple(level=38,total_xp=12000000,xp_required=3000000),
	LevelTuple(level=39,total_xp=15000000,xp_required=5000000),
	LevelTuple(level=40,total_xp=20000000,xp_required=float("inf"))
	]
	
	if xp and level:
		raise ValueError
	if xp:
		LevelTuples.reverse()
		for level in LevelTuples:
			if level.total_xp <= xp:
				return level
	if level:
		return next((x for x in LevelTuples if x.level == level), None)
	else:
		raise ValueError

def get_team(team):
	return (TeamTuple(id=0, name='Teamless', colour='#929292'),TeamTuple(id=1, name='Mystic', colour='#0005ff'),TeamTuple(id=2, name='Valor', colour='#ff0000'),TeamTuple(id=3, name='Instinct', colour='#fff600'))[team]
