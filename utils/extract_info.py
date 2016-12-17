import youtube_dl
import functools
import asyncio


class Extract:

    def __init__(self):
        self.loop = asyncio.get_event_loop()
        # TODO: do these instance vars need setting?
        self.title = None
        self.url = None
        self.yt = None
        self.display_id = None
        self.webpage_url = None
        self.thumbnail = None
        self.upload_url = None
        self.download_url = None
        self.views = None
        self.is_live = None
        self.likes = None
        self.dislikes = None
        self.duration = None
        self.uploader = None
        self.description = None

    async def extract(self, url):
        opts = {
            'default_search': 'auto',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }],
            'force_ipv4': True,
            'source_address': '0.0.0.0',
            "playlist_items": "0",
            "playlist_end": "0",
            "noplaylist": True,
            "outtmpl": 'cache/%(id)s.%(ext)s',
            "forcefilename": True
        }
        ydl = youtube_dl.YoutubeDL(opts)
        func = functools.partial(ydl.extract_info, url)
        info = await self.loop.run_in_executor(None, func)
        if "entries" in info:
            info = info['entries'][0]

        self.url = url
        self.yt = ydl
        self.display_id = info.get('display_id')
        self.thumbnail = info.get('thumbnail')
        self.webpage_url = info.get('webpage_url')
        self.download_url = info.get('download_url')
        self.views = info.get('view_count')
        self.is_live = bool(info.get('is_live'))
        self.likes = info.get('like_count')
        self.dislikes = info.get('dislike_count')
        self.duration = info.get('duration')
        self.uploader = info.get('uploader')

        is_twitch = 'twitch' in url
        if is_twitch:
            # twitch has 'title' and 'description' sort of mixed up.
            self.title = info.get('description')
            self.description = None
        else:
            self.title = info.get('title')
            self.description = info.get('description')

        return self
