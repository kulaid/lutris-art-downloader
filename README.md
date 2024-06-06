# Lutris Cover Art Downloader

This is an **EXTREMELY DIRTY** script to download cover art for Lutris games. 

Forked from https://github.com/vzepec/lutris-art-downloader, I added an option to download both at once, as well as two seperate scripts for whether you are using AUR lutris or a Flatpak of lutris, simply to save people time on changing the path directories.

It comes from a long time bug in Lutris. The source used to get cover arts is... unreliable. It's not a big deal, but it's annoying. So I wrote this script to download the cover arts from SteamGridDB.

SteamGridDB offers the original Steam covers on their website, however those are unable to be called through their API. If you want the original covers, use it manually.

## Usage

1. Clone the repository
```bash
git clone https://github.com/kulaid/lutris-art-downloader
cd lutris-art-downloader/
```

2. Install the dependencies

```bash
pip install -r requirements.txt
```

```bash
yay -S python-inquirer python-requests # If you are on Arch
```

3. Run the script

```bash
python3 flatpak-version.py # Flatpak Script
```

```bash
python3 aur-version.py # AUR Script
```

> You need a SteamGridDB API key. You can get one [here](https://www.steamgriddb.com/profile/preferences/api).

## How it works and warnings

When I said the script dirty, it **IS** dirty. Obvisouly this won't get you any malware, but since I'm not that much into Python, I did what I could.
What the script does is that it fetches the list of games from Lutris at `./.local/share/lutris/pga.db`, then it fetches the first cover art from SteamGridDB. It then saves the cover art in the Lutris cache folder.

## Screenshots

Your library will go from this:

![No covers](https://i.imgur.com/GcyWlHA.png)

To this:

![Covers downloaded](https://i.imgur.com/SWYWqoy.png)

In a matter of seconds.

## Planned features

- Better code
- A better README?

## Credits

- Big thanks to the Lutris team!
- Big thanks to SteamGridDB for their API and their resources!
- Obvious thanks to StackOverflow!
