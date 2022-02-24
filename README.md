#Among Us Mod Installer for Steam

##To simplify installing Town of Us or The Other Roles mods for Among US

This is designed to find your Steam Library where Among Us is installed, make a copy of Among Us for backup and modding purposes this way we do not touch your original version. 
It will then go and grab the required files from the GitHub repos for 'The Other Roles' and 'Town of Us' mods for Among Us.
Using the backup copy of Among us it will install both Mods in separate directories and create shorts for you. 

You can clone this and get the python requirements (this was built on Python 3.10) and run the main.py script OR download the exe file in the dist directory and run that. 
Because it was compiled with PyInstaller sometimes Windows will flag it as a virus, this is a known issue with PyInstaller compiled executables. Allow it to run if you are okay and understand. 

If you fork this repo you will need to setup a GitHub personal access token and create a .env file with the entry of "AUMI_GITHUB_TOKEN=" followed by your GitHub Personal Access token in order for main.py to work.