import dotenv
dotenv.load_dotenv()

import discord
from discord import app_commands

import time
import os
import platform
import asyncio
from threading import Thread

import utils
import json

### env
steamcmd_path = os.getenv("STEAMCMD_PATH")
binaries_path = os.getenv("BINARIES_PATH")
data_path = os.getenv("DATA_PATH")

app_id = os.getenv('STEAMCMD_APPID')
item_id = os.getenv('STEAMCMD_ITEMID')

discord_token = os.getenv("DISCORD_TOKEN")
###

### vars
os_type = "linux" if platform.system() == "Linux" else "windows"
executable_type = ".exe" if os_type == "windows" else ""

steamcmd = steamcmd_path + "/steamcmd.exe"
workshop = steamcmd_path + f"/steamapps/workshop/content/{os.getenv('STEAMCMD_APPID')}"
###

### worker
active_downloads = {}
###

### discord
intents = discord.Intents.default()

bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)
###

async def download_worker(user_id: int, item_id: int, interaction: discord.Interaction):
  try:
    start = time.time()

    process = await asyncio.create_subprocess_shell(
      f"{steamcmd} +login anonymous +workshop_download_item {app_id} {item_id} +quit",
      stdout=asyncio.subprocess.DEVNULL,
      stderr=asyncio.subprocess.DEVNULL
    )
    await process.wait()

    if not os.path.exists("./data/"):
      return await interaction.channel.send("`data` directory not found")
    if not os.path.exists(f"./binaries/{os_type}/fastgmad{executable_type}"):
      return await interaction.channel.send("`fastgmad` binary not found")

    os.makedirs(f"{data_path}/{item_id}", exist_ok=True)

    gma_files = [f for f in os.listdir(f"{workshop}/{item_id}") if f.endswith('.gma')]
    if not gma_files:
      return await interaction.channel.send(f"no `.gma` files found for item `{item_id}`")

    extract_process = await asyncio.create_subprocess_shell(
      f"{binaries_path}/{os_type}/fastgmad{executable_type} extract "
      f"-file {workshop}/{item_id}/{gma_files[0]} "
      f"-out {data_path}/{item_id}",
      stdout=asyncio.subprocess.DEVNULL,
      stderr=asyncio.subprocess.DEVNULL
    )
    await extract_process.wait()

    end_time = time.time()
    await interaction.channel.send(f"download and extraction completed for item `{item_id}` in `{end_time - start:.2f}` seconds")

  except Exception as e:
    print(f"[ disgma ] error: {e}")
    await interaction.channel.send(f"an error occurred while downloading the item with ID: `{item_id}`")
  finally:
    active_downloads.pop(user_id, None)

###
@bot.event
async def on_ready():
  try:
    print(f"[ disgma ] logged in as {bot.user}")
  except Exception as e:
    print(f"[ disgma ] error during syncing: {e}")

@tree.command(
  name = "sync",
  description = "Sync the commands with the Discord API",
)
async def sync(interaction: discord.Interaction):
  if interaction.user.id != 468359358586159105:
    return await interaction.response.send_message("you don't have permission to run this command", ephemeral=True)

  try:
    await tree.sync()
    await interaction.response.send_message("commands synced successfully", ephemeral=True)
  except Exception as e:
    await interaction.response.send_message(f"an error occurred while syncing commands: {e}", ephemeral=True)

@tree.command(
  name="download",
  description="Download an item by its ID"
)
@app_commands.describe(item_id="The ID of the item to download")
async def download(interaction: discord.Interaction, item_id: int):
  user_id = interaction.user.id

  if user_id in active_downloads:
    return await interaction.response.send_message("you already have an active download in progress", ephemeral=True)

  active_downloads[user_id] = item_id

  await interaction.response.send_message(f"started downloading item `{item_id}`\nyou will be notified when it's done", ephemeral=True)
  Thread(target=lambda: asyncio.run_coroutine_threadsafe(download_worker(user_id, item_id, interaction), bot.loop)).start()

@tree.command(
  name="status",
  description="Check the status of the active downloads"
)
async def status(interaction: discord.Interaction):
  user_id = interaction.user.id

  if user_id not in active_downloads:
    return await interaction.response.send_message("you don't have any active downloads", ephemeral=True)

  await interaction.response.send_message(f"your active download is for item `{active_downloads[user_id]}`", ephemeral=True)

@tree.command(
  name="view",
  description="View file from download"
)
@app_commands.describe(item_id="The ID of the item to view")
@app_commands.describe(file_name="The name of the file to view")
async def view(interaction: discord.Interaction, item_id: int, file_name: str):
  if not os.path.exists(f"{data_path}/{item_id}/{os.path.normpath(file_name)}"):
    return await interaction.response.send_message("the file you requested does not exist.", ephemeral=True)

  with open(f"{data_path}/{item_id}/{os.path.normpath(file_name)}", "rb") as f:
    await interaction.response.send_message(file=discord.File(f, file_name))

@tree.command(
  name="list",
  description="List files from download"
)
@app_commands.describe(item_id="The ID of the item to list")
async def list(interaction: discord.Interaction, item_id: int):
  if not os.path.exists(f"{data_path}/{item_id}"):
    return await interaction.response.send_message("the item you requested does not exist", ephemeral=True)

  tree_output = utils.generate_tree(f"{data_path}/{item_id}")
  if not tree_output:
    return await interaction.response.send_message("no files found for this item", ephemeral=True)

  tree_text = "\n".join(tree_output)
  if len(tree_text) > 1990:
    with open(f"{data_path}/{item_id}/file_list.txt", "w", encoding="utf-8") as f:
      f.write(tree_text)

    await interaction.response.send_message(file=discord.File(f"{data_path}/{item_id}/file_list.txt"))
    os.remove(f"{data_path}/{item_id}/file_list.txt")
  else:
    await interaction.response.send_message(f"```\n{tree_text}\n```")

@tree.command(
  name="delete",
  description="Delete item download"
)
@app_commands.describe(item_id="The ID of the item to delete")
async def delete(interaction: discord.Interaction, item_id: int):
  if not os.path.exists(f"{data_path}/{item_id}"):
    return await interaction.response.send_message("the item you requested does not exist", ephemeral=True)

  for root, dirs, files in os.walk(f"{data_path}/{item_id}", topdown=False):
    for name in files:
      os.remove(os.path.join(root, name))
    for name in dirs:
      os.rmdir(os.path.join(root, name))

  os.rmdir(f"{data_path}/{item_id}")

  await interaction.response.send_message(f"item `{item_id}` has been deleted", ephemeral=True)

@tree.command(
  name="delete_all",
  description="Delete all items"
)
async def delete_all(interaction: discord.Interaction):
  if interaction.user.id != 468359358586159105:
    return await interaction.response.send_message("you don't have permission to run this command", ephemeral=True)

  for root, dirs, files in os.walk(data_path, topdown=False):
    for name in files:
      os.remove(os.path.join(root, name))
    for name in dirs:
      os.rmdir(os.path.join(root, name))

  await interaction.response.send_message("all items have been deleted", ephemeral=True)

@tree.command(
  name="list_all",
  description="List all downloaded items"
)
async def list_all(interaction: discord.Interaction):
  if not os.path.exists(data_path):
    return await interaction.response.send_message("no items have been downloaded yet", ephemeral=True)

  items = [d for d in os.listdir(data_path) if os.path.isdir(os.path.join(data_path, d))]
  if not items:
    return await interaction.response.send_message("no items have been downloaded yet", ephemeral=True)

  item_details = []
  for item in sorted(items):
    addon_path = os.path.join(data_path, item, "addon.json")
    if os.path.exists(addon_path):
      try:
        with open(addon_path, 'r', encoding='utf-8') as f:
          addon_data = json.load(f)
          title = addon_data.get('title', 'Unknown')
          item_details.append(f"{item}: {title}")
      except:
        item_details.append(f"{item}: <error reading addon.json>")
    else:
      item_details.append(f"{item}: <no addon.json found>")

  items_text = "\n".join(item_details)
  await interaction.response.send_message(f"```\n{items_text}\n```", ephemeral=True)

###
bot.run(token=discord_token)