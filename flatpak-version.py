# Import necessary modules
import requests, sqlite3, os, inquirer, base64
from os import remove, path

# Vars
user = ''
dbpath = ''
dim = ''
auth = ''
selectedpath = ''

# Main function
def main():
    global user, auth, dbpath, bannerpath, coverpath, dim
    user = GetUser()
    print("Welcome " + user + " to Lutris Cover Art Downloader!\n")
    auth = GetAPIKey()
    print("Getting API Key...\n")
    if auth == '':
        auth = SetAPIKey()
    dbpath = '/home/' + user + '/.var/app/net.lutris.Lutris/data/lutris/pga.db/'
    bannerpath = '/home/' + user + '/.var/app/net.lutris.Lutris/cache/lutris/banners/'
    coverpath = '/home/' + user + '/.var/app/net.lutris.Lutris/cache/lutris/coverart/'
    dim = GetDimType()
    co = DBConnect()
    GetGamesList(co)
    CleanNotInstalledGames(co)


####### FUNCTIONS
def GetUser():
    try:
        return os.getlogin()
    except:
        print("Could not get session username")
        exit(1)

def GetAPIKey():
    if os.path.isfile('./apikey.txt'):
        with open('./apikey.txt', 'r') as f:
            key = f.read()
            auth = {'Authorization': 'Bearer ' + key}
            return auth
    else:
        return ''


def SetAPIKey():
    print("Could not find API key")
    print('You need a SteamGriDB API key to use this script.')
    print('You can get one by using your Steam account and heading here: https://www.steamgriddb.com/profile/preferences/api\n')
    api = input("Enter your SteamGridDB API key: ")
    auth = {'Authorization': 'Bearer ' + api}
    TestAPI(auth, api)
    return api

def SaveAPIKey(key):
    with open('./apikey.txt', 'w') as f:
        f.write(key)

def TestAPI(key, api):
    r = requests.get('https://www.steamgriddb.com/api/v2/grids/game/1?dimensions=600x900', headers=key)
    if r.status_code == 200:
        print("API key is valid, saving...")
        SaveAPIKey(api)
    else:
        print("API key is invalid")
        exit(1)

#Get list of installed games
def CleanNotInstalledGames(co):
    c = co.execute('SELECT slug FROM games WHERE installed = "1"')
    games = c.fetchall()
    listgames = []
    for entry in games:
        title = entry[0] + '.jpg'
        listgames.append(title.lower())
    DeleteImages(listgames)


#Delete covers/banners for not installed games
def DeleteImages(listgames):
    for path in [bannerpath, coverpath]:
        for filename in os.listdir(path):
            if filename.lower() not in listgames and os.path.isfile(os.path.join(path, filename)):
                if filename.lower().endswith('.jpg'):
                    os.remove(os.path.join(path, filename))


def GetDimType():
    global selectedpath, dim
    questions = [
    inquirer.List('type',
                    message="Would you like to download banners, covers, or both?",
                    choices=['Banner (460x215)', 'Cover (600x900)', 'Both'],
                ),
    ]
    ans = inquirer.prompt(questions)["type"]
    print('Cover type set to ' + ans + '\n')
    if ans == 'Banner (460x215)':
        selectedpath = bannerpath
        dim = '460x215'
    elif ans == 'Cover (600x900)':
        selectedpath = coverpath
        dim = '600x900'
    else:
        selectedpath = [bannerpath, coverpath]
        dim = ['460x215', '600x900']
    return dim


def SaveAPIKey(key):
    with open('./apikey.txt', 'w') as f:
        f.write(key)


def TestAPI(key, api):
    r = requests.get('https://www.steamgriddb.com/api/v2/grids/game/1?dimensions=600x900', headers=key)
    if r.status_code == 200:
        print("API key is valid, saving...")
        SaveAPIKey(api)
    else:
        print("API key is invalid")
        exit(1)


def DBConnect():
    try:
        conn = sqlite3.connect(dbpath)
    except:
        print("Could not find Lutris database 'pga.db'. You can manually edit script's path if necessary")
        exit(1)
    return conn


# Search for a game by name via Lutris database, then get the grid data
def SearchGame(game):
    res = requests.get('https://www.steamgriddb.com/api/v2/search/autocomplete/' + game, headers=auth).json()
    if len(res["data"]) == 0:
        print("Could not find artwork for " + game)
    else:
        print("Found " + game.replace('-', ' ').title())
        id = res["data"][0]["id"]
        return id


# Download cover by searching for the game via its name, then via its SteamGriDB's ID
def DownloadArt(name):
    gameid = SearchGame(name)
    if isinstance(dim, list):
        for i in range(len(dim)):
            if dim[i] == "460x215":
                print("Downloading banner for " + name.replace('-', ' ').title())
            else:
                print("Downloading cover for " + name.replace('-', ' ').title())
            grids = requests.get('https://www.steamgriddb.com/api/v2/grids/game/' + str(gameid) + '?dimensions=' + dim[i], headers=auth).json()
            try:
                url = grids["data"][0]["url"]
            except:
                print("Could not find a cover for game " + name)
                return
            r = requests.get(url)
            os.makedirs(selectedpath[i], exist_ok=True)  # Ensure the directory exists
            with open(selectedpath[i] + name + '.jpg', 'wb') as f:
                f.write(r.content)
    else:
        for i in range(len(dim)):
            grids = requests.get('https://www.steamgriddb.com/api/v2/grids/game/' + str(gameid) + '?dimensions=' + dim, headers=auth).json()
            try:
                url = grids["data"][0]["url"]
            except:
                if dim[i] == "Banner":
                    print("Could not find a banner for " + name)
                else:
                    print("Could not find a cover for " + name)
                return
            r = requests.get(url)
            with open(selectedpath + name + '.jpg', 'wb') as f:
                f.write(r.content)


# Get all games and for each game, check if it already has a cover
def GetGamesList(co):
    c = co.execute('SELECT slug FROM games WHERE installed = "1"')
    games = c.fetchall()
    for entry in games:
        title = entry[0]
        if isinstance(selectedpath, list):
            for path in selectedpath:
                if not os.path.isfile(path + title + '.jpg'):
                    DownloadArt(title)
                else:
                    if path == bannerpath:
                        print("Banner for " + title.replace('-', ' ').title() + " already exists")
                    else:
                        print("Cover for " + title.replace('-', ' ').title() + " already exists")
        else:
            if not os.path.isfile(selectedpath + title + '.jpg'):
                DownloadArt(title)
            else:
                if dim == "460x215":
                    print("Banner for " + title.replace('-', ' ').title() + " already exists")
                else:
                    print("Cover for " + title.replace('-', ' ').title() + " already exists")
    print('All done ! Restart Lutris for the changes to take effect')


if __name__ == '__main__':
    main()
