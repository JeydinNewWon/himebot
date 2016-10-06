import discord
from discord.ext import commands
import requests
import random
import datetime
import time


def isint(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


class Public:
    def __init__(self, bot):
        self.bot = bot
        self.uptime = time.time()

    @commands.command(pass_context=True)
    async def test(self, ctx):
        for i in self.bot.servers:
            await self.bot.say(i.name)

    @commands.command()
    async def help(self):
        await self.bot.say('''
General cmds for fgts:
**.help**: returns help command
**.randint start end**: rolls a random number in the specified range
**.cal expression**: calculates an arithemetical expression
**.botinfo**: tf do u think?

Advanced cmds that need advanced perms:
**.ban**: ban a fgt (bot need perms, and u need perms aswell)
**.kick**: replace ban with kick^
**.purge amount**: go through that amount of messages and delete it.
**.purge amount user**: go through that amount of messages, if the author of the message is user, delete it.
**.serverinfo**: returns some info about the server.


Made by init0
            ''')

    @commands.command(pass_context=True)
    async def lookup(self, ctx):
        ip = ctx.message.content[8:]
        print(ip)
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
    async def randint(self, ctx):
        msg = ctx.message.content.split()
        if len(msg) == 3:
            if isint(msg[1]) and isint(msg[2]):
                await self.bot.say(random.randint(int(msg[1]), int(msg[2])))
            else:
                await self.bot.say('are those ints?!')
        else:
            await self.bot.say('you need a start and an end integer dumbfook')

    @commands.command(pass_context=True)
    async def cal(self, ctx):
        msg = ctx.message.content.split()
        args = ''.join(ctx.message.content.split()[1:])
        disallowed = ['**', '/0', '-0', '+0']
        allowed = '0123456789\/*-+.() '
        wl_fail = False
        bl_fail = False

        if len(msg) > 1:
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
        else:
            await self.bot.say('.calculate takes in only 1 parameter')

    @commands.command()
    async def botinfo(self):
        time_online = str(datetime.timedelta(seconds=int(time.time() - self.uptime)))
        channels = sum([len(s.channels) for s in self.bot.servers])
        servers = sum([len(s.members) for s in self.bot.servers])
        await self.bot.say('''
```How many fgts have invited me to their server: {}
How many shitty channels i am connected to: {}
How many shitfaces i've encountered: {}
Time online: {}```
Invite me here
https://discordapp.com/oauth2/authorize?client_id=228759088593371137&scope=bot&permissions=536063039
'''.format(len(self.bot.servers), channels, servers, time_online))

    @commands.command(pass_context=True)
    async def serverinfo(self, ctx):
        server = ctx.message.server
        channels = [channel for channel in ctx.message.server.channels if channel.type == discord.ChannelType.text]
        await self.bot.say('''```
Dis This server is called {} and is made by {} at {} UTC.
There are {} useless channels and {} ugly fuckfaces on this server.
This server also has some weird rolenames like

{}

gay server tbh, 2/10 IGN    ```
{}'''.format(server.name, server.owner, str(server.created_at)[:19], len(channels),
                                              len(server.members), ' '.join([role.name for role in server.roles if not role.is_everyone]), server.icon_url))

def setup(bot):
    bot.add_cog(Public(bot))