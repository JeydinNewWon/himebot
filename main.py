import discord
import datetime
import time

from discord.ext import commands
from utils import checks, os_execute

bot = commands.Bot(command_prefix=commands.when_mentioned_or(
    ",", "hime ", "Hime ", "himebot ", "Himebot "))
bot.remove_command('help')

startup_extensions = ["commands.private", "commands.mod_cmds",
                      "commands.public", "commands.smod_cmds", "commands.music", "errors", "servers"]
uptime = time.time()


@bot.event
async def on_ready():
    await bot.change_presence(game=discord.Game(name='.help | .invite'))
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
        except ImportError as e:
            print('Failed to load extension {}: {}: {}'.format(extension, e.__class__.__name__, e))


@bot.event
async def on_message(message):
    msg = message.content.lower()
    ch = message.channel

    if message.author == bot.user:
        return
    if msg.split()[0][1:] in dir(bot.cogs['SMod']) + dir(bot.cogs['Private']):
        if msg.split()[0][0] == '.' and msg.split()[0][1:] not in ['e', 'px', 'x']:
            try:
                await bot.delete_message(message)
            except:
                pass
    if msg.startswith('ayy') and len(msg) == 3:
        await bot.send_message(ch, 'lmao')
    if msg.startswith('wew') and len(msg) == 3:
        await bot.send_message(ch, 'lad')
    await bot.process_commands(message)


@bot.command()
@checks()
async def load(extension_name: str):
    """Loads an extension."""
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await bot.say("```py\n{}: {}\n```".format(e.__class__.__name__, e))
        return
    await bot.say("{} loaded.".format(extension_name))


@bot.command()
@checks()
async def unload(extension_name: str):
    """Unloads an extension."""
    bot.unload_extension(extension_name)
    await bot.say("{} unloaded.".format(extension_name))


@bot.command()
@checks()
async def reload(extension_name: str):
    bot.unload_extension(extension_name)
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await bot.say("```py\n{}: {}\n```".format(e.__class__.__name__, e))
        return
    await bot.say("{} reloaded".format(extension_name))


@bot.command()
async def botinfo():
    time_online = str(datetime.timedelta(seconds=int(time.time() - uptime)))
    channels = sum([len(s.channels) for s in bot.servers])
    members = sum([len(s.members) for s in bot.servers])
    server_count = len(bot.servers)
    playing_on = len([bot.cogs['Music'].voice_states[k].current for k in bot.cogs[
                     'Music'].voice_states if bot.cogs['Music'].voice_states[k].current is not None])
    load = await os_execute(None).subproc("cat /proc/loadavg")

    data = discord.Embed(
        description="A multifunctional discord bot made by init0#8366",
        colour=discord.Color(value="16727871"))

    data.add_field(name="Servers that i am in", value=str(server_count))
    data.add_field(name="Uptime", value=time_online)
    data.add_field(name="Channels that i am in", value=channels)
    data.add_field(name="Total users encountered", value=members)
    data.add_field(name="Servers playing music on", value=str(playing_on))
    data.add_field(name="Load (ignore pls, not important)", value=load[:14])

    data.set_author(name="himebot", url="https://himebot.xyz")
    data.set_thumbnail(url=bot.user.avatar_url)

    try:
        await bot.say(embed=data)
    except discord.HTTPException:
        await bot.say("I need to be able to send embedded links")


def blog():
    bot.run('MjI4NzU5MDg4NTkzMzcxMTM3.CzWl8A.JBXVnB3bUFHhV0lD9ODcf94HqjE')

blog()
