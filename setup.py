from setuptools import setup

setup(
	name = 'AUMI4Steam',
	version = '0.01',
	packages = ['AUMI4Steam'],
	install_requires = ['vdf', 'wget', 'PyGithub', 'Pillow'],
	url = 'https://github.com/camarokris/AUMI4Steam',
	license = '',
	author = 'Kris Barrantes',
	author_email = 'kris.barrantes@outlook.com',
	description = 'Among Us Mod Installer for Steam'
)
