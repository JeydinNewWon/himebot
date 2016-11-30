import discord

from discord.ext import commands
from utils.check_perms import checks


bot = commands.Bot(command_prefix=commands.when_mentioned_or(".", "hime ", "Hime ", "himebot ", "Himebot "))
bot.remove_command('help')

startup_extensions = ["commands.private", "commands.mod_cmds", "commands.public", "commands.smod_cmds", "commands.music", "utils.errors", "utils.servers"]
        
        
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
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))


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
        await bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
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
        await bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await bot.say("{} reloaded".format(extension_name))

def blog():
    bot.run('token')

blog()
