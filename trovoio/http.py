import json
import logging
import aiohttp

logger = logging.getLogger("trovoio.http")


class TrovoHTTP:
    TOKEN_BASE = 'https://open-api.trovo.live/openplatform/chat/channel-token/'

    def __init__(
            self, client_id: str = None
    ):
        self.client_id = client_id

    async def get_chat_token(self, channel_id: int) -> str:
        return (await self._request(self.TOKEN_BASE + str(channel_id)))['token']

    async def _request(self, route: str):
        headers = {
            'Accept:': 'application/json',
            'Client-ID': self.client_id,
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(route, headers=headers) as response:
                if 200 != response.status:
                    raise Exception('unable to get token')
                return json.loads(await response.text())
