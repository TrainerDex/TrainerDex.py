from trainerdex import Level, levels

import pytest

def func(level, stat):
    return list(levels())[level].requirements.get(stat)

options = [
    (40, 'total_xp', 20000000),
    (2, 'total_xp', 1000)
]

@pytest.mark.parametrize("level, stat, expected", options)
def test_answer(level: int, stat: str, expected):
    assert func(level, stat) == expected
