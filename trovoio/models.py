from enum import Enum


class MessageType(str, Enum):
    auth = 'AUTH'
    response = 'RESPONSE'  # on successful auth
    ping = 'PING'
    pong = 'PONG'
    chat = 'CHAT'


class ChatMessageType(Enum):
    normal = 0
    spell = 5
    magic = 6
    magic_color = 7
    magic_spell = 8
    magic_bullet = 9
    subscription = 5001
    system = 5002
    follow = 5003
    welcome = 5004
    gift_sub = 5005
    gift_sub_detailed = 5006
    event = 5007
    raid_welcome = 5008
    custom_spell = 5009
    stream_on_off = 5012
    unfollow = 5013


class WsMessage:
    def __init__(self, msg_type: MessageType, data: dict = None, nonse: str = ''):
        self.type = msg_type
        self.nonse = nonse
        self.data = data


class AuthMessage(WsMessage):
    @staticmethod
    def create_from_token(token: str):
        return AuthMessage(
            MessageType.auth,
            {
                "token": token
            }
        )
