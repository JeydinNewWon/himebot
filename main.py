import discord
from discord.ext import commands
import asyncio
import traceback


bot = commands.Bot(command_prefix='.')
bot.remove_command('help')

# 205346839082303488 id

startup_extensions = ["commands.mod_cmds", "commands.public"]

@bot.event
async def on_ready():
    await bot.change_status(game=discord.Game(name='.help'))
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
async def on_message(ctx):
    msg = ctx.content
    ch = ctx.channel

    if ctx.author == bot.user:
        return

    if ' '.join(msg.split()[:3]).lower() in ['i am gay', 'im gay', 'i\'m gay']:
        print('works')
        print(ctx.channel)
        await bot.send_message(ch, 'kys fgt')
        await asyncio.sleep(2)
        await bot.send_message(ch, 'jk')
    if msg.startswith('ayy' ):
        await bot.send_message(ch, 'lmao')

    if ctx.channel.is_private:
        print('Private Message:', str(ctx.timestamp)[:16], ctx.author, ctx.content)
        print()
    else:
        print('Public Message:', str(ctx.timestamp)[:16],
              ctx.server.name + ':' + ch.name, ctx.author, ctx.content)
        print()

    await bot.process_commands(ctx)


@bot.event
async def on_command_error(error, ctx):
    channel = ctx.message.channel
    if ctx.message.content.startswith('.s'):
        await bot.delete_message(ctx.message)
        return
    if isinstance(error, commands.MissingRequiredArgument):
        msg = await bot.send_message(channel, 'missing arg(s) dumbfook')
        await asyncio.sleep(3)
        await bot.delete_message(msg)
    if isinstance(error, commands.CheckFailure):
        msg = await bot.send_message(channel, 'u ain\'t got perms fgt')
        await asyncio.sleep(3)
        await bot.delete_message(msg)
    if isinstance(error, commands.BadArgument):
        msg = await bot.send_message(channel, 'bad arguments, look at .help for halp')
        await asyncio.sleep(3)
        await bot.delete_message(msg)
    if isinstance(error, commands.NoPrivateMessage):
        msg = await bot.send_message(channel, "That command is not "
                                         "available in DMs.")
        await asyncio.sleep(3)
        await bot.delete_message(msg)
    for i in bot.get_all_channels():
        if i.id == '232190536231026688':
            traceback_msg = "```" + "".join(traceback.format_exception(type(error), error, error.__traceback__))+"```"
            await bot.send_message(i, traceback_msg)
            await bot.send_message(i, 'Origin: {}'.format(ctx.message.server))

def blog():
    print('Connected')
    bot.run('token')
    bot.change_status(game='help')

blog()
