from collections import namedtuple

TeamTuple = namedtuple('TeamTuple', [
    'id',
    'name',
    'colour'
])

def get_team(team):
    return (TeamTuple(id=0, name='Teamless', colour='#929292'),TeamTuple(id=1, name='Mystic', colour='#0005ff'),TeamTuple(id=2, name='Valor', colour='#ff0000'),TeamTuple(id=3, name='Instinct', colour='#fff600'))[team]
