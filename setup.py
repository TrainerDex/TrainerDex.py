import re
from setuptools import setup

with open('README.md') as f:
	readme = f.read()

with open('trainerdex/__init__.py') as f:
	version = re.search(r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read()).group(1)
	
with open('requirements.txt') as f:
	requirements = f.read().splitlines()

setup(
	name='trainerdex',
	version=version,
	description='An API to interact with TrainerDex - a online database of Pokemon Go trainers',
	long_description=readme,
	author='JayTurnr',
	author_email='jaynicholasturner@gmail.com',
	url='https://github.com/TrainerDex/TrainerDex.py',
	license='GPL-3.0',
	classifiers=[
		'Intended Audience :: Developers',
		'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
		'Natural Language :: English',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
		'Programming Language :: Python :: 3.8',
		'Topic :: Database',
		'Topic :: Games/Entertainment'
		],
	keywords='pokemon pokemongo trainer trainerdex',
	packages=['trainerdex'],
	zip_safe=True,
	install_requires=requirements,
)
