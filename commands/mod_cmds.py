from utils import check_perms
from discord.ext import commands
import discord

class Mod(object):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @check_perms.check(manage_messages=True)
    async def purge(self, ctx, amount=None, member: discord.Member = None):
        try:
            await self.bot.purge_from(ctx.message.channel, limit=int(amount), before=ctx.message, check=lambda e: member is None or e.author == member)
        except ValueError:
            await self.bot.say('wtf that\'s not an int')
        except TypeError:
            await self.bot.say('did you tag the fgt u wanna purge from?')
        except discord.errors.Forbidden:
            await self.bot.say('no perms')


    @commands.command(pass_context=True)
    @check_perms.check(ban_members=True)
    async def ban(self, ctx, *, member: discord.Member = None):
        """Bans a member from the server.
        In order for this to work, the bot must have Ban Member permissions.
        To use this command you must have Ban Members permission or have the
        Bot Admin role.
        """

        try:
            await self.bot.ban(member)
        except discord.Forbidden:
            await self.bot.say('bot ain\'t got perms yo')
        except discord.HTTPException:
            await self.bot.say('fgt didn\'t get banned')
        except AttributeError:
            await self.bot.say('which fgt to ban??')
        else:
            await self.bot.say('\U0001f44c')


    @commands.command(pass_context=True)
    @check_perms.check(kick_members=True)
    async def kick(self, ctx, *, member: discord.Member = None):
        try:
            await self.bot.kick(member)
        except discord.Forbidden:
            await self.bot.say('bot ain\'t got perms yo')
        except discord.HTTPException:
            await self.bot.say('fgt didn\'t get kicked')
        except AttributeError:
            await self.bot.say('which fgt to kick??')
        else:
            await self.bot.say('\U0001f44c')


def setup(bot):
    bot.add_cog(Mod(bot))