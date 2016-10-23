import discord
import requests
import random
import time
import datetime

from discord.ext import commands
from utils import check_perms, formats
from cleverbot import Cleverbot


class Public:
    def __init__(self, bot):
        self.bot = bot
        self.uptime = time.time()

    async def do_removal(self, message, limit, predicate):
        if message.channel.permissions_for(message.author).manage_messages:
            await self.bot.delete_message(message)
            await self.bot.purge_from(message.channel, limit=limit, before=message, check=predicate)
        else:
            await self.bot.say('not enuff perms')

    @commands.command(pass_context=True, command_prefix=commands.when_mentioned_or('.'))
    async def h(self, ctx, message):
        cb = Cleverbot()
        reply = cb.ask(message)
        await self.bot.say(reply)

    @commands.command(pass_context=True)
    async def say(self, ctx, *, msg):
        await self.bot.say(msg)

    @commands.command(pass_context=True)
    async def help(self, ctx):
        await self.bot.send_message(ctx.message.author, '''
General cmds for fgts:
**.help**: returns help command
**.randint *start* *end***: rolls a random number in the specified range, if no numbers are specified, roll a random number between 0 and 100
**.cal expression**: calculates an arithemetical expression
**.botinfo**: tf do u think?
**.invite**: for inviting the bot
**.serverinfo**: returns some info about the server
**.lookup**: lookup an ip
**.h**: have a nice chat with me

Music cmds:
**.summon**: summons bot into the current voice channel.
**.play**: play a song
**.skip**: vote to skip a song
**.volume**: change the volume
**.pause**: pause the song
**.resume**: resume the song
**.stop**: stops the bot from playing anything
**.current**: shows info about the current song


Advanced cmds that need advanced perms:
**.createinvite**: creates an instant invite in the current server
**.ban**: ban a fgt
**.kick**: replace ban with kick^
**.purge amount**: go through **amount** messages and delete it, purging by default goes through or purges 100 msgs if an amount is not given.
**.purge user**: go through 100 messages, if the author of the message is **user**, delete it
**.purge amount user**: go through **amount** messages, if the author of the message is **user**, delete it


Made by hime
            ''')

    @commands.command(pass_context=True)
    async def lookup(self, ctx, ip):
        verify = ip.replace('.', '')
        if verify.isdigit():
            r = requests.get('http://ip-api.com/json/{}'.format(ip), allow_redirects=True)
            country = r.json()['country']
            city = r.json()['city']
            isp = r.json()['isp']
            region = r.json()['region']
            timezone = r.json()['timezone']
            zipcode = r.json()['zip']
            latitude = r.json()['lat']
            longitude = r.json()['lon']
            org = r.json()['org']
            await self.bot.say('''```
Country: {}
City: {}
ISP: {}
Region: {}
Time Zone: {}
Zip Code: {}
Latitude: {}
Longitude: {}
Organization: {}```'''.format(
                    country, city, isp, region, timezone, zipcode, latitude, longitude, org))
        else:
            await self.bot.say("you dumb or wat, is that an ip?")

    @commands.command(pass_context=True)
    async def randint(self, ctx, start: int=0, end: int=100):
        await self.bot.say(random.randint(start, end))

    @commands.command(pass_context=True)
    async def cal(self, ctx, *, exp):
        args = ''.join(exp.split())
        disallowed = ['**', '/0', '-0', '+0']
        allowed = '0123456789\/*-+.() '
        wl_fail = False
        bl_fail = False

        for i in args:
            if i not in allowed:
                wl_fail = True

        for i in disallowed:
            if i in args:
                bl_fail = True

        if wl_fail or bl_fail:
            await self.bot.say('did you just try to eval bomb me u dickhead')
        else:
            try:
                await self.bot.say(eval(args))
            except SyntaxError:
                await self.bot.say('wtf did you enter??')

    @commands.command()
    async def botinfo(self):
        time_online = str(datetime.timedelta(seconds=int(time.time() - self.uptime)))
        channels = sum([len(s.channels) for s in self.bot.servers])
        servers = sum([len(s.members) for s in self.bot.servers])
        await self.bot.say('''
```How many fgts have invited me to their server: {}
How many shitty channels i am connected to: {}
How many shitfaces i've encountered: {}
Time online: {}

beemo halped me ok
github
```
https://github.com/initzx/himebot
'''.format(len(self.bot.servers), channels, servers, time_online))

    @commands.command(pass_context=True)
    async def serverinfo(self, ctx):
        server = ctx.message.server
        channels = [channel for channel in ctx.message.server.channels if channel.type == discord.ChannelType.text]
        vchannels = [channel for channel in ctx.message.server.channels if channel.type != discord.ChannelType.text]
        roles = '  '.join([role.name for role in server.roles if not role.is_everyone])

        serverinfo = [
            ("Server Name", server.name),
            ("Server Owner", server.owner),
            ("Created at", str(server.created_at)[:19]),
            ("Total Members", len(server.members)),
            ("Total Text Channels", len(channels)),
            ("Total Voice Channels", len(vchannels)),
            ("Server Roles", roles)
        ]

        await formats.indented_entry_to_code(self.bot, serverinfo)
        await self.bot.say(server.icon_url)

    @commands.command(pass_context=True)
    @check_perms.check(create_instant_invite=True)
    async def createinvite(self, ctx):
        invite = None
        try:
            invite = await self.bot.create_invite(ctx.message.server)
        except discord.errors.Forbidden:
            await self.bot.say('bot got no perms to create inv in this server')
            return
        await self.bot.say(invite.url)

    @commands.command()
    async def invite(self):
        await self.bot.say('''
Invite me here
https://discordapp.com/oauth2/authorize?client_id=232916519594491906&scope=bot&permissions=536063039

My server
https://discord.gg/b9RCGvk
''')


def setup(bot):
    bot.add_cog(Public(bot))