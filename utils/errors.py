from discord.ext import commands
from cleverbot import Cleverbot
import asyncio

import traceback
import discord

class Errors(object):
    def __init__(self, bot):
        self.bot = bot
        self.instances = {}

    async def on_command_error(self, error, ctx):
        channel = ctx.message.channel
        if isinstance(error, commands.MissingRequiredArgument):
            msg = await self.bot.send_message(channel, 'missing arg(s) dumbfook')
            await asyncio.sleep(3)
            await self.bot.delete_message(msg)
        if isinstance(error, commands.CheckFailure):
            msg = await self.bot.send_message(channel, 'u ain\'t got perms fgt')
            await asyncio.sleep(3)
            await self.bot.delete_message(msg)
        if isinstance(error, commands.BadArgument):
            msg = await self.bot.send_message(channel, 'bad arguments, look at .help for halp')
            await asyncio.sleep(3)
            await self.bot.delete_message(msg)
        if isinstance(error, commands.NoPrivateMessage):
            msg = await self.bot.send_message(channel, "That command is not "
                                             "available in DMs.")
            await asyncio.sleep(3)
            await self.bot.delete_message(msg)

        if isinstance(error, discord.ext.commands.errors.CommandNotFound):
            if ctx.prefix is not '.':
                if ctx.message.author.id not in self.instances.keys():
                    future = self.bot.loop.run_in_executor(None, Cleverbot)
                    self.instances[ctx.message.author.id] = await future

                question = ctx.message.content.lstrip(str(ctx.prefix))
                future = self.bot.loop.run_in_executor(None, self.instances[ctx.message.author.id].ask, question)
                answer = await future
                
                await self.bot.send_message(ctx.message.channel, answer)
                
        for i in self.bot.get_all_channels():
            if i.id == '232190536231026688':
                traceback_msg = "```" + "".join(traceback.format_exception(type(error), error, error.__traceback__))+"```"
                print(traceback_msg)
                await self.bot.send_message(i, traceback_msg)
                await self.bot.send_message(i, 'Origin: {}'.format(ctx.message.server))

def setup(bot):
    bot.add_cog(Errors(bot))