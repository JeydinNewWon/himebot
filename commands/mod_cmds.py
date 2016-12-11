import discord

from utils import skid, check
from discord.ext import commands

class Mod(object):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(pass_context=True)		
    @check(create_instant_invite=True)
    async def createinvite(self, ctx):		
        invite = None		
        try:		
            invite = await self.bot.create_invite(ctx.message.server)		
        except discord.errors.Forbidden:		
            await self.bot.say('bot got no perms to create invites in this server')
            return		
        await self.bot.say(invite.url)

    @commands.command(pass_context=True)
    @check(manage_messages=True)
    async def purge(self, ctx):
        params = ctx.message.content.split()
        member = None
        amount = 100

        for i in params:
            if skid.isint(i):
                amount = i

        if len(ctx.message.mentions) > 0:
            member = ctx.message.mentions[0]

        try:
            await self.bot.purge_from(ctx.message.channel, limit=int(amount), before=ctx.message, check=lambda e: member is None or e.author == member)
        except ValueError:
            await self.bot.say('wtf that\'s not an int')
        except TypeError:
            await self.bot.say('did you tag the fgt you wanna purge from?')
        except discord.errors.Forbidden:
            await self.bot.say('bot got no perms')
            
    @commands.command()
    @check(manage_messages=True)
    async def clear(self):
        try:
            await self.bot.say("\0\n"*1000)
        except:
            pass


    @commands.command(pass_context=True)
    @check(ban_members=True)
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
            await self.bot.say('banned this fgt')


    @commands.command(pass_context=True)
    @check(kick_members=True)
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
            await self.bot.say('kicked this fgt')


def setup(bot):
    bot.add_cog(Mod(bot))