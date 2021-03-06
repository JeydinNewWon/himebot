import json
import aiohttp
import operator

from discord.ext import commands


class BotList(object):
    """Updates bots.discord.pw infomation"""

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()
        self.bot.loop.create_task(self.update())

    def __unload(self):
        self.bot.loop.create_task(self.session.close())

    async def update(self):
        payload = json.dumps({
            "server_count": len(self.bot.servers)
        })

        headers = {
            "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySUQiOiIyMTY4NDcxMzMxOTY2ODEyMTciLCJyYW5kIjo4NzMsImlhdCI6MTQ3ODQzMzY2N30.x-iXS4JEWPuGEp83VTau1jKCEcgY6jG_CswR9uoOceI",
            "content-type": "application/json"
        }

        url = "https://bots.discord.pw/api/bots/{0}/stats".format(
            self.bot.user.id)

        await self.session.post(url, data=payload, headers=headers)

    async def on_server_join(self, server):
        await self.update()

    async def on_server_leave(self, server):
        await self.update()


def setup(bot):
    bot.add_cog(BotList(bot))
