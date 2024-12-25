# DisGMA

A sophisticated Discord bot designed for downloading and managing Steam Workshop content through SteamCMD integration.

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