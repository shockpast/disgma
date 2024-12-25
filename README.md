# DisGMA

A sophisticated Discord bot designed for downloading and managing Steam Workshop content through SteamCMD integration.

## Installation

### SteamCMD
1. Download SteamCMD from [Valve's official site](https://developer.valvesoftware.com/wiki/SteamCMD)
2. Extract to your desired location
3. Add SteamCMD location to `.env` in `STEAMCMD_PATH`

### FastGMAD
1. Download the latest release from [FastGMAD repository](https://github.com/WilliamVenner/fastgmad/releases)
2. Extract the executable to your desired location
3. Add FastGMAD location to `.env` in `BINARIES_PATH`

## Requirements

- [Python 3.8+](https://www.python.org/)
- [discord.py](https://discordpy.readthedocs.io/en/stable/)
- [steamcmd](https://developer.valvesoftware.com/wiki/SteamCMD)
- [fastgmad](https://github.com/WilliamVenner/fastgmad)

## Commands

| Command        | Description                             |
|----------------|-----------------------------------------|
| `/sync`        | Synchronizes commands with Discord API  |
| `/download`    | Initiates workshop item download        |
| `/status`      | Shows active download status            |
| `/view`        | Displays specific file content          |
| `/list`        | Shows file structure of downloaded item |
| `/delete`      | Removes specific downloaded item        |
| `/delete_all`  | Purges all downloaded content           |
| `/list_all`    | Displays all downloaded items           |

## Running the Bot

0. Follow the `Installation` steps, and only then follow next steps.

1. Clone the repository
```bash
git clone https://github.com/shockpast/disgma
```

2. Install the required Python packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file and fill it with values from `.env.example`

4. Run the bot:
```bash
python main.py
```