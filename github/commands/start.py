from settings import URL
from .base import CommandBase
from classes.chat_controller import ChatController


class CommandStart(CommandBase):

    async def __call__(self, payload):
        self.sdk.log(f"/start handler fired with payload {payload}")

        self.set_bot(payload)

        chat = ChatController(self.sdk).get_chat(payload['chat'], self.bot)

        link = f'{URL}/github/{chat["user"]}'

        await self.send(
            payload["chat"],
            "To connect repository notifications follow next steps:"
        )

        await self.sdk.send_image_to_chat(
            payload['chat'],
            photo=f'{URL}/img/step_1.jpg',
            caption="1) Open repository settings.",
            bot=self.bot,
        )


        await self.sdk.send_image_to_chat(
            payload['chat'],
            photo=f'{URL}/img/step_2.jpg',
            caption="2) Go to \"Webhooks\" and press button \"Add webhook\".",
            bot=self.bot,
        )


        message = "3) Paste in the \"Payload URL\" field this link.\n{}\n" \
                  "\n" \
                  "4) For «Content type» choose «application/json».\n" \
                  "\n" \
                  "5) For «Which events would you like to trigger this webhook?» choose \n" \
                  "«Send me everything.»\n" \
                  "\n" \
                  "6) Press button «Add webhook».".format(link)

        await self.send(
            payload["chat"],
            message
        )
