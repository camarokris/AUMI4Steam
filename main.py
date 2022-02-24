import warnings
from json import load as jload, dump as jdump
from os.path import join as pjoin, isdir, exists as isfile
from os import getenv as genv, remove as rm
from win32com.client import Dispatch
from shutil import copytree as copydir, rmtree as rmd
from wget import download as getfile
from zipfile import ZipFile
from github import Github
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    from distutils.dir_util import copy_tree as ctree
from PIL import Image
from sys import exit
import winreg
import vdf
import io

appdata = genv('APPDATA')
usrhome = genv('USERPROFILE')
dsktp = pjoin(usrhome,'Desktop')

def yes_or_no(question):
    reply = str(input(question+' (y/n): ')).lower().strip()
    if reply[0] == 'y':
        return True
    if reply[0] == 'n':
        return False
    else:
        return yes_or_no("Uhhhh... please enter ")

def updregioninfo():
    rinfo = jload(open(appdata + '/../localLow/Innersloth/Among Us/regionInfo.json'))
    TranslateName = 0
    for a in range(len(rinfo['Regions'])):
        if rinfo['Regions'][a]['Name'] == "TechDaddy's Private Server":
            return "You already have TechDaddy's Private Server setup in your regions file"
        if rinfo['Regions'][a]['TranslateName'] > TranslateName:
            TranslateName = rinfo['Regions'][a]['TranslateName']
    csrvr = {
            "$type": "DnsRegionInfo, Assembly-CSharp",
            "Fqdn": "au.8-bitdigital.com",
            "DefaultIp": "au.8-bitdigital.com",
            "Port": 22023,
            "UseDtls": False,
            "Name": "TechDaddy's Private Server",
            "TranslateName": 1003
        }
    rinfo['Regions'].append(csrvr)
    with open(appdata + '/../localLow/Innersloth/Among Us/regionInfo.json', 'w') as outfile:
        jdump(rinfo,outfile)
    return "Update complete!"

def getgamver(AUDir):
    ggm = pjoin(AUDir, "Among Us_Data\globalgamemanagers")
    try:
        with open(ggm, "rb") as f:
            byte = f.read()
    except IOError:
        print('Error While Opening the File!')
    string = "public.app-category.games"
    pattern = bytes(string, 'utf-8')
    findex = byte.index(pattern) + len(pattern)
    pattern = bytes('20', 'utf-8')
    ver = byte.find(pattern, int(findex))
    bver = byte[int(ver):int(ver)+10]
    AUVersion = bver.decode('utf-8', 'ignore').replace('\x00','')
    return AUVersion

def regkey_value(path, name="", start_key = None):
    if isinstance(path, str):
        path = path.split("\\")
    if start_key is None:
        start_key = getattr(winreg, path[0])
        return regkey_value(path[1:], name, start_key)
    else:
        subkey = path.pop(0)
    with winreg.OpenKey(start_key, subkey) as handle:
        assert handle
        if path:
            return regkey_value(path, name, handle)
        else:
            desc, i = None, 0
            while not desc or desc[0] != name:
                desc = winreg.EnumValue(handle, i)
                i += 1
            return desc[1]

def get_steamlibrary(steamdir):
    slibfile = pjoin(steamdir, 'steamapps/libraryfolders.vdf')
    if isfile(slibfile) == False:
        print('I am unable to locate your Steam Library folder where Among Us is installed.')
        while True:
            uislib = input('Please enter the path to your Steam Library. i.e. d:\steamlibrary : ')
            if isdir(uislib) == False:
                print('The path you entered is not a valid directory, please try again.')
            else:
                if isfile(pjoin(uislib, 'steamapps\common\Among Us\Among Us.exe')) == True:
                    print('Among Us installation found')
                    return uislib
                else:
                    print('The Steam Library path you entered does not contain Among Us. Make sure you are entering just the path to the Steam Library and NOT the path to Among Us directly.')
    else:
        d = vdf.load(open(slibfile))
        for a in d:
            for b in d[a]:
                if type(d[a][b]) is dict:
                    if 'apps' in d[a][b]:
                        if '945360' in d[a][b]['apps']:
                            aufpath = d[a][b]['path']
                            return aufpath

def createshortcut(path, target, wdir, icon):
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(path)
    shortcut.TargetPath = target
    shortcut.WorkingDirectory = wdir
    shortcut.IconLocation = icon
    shortcut.save()

def getmods(augver, auloc):
    g = Github('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')
    tourepo = g.get_repo('eDonnes124/Town-Of-Us-R')
    tourlv = tourepo.get_latest_release().title
    torrepo = g.get_repo('Eisbison/TheOtherRoles')
    torlv = torrepo.get_latest_release().title
    aumoddir = pjoin(usrhome, 'Desktop/ModdedAmongUs')
    toraudir = pjoin(aumoddir, torlv + '_' + augver)
    touraudir = pjoin(aumoddir, 'Town Of Us Reloaded ' + tourlv + '_' + augver)
    auvbackdir = pjoin(aumoddir, 'Among Us Vanilla ' + augver)
    copydir(auloc, toraudir)
    copydir(auloc, touraudir)
    copydir(auloc, auvbackdir)
    tdrepo = g.get_repo("camarokris/private-stuff")
    print('Downloading the latest version of The Other Roles and modding a copy of Among Us')
    torlatest = 'https://github.com/Eisbison/TheOtherRoles/releases/latest/download/TheOtherRoles.zip'
    torlocal = pjoin(toraudir, 'TheOtherRoles.zip')
    torlogol = pjoin(aumoddir, 'TORLogo.png')
    getfile(torlatest, torlocal)
    with Image.open(io.BytesIO(tdrepo.get_contents("TORLogo.png").decoded_content)) as ima:
        ima.save(torlogol)
    with ZipFile(torlocal, 'r') as tor_ref:
        tor_ref.extractall(toraudir)
    rm(torlocal)
    torimg = Image.open(torlogol)
    torico = pjoin(toraudir, 'tor.ico')
    torimg.save(torico, format = 'ICO')
    rm(torlogol)
    print('Downloading the latest version of Town Of Us Reloaded and modding a copy of Among Us')
    tourlatest = 'https://github.com/eDonnes124/Town-Of-Us-R/releases/latest/download/ToU.' + tourlv + '.zip'
    tourlocal = pjoin(aumoddir, 'ToU.' + tourlv + '.zip')
    tourlogol = pjoin(aumoddir, 'TOURLogo.png')
    getfile(tourlatest, tourlocal)
    with Image.open(io.BytesIO(tdrepo.get_contents("ToURLogo.png").decoded_content)) as imb:
        imb.save(tourlogol)
    with ZipFile(tourlocal, 'r') as tour_ref:
        tour_ref.extractall(aumoddir)
    toured = pjoin(aumoddir, 'ToU ' + tourlv)
    ctree(toured, touraudir)
    rm(tourlocal)
    rmd(toured)
    tourimg = Image.open(tourlogol)
    tourico = pjoin(touraudir, 'tour.ico')
    tourimg.save(tourico, format = 'ICO')
    rm(tourlogol)
    createshortcut(pjoin(aumoddir, torlv + '_' + augver + '.lnk'), pjoin(toraudir, 'Among Us.exe'), toraudir, torico)
    createshortcut(pjoin(aumoddir, 'Town Of Us Reloaded ' + tourlv + '_' + augver + '.lnk'), pjoin(touraudir, 'Among Us.exe'), touraudir, tourico)
    print('Your modded copies of Among Us are located in a folder on your desktop called ModdedAmongUs.')
    print('Here is the path to the folder if you like: ' + aumoddir)


if __name__ == '__main__':
    print("""This is ONLY for use for Among Us installed by Steam and will NOT
work for installations from itch.io, xbox game pass for PC, or Epic
Games. 
---------------------------------------------------------------------
This app will make a copy of your current Among Us installation
and place it on your desktop in a folder called ModdedAmongUs. Your
original copy of the game that is launched by Steam will NOT be 
affected.
---------------------------------------------------------------------
It will also update the regionInfo file to add TechDaddy's Private
Server as an option for you to connect to and this server will work
for both Vanilla and Modded versions of Among Us
---------------------------------------------------------------------""")
    if yes_or_no("Continue?") == False:
        exit(0)
    print("Updating Among Us to have access to TechDaddy's Private Server")
    print(updregioninfo())
    print('---------------------------------------------------------------------')
    steamloc = regkey_value(r"HKEY_CURRENT_USER\Software\Valve\Steam", "SteamPath")
    steamlib = get_steamlibrary(steamloc)
    auloc = pjoin(steamlib, 'steamapps\common\Among Us')
    augver = getgamver(auloc)
    getmods(augver, auloc)
    print('---------------------------------------------------------------------')
    print("""The shortcuts generated for The Other Roles and Town Of Us that have
been placed in the ModdedAmongUs directory can be placed anywhere but do not 
move the ModdedAmongUs directory as that will break the shortcuts. Unless you
know what you are doing of course, then have at it :D""")
    print('---------------------------------------------------------------------')
    input("Press Any Key To Exit")