from setuptools import setup

setup(
	name = 'AUMI4Steam',
	version = '0.04',
	packages = ['AUMI4Steam'],
	install_requires = ['vdf', 'wget', 'PyGithub', 'Pillow', 'future', 'python-dotenv', 'setuptools', 'pyinstaller', 'altgraph', 'pefile', 'requests', 'pypiwin32', 'pywin32', 'wheel'],
	url = 'https://github.com/camarokris/AUMI4Steam',
	license = '',
	author = 'Kris Barrantes',
	author_email = 'kris.barrantes@outlook.com',
	description = 'Among Us Mod Installer for Steam'
)
