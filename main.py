import pyfiglet
import os, random
import discord
from discord.ext import commands
import time
from colorama import Fore, Style

class colors:
  def banner(txt):
    print(f"{Fore.LIGHTMAGENTA_EX}{Style.BRIGHT}{txt}{Fore.RESET}{Style.NORMAL}")

  def error(txt):
    print(f"{Fore.RED}[{random.choice(['-', '!'])}]{Fore.RESET}{Style.DIM} {txt}{Fore.RESET}{Style.NORMAL}")

  def success(txt):
    print(f"{Fore.GREEN}[+]{Fore.RESET}{Style.BRIGHT} {txt}{Fore.RESET}{Style.NORMAL}")

  def warning(txt):
    print(f"{Fore.LIGHTYELLOW_EX}[!]{Fore.RESET}{Style.DIM} {txt}{Fore.RESET}{Style.NORMAL}")

banner = pyfiglet.figlet_format("Cloner")
colors.banner(banner)
colors.warning("\x1B[3mhttps://t.me/idkconsole\x1B[0m\n")

colors.warning("Token")
token = input()
client = commands.Bot(command_prefix=".", case_insensitive=True,
                      self_bot=True)

client.remove_command('help')
header = {"Authorization": f'Bot {token}'}
os.system('cls' if os.name == 'nt' else 'clear')
intents = discord.Intents.all()
intents.members = True

@client.event
async def on_ready():
    target_guild_id = int(input("Enter the guild ID which you want to copy: "))
    paste_guild_id = int(input("Enter the guild ID where you want to paste it: "))
    source_guild = client.get_guild(target_guild_id)
    if not source_guild:
        print(f"Error | Source guild (ID: {target_guild_id}) not found!")
        return
    target_guild = client.get_guild(paste_guild_id)
    if not target_guild:
        print(f"Error | Target guild (ID: {paste_guild_id}) not found!")
        return
    for c in target_guild.channels:
        try:
            await c.delete()
            colors.success(f"INFO | Deleted Channel {c.name}")
            time.sleep(3)
        except Exception as e:
            print(f"Error deleting channel {c.name}: {e}")
    for cate in source_guild.categories:
        x = await target_guild.create_category(cate.name)
        for chann in cate.channels:
            try:
                if isinstance(chann, discord.VoiceChannel):
                    await x.create_voice_channel(chann.name)
                elif isinstance(chann, discord.TextChannel):
                    await x.create_text_channel(chann.name, overwrites=chann.overwrites, topic=chann.topic, slowmode_delay=chann.slowmode_delay, nsfw=chann.nsfw, position=chann.position)
                time.sleep(5)
            except Exception as e:
               colors.success(f"Error creating channel {chann.name}: {e}")
    for role in target_guild.roles:
        if role.name != "@everyone":
            try:
                await role.delete()
                colors.success(f"INFO | Deleted Role {role.name}")
                time.sleep(5)
            except Exception as e:
                print(f"Couldn't delete role {role.name}: {e}")
    for role in source_guild.roles[::-1]:
        if role.name != "@everyone":
            try:
                await target_guild.create_role(name=role.name, color=role.color, permissions=role.permissions, hoist=role.hoist, mentionable=role.mentionable)
                colors.success(f"INFO | Created Role {role.name}")
                time.sleep(3)
            except Exception as e:
                print(f"Couldn't create role {role.name}: {e}")
              
client.run(token, bot=False)
