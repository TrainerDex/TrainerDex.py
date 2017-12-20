import re
from setuptools import setup

def readme():
	with open('README.rst') as f:
		return f.read()

version = ''
with open('trainerdex/__init__.py') as f:
	version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

if not version:
	raise RuntimeError('version is not set')

setup(
	name='trainerdex',
	version=version,
	description='An API to interact with TrainerDex - a online database of Pokemon Go trainers.',
	long_description=readme(),
	author='JayTurnr',
	author_email='jaynicholasturner@gmail.com',
	url='https://github.com/TrainerDex/TrainerDex.py',
	license='GPL-3.0',
	classifiers=[
		'Development Status :: 4 - Beta',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
		'Natural Language :: English',
		'Programming Language :: Python :: 2.6',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3.2',
		'Programming Language :: Python :: 3.3',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
		'Topic :: Database',
		'Topic :: Games/Entertainment'
		],
	keywords='pokemon pokemongo trainer',
	packages=['trainerdex'],
	zip_safe=True,
	install_requires=[
		'maya==0.3.3',
		'requests==2.18.4',
	],
)
