import discord
import asyncio

from discord.ext import commands


bot = commands.Bot(command_prefix=commands.when_mentioned_or(","))
bot.remove_command('help')

# initbot MjI4NzU5MDg4NTkzMzcxMTM3.Ct57pw.4HYJ489ksnxYzk7bzby5BQFM3FA
# himebot MjMyOTE2NTE5NTk0NDkxOTA2.Cwefhg.VLrV35zyIHJo1_Z1oZwOwQFDiDk

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
    if ' '.join(msg.split()[:3]) in ['i am gay', 'im gay', 'i\'m gay']:
        await bot.send_message(ch, 'kys fgt')
        await asyncio.sleep(2)
        await bot.send_message(ch, 'jk')
    if msg.startswith('ayy') and len(msg) == 3:
        await bot.send_message(ch, 'lmao')
    if msg.startswith('wew') and len(msg) == 3:
        await bot.send_message(ch, 'lad')
    await bot.process_commands(message)


def blog():
    bot.run('token')

blog()
