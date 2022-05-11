from classes.chat_controller import ChatController
from settings import URL
from .base import CommandBase


class CommandLink(CommandBase):

    async def __call__(self, payload):
        self.sdk.log(f"/github_link handler fired with payload {payload}")

        self.set_bot(payload)

        chat = ChatController(self.sdk).get_chat(payload['chat'], self.bot)

        link = f'{URL}/github/{chat["user"]}'

        await self.send(payload["chat"], f"Link to the chat: {link}")
