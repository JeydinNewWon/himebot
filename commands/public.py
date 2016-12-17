import discord
import requests
import random
import urllib3
import re

from discord.ext import commands

class Public:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def say(self, ctx, *, msg):
        await self.bot.say(msg)

    @commands.command(pass_context=True)
    async def help(self, ctx):
        await self.bot.send_message(ctx.message.author, '''
General cmds for fgts:
**.help**: returns help command
**.randint [start | end]**: rolls a random number in the specified range, if no numbers are specified, roll a random number between 0 and 100
**.cal expression**: calculates an arithemetical expression
**.lookup ip**: lookup an ip
**.define word**: looks up a definition for the word in urban dictionary
**.invite**: for inviting the bot
**.botinfo**: tf do u think?
**.serverinfo**: returns some info about the server
**.userinfo user**: returns some info about a user
**mention me or call my name**: to have a nice chat with me
**.rule34**: :smirk:

Music cmds:
**.play name of song/url**: play a song with url or song name. Searches on yt for the song if no url not specified. Use this to summon bot aswell
**.skip**: vote to skip a song
**.volume 0-100**: change the volume
**.pause**: pause the song
**.resume**: resume the song
**.stop**: stops the bot from playing, and makes it leave the channel
**.current**: shows info about the current song
**.songlist**: shows all the queued songs to be played

Advanced cmds that need advanced perms:
**.createinvite**: creates an instant invite in the current server
**.ban fgt**: ban a fgt
**.kick fgt**: replace ban with kick^
**.clear**: sends 1000 lines of NULL chars to clear the chat
**.purge [member] [amount]**: this takes a lot to explain xd. Go to https://www.himebot.xyz for help
''')

INVITE = '''
Invite me here
https://discordapp.com/oauth2/authorize?client_id=232916519594491906&scope=bot&permissions=536063039

My server
https://discord.gg/b9RCGvk
'''

NUDES = [
    'https://goo.gl/8jjmeR'
]

def r34(query):
    http = urllib3.PoolManager()
    request = http.request(
        'GET', 'http://cloud.rule34.xxx/index.php?page=dapi&s=post&q=index&tags={}&limit=1000'.format(query)).data.decode()
    links = [i for i in re.findall(
        'cloudimg\.rule34[^"]+', request) if 'thumbnails' not in i]
    if len(links) > 0:
        return 'http://' + random.choice(links)
    return "couldn't match the query"


    @commands.command(pass_context=True)
    async def lookup(self, ctx, ip):
        verify = ip.replace('.', '')
        if verify.isdigit():
            r = requests.get(
                'http://ip-api.com/json/{}'.format(ip), allow_redirects=True).json()

            data = discord.Embed(
                description="Information about this IP",
                color=discord.Color(value="16727871")
            )

            data.add_field(name="Country", value=r['country'])
            data.add_field(name="City", value=r['city'])
            data.add_field(name="Zipcode", value=r['zip'])
            data.add_field(name="Region", value=r['region'])
            data.add_field(name="Timezone", value=r['timezone'])
            data.add_field(name="Latitude", value=r['lat'])
            data.add_field(name="Longitude", value=r['lon'])
            data.add_field(name="ISP", value=r['isp'])
            data.add_field(name="Org", value=r['org'])

            data.set_author(name=ip, url="http://ip-api.com/{}".format(ip))

            try:
                await self.bot.say(embed=data)
            except discord.HTTPException:
                await self.bot.say("I need to be able to send embedded links")
        else:
            await self.bot.say("you dumb or wat, is that an ip?")

    @commands.command(pass_context=True)
    async def define(self, ctx, *, word):
        if ' ' in word:
            word = word.replace(' ', '+')

        try:
            r = requests.get('http://api.urbandictionary.com/v0/define?term={}'.format(word), allow_redirects=True).json()
            definition = r['list'][0]['definition']
            example = r['list'][0]['example']
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

    @commands.command(pass_context=True, no_pm=True)
    async def serverinfo(self, ctx):
        server = ctx.message.server
        online = len([m.status for m in server.members
                      if m.status == discord.Status.online or
                      m.status == discord.Status.idle])
        total_users = len(server.members)
        text_channels = len([x for x in server.channels
                             if x.type == discord.ChannelType.text])
        voice_channels = len(server.channels) - text_channels
        created_at = ("{}".format(
            server.created_at.strftime("%d %b %Y %H:%M")))

        data = discord.Embed(
            description="Server ID: " + server.id,
            colour=discord.Colour(value="16727871"))
        data.add_field(name="Region", value=str(server.region))
        data.add_field(name="Users online",
                       value="{}/{}".format(online, total_users))
        data.add_field(name="Total Text Channels", value=str(text_channels))
        data.add_field(name="Total Voice Channels", value=str(voice_channels))
        data.add_field(name="Roles", value=str(
            len([i.name for i in server.roles if i.name != "@everyone"])))
        data.add_field(name="Owner", value=str(server.owner))
        data.add_field(name="Created at", value=created_at)

        if server.icon_url:
            data.set_author(name=server.name, url=server.icon_url)
            data.set_thumbnail(url=server.icon_url)
        else:
            data.set_author(name=server.name)

        try:
            await self.bot.say(embed=data)
        except discord.HTTPException:
            await self.bot.say("I need to be able to send embedded links")

    @commands.command(pass_context=True)
    async def userinfo(self, ctx, member: discord.Member):

        name = member.name
        discriminator = member.discriminator
        game = member.game if member.game else None
        nick = member.nick
        id = member.id
        created_at = "{}".format(member.created_at.strftime("%d %b %Y %H:%M"))
        joined_at = "{}".format(member.joined_at.strftime("%d %b %Y %H:%M"))
        roles = ', '.join(
            [i.name for i in member.roles if i.name != "@everyone"])

        data = discord.Embed(
            description="User ID: " + id,
            colour=discord.Color(value="16727871")
        )

        data.add_field(name="Discriminator", value=discriminator)
        data.add_field(name="Nickname", value=nick)
        data.add_field(name="Playing or streaming", value=game)
        data.add_field(name="Account created at", value=created_at)
        data.add_field(name="Joined this server at", value=joined_at)
        data.add_field(name="Roles", value=roles, inline=False)

        if member.avatar_url:
            data.set_author(name=name, url=member.avatar_url)
            data.set_thumbnail(url=member.avatar_url)
        else:
            data.set_author(name=name)

        try:
            await self.bot.say(embed=data)
        except discord.HTTPException:
            await self.bot.say("I need to be able to send embedded links")

    @commands.command()
    async def invite(self):
        await self.bot.say(INVITE)

    @commands.command()
    async def nudes(self):
        await self.bot.say(random.choice(NUDES))
        await self.bot.say("donate for more ;)")

    @commands.command(pass_context=True)
    async def rule34(self, ctx, *, term):
        future = await self.bot.loop.run_in_executor(None, r34, term.replace(' ', '_'))
        await self.bot.say(future)


def setup(bot):
    bot.add_cog(Public(bot))
