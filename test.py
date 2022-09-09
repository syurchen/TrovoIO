import asyncio
from trovoio.http import TrovoHTTP
from settings import client_id


async def main():
    client = TrovoHTTP(client_id)
    token = await client.get_chat_token(108099298)
    print(token)

if __name__ == '__main__':
  loop = asyncio.get_event_loop()
  loop.run_until_complete(main())
  loop.close()

