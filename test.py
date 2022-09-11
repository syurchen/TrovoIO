import asyncio
from trovoio import TrovoHTTP
from trovoio import WebSocket
from settings import client_id


async def main():
    client = TrovoHTTP(client_id)
    token = await client.get_chat_token(108099298)
    ws = WebSocket()
    await ws.join_via_token(token)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
