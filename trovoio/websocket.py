import json

import aiohttp
import logging
import asyncio
import time

logger = logging.getLogger("trovoio.http")


class WebSocket:
    WS_URL = 'wss://open-chat.trovo.live/chat'

    def __init__(self, heartbeat: float = None):
        self._websocket = None
        self._keeper = None
        self.heartbeat = heartbeat
        self._reconnect_delay = 5
        self._last_ping = None
        self._ping_interval = 30
        self._reconnect_requested = False
        self._chat_token = None
        self._session = aiohttp.ClientSession()

    @property
    def is_alive(self) -> bool:
        return self._websocket is not None and not self._websocket.closed

    async def join_via_token(self, token: str):
        self._chat_token = token
        await self._connect_and_auth()

    async def _connect_and_auth(self):
        if self._keeper:
            self._keeper.cancel()  # Stop our current keep alive.
        if self.is_alive:
            await self._websocket.close()  # If for some reason we are in a weird state, close it before retrying.
        try:
            self._websocket = await self._session.ws_connect(url=self.WS_URL, heartbeat=self.heartbeat)
            await self._send({
                "type": "AUTH",
                "nonce": "",
                "data": {
                    "token": self._chat_token
                }
            })
        except Exception as e:
            retry = self._reconnect_delay
            logger.error(f"Websocket connection failure: {e}:: Attempting reconnect in {retry} seconds.")

            await asyncio.sleep(retry)
            return asyncio.create_task(self._connect_and_auth())
        self._keeper = asyncio.create_task(self._keep_alive())
        asyncio.create_task(self._keep_pinging())

    async def _keep_pinging(self):
        while not self._websocket.closed and not self._reconnect_requested:
            if not self._last_ping:
                self._last_ping = time.time()
            else:
                if time.time() >= self._last_ping + self._ping_interval:
                    await self._ping()
            await asyncio.sleep(1)

    async def _keep_alive(self):
        while not self._websocket.closed and not self._reconnect_requested:
            msg = await self._websocket.receive()  # Receive data...

            if msg.type is aiohttp.WSMsgType.CLOSED:
                logger.error(f"Websocket connection was closed: {msg.extra}")
                break
            data = json.loads(msg.data)
            if data:
                logger.debug(f" < {data}")
                if 'PONG' == data['type']:
                    self._ping_interval = data['data']['gap']
        asyncio.create_task(self._connect_and_auth())

    async def _ping(self):
        await self._send(
            {
                "type": "PING",
                "nonce": ""
            }
        )
        self._last_ping = time.time()

    async def _send(self, message: dict):
        await self._websocket.send_str(json.dumps(message) + "\r\n")
