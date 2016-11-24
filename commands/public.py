import discord
import requests
import random
import time
import datetime

from discord.ext import commands
from utils import check_perms, formats


class Public:
    def __init__(self, bot):
        self.bot = bot
        self.uptime = time.time()

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
**.lookup ip**: lookup an ip
**.define word**: looks up a definition for the word in urban dictionary
**.botinfo**: tf do u think?
**.invite**: for inviting the bot
**.serverinfo**: returns some info about the server
**mention me or call my name**: to have a nice chat with me

Music cmds:
**.play name of song/url**: play a song with url or song name. Searches on yt for the song if no url not specified. Use this to summon bot aswell
**.skip**: vote to skip a song
**.volume 0-100**: change the volume
**.pause**: pause the song
**.resume**: resume the song
**.stop**: stops the bot from playing, and makes it leave the channel
**.current**: shows info about the current song

Advanced cmds that need advanced perms:
**.createinvite**: creates an instant invite in the current server
**.ban fgt**: ban a fgt
**.kick fgt**: replace ban with kick^
**.purge amount**: go through **amount** messages and delete it, purging by default goes through or purges 100 msgs if an amount is not given.
**.purge user**: go through 100 messages, if the author of the message is **user**, delete it
**.purge amount user**: go through **amount** messages, if the author of the message is **user**, delete it
**.clear**: sends 1000 lines of NULL chars to clear the chat
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
            
            ipinfo = [
                ("Country", country),
                ("City", city),
                ("Region", region),
                ("Timzone", timezone),
                ("Zip", zipcode),
                ("Latitude", latitude),
                ("Longitude", longitude),                
                ("ISP", isp),
                ("Org", org)
                ]
            
            await formats.indented_entry_to_code(self.bot, ipinfo)
        else:
            await self.bot.say("you dumb or wat, is that an ip?")
    
    @commands.command(pass_context=True)
    async def define(self, ctx, *, word):
        if ' ' in word:
            word = word.replace(' ', '+')
        
        try:     
            r = requests.get('http://api.urbandictionary.com/v0/define?term={}'.format(word), allow_redirects=True)
            definition = r.json()['list'][0]['definition']
            example = r.json()['list'][0]['example']
            await self.bot.say("```{0}```\n{1}".format(definition, example))    
        except:
            await self.bot.say('no definition found for this word')
    
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
        members = sum([len(s.members) for s in self.bot.servers])
        
        botinfo = [
            ("How many fgts have invited me to their server", len(self.bot.servers)),
            ("How many shitty channels i am connected to", channels),
            ("How many shitfaces i've encountered", members),
            ("Servers playing music on", len([i for i in self.bot.cogs['Music'].voice_states if i is not None])),
            ("Been online for", time_online),
            ]
        
        
        await formats.indented_entry_to_code(self.bot, botinfo)
        await self.bot.say('''

Beemo halped me ok
https://github.com/initzx/himebot

My site
http://init0.zsrv.pw
''')

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