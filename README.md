# Lutris Cover Art Downloader

This is an **EXTREMELY DIRTY** script to download cover art for Lutris games. With this fork I added an option to download both the cover and the banner at once, as well as two seperate scripts for whether you are using AUR lutris or a Flatpak of lutris, simply to save people time on changing the path directories.

SteamGridDB offers the original Steam covers on their website, however those are unable to be called through their API. If you want the original covers, use it manually.

## Usage

> You will need a SteamGridDB API key. You can get one [here](https://www.steamgriddb.com/profile/preferences/api).

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

## How it works

What the script does is that it fetches the list of games from Lutris at `./.local/share/lutris/pga.db`, then it fetches the first cover art from SteamGridDB. It then saves the cover art in the Lutris cache folder.

## Screenshots

Your library will go from this:

![No covers](https://i.imgur.com/GcyWlHA.png)

To this:

![Covers downloaded](https://i.imgur.com/SWYWqoy.png)

In a matter of seconds.

## Planned features

- Better code
- An icon downloading function
- Rename your games into the exact Steam title(?)

## Credits

- All the credit goes to the original author and contributors to this script.

### Original Credits

- Big thanks to the Lutris team!
- Big thanks to SteamGridDB for their API and their resources!
- Obvious thanks to StackOverflow!
