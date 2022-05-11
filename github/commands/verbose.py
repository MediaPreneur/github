from classes.chat_controller import ChatController
from settings import URL, USERS_COLLECTION_NAME
from .base import CommandBase


class CommandVerbose(CommandBase):

    async def __call__(self, payload):
        self.sdk.log(f"/github_verbose handler fired with payload {payload}")

        self.set_bot(payload)

        verbose = payload.get("params", "")
        if not len(verbose) or verbose not in ["on", "off", "true", "false"]:
            return await self.send(
                payload["chat"],
                "Please, specify verbosity:\ntrue or false. This parameter regulates whether modified/added/removed files will be visible."
            )

        verbose = verbose in ["on", "true"]

        chat = ChatController(self.sdk).get_chat(payload['chat'], self.bot)
        chat["verbose"] = verbose
        self.sdk.db.update(USERS_COLLECTION_NAME, {'chat': chat['chat'], 'bot': self.bot}, chat)

        await self.send(payload["chat"], f"Verbosity mode set for {verbose}")
