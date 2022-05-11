import html

from data_types.discussion import Discussion
from data_types.repository import Repository
from data_types.user import User
from .base import EventBase


class EventDiscussions(EventBase):

    def __init__(self, sdk):
        super(EventDiscussions, self).__init__(sdk)
        self.discussion = None
        self.repository = None
        self.sender = None
        self.sdk = sdk

    """
    DiscussionsEvent

    Triggered when an discussion is created.

    https://developer.github.com/v3/activity/events/types/#discussionevent
    """

    async def process(self, payload, chat):
        """
        Processes Discussions event
        :param payload: JSON object with payload
        :param chat: current chat object
        :return:
        """

        self.sdk.log("Discussions event payload taken")

        try:
            self.discussion = Discussion(payload['discussion'])
            self.repository = Repository(payload['repository'])
            self.sender = User(payload['sender'])

        except Exception as e:
            self.sdk.log(f'Cannot process DiscussionsEvent payload because of {e}')

        action = payload['action']

        available_actions = {
            'created': self.created,
            'deleted': self.deleted,
        }

        if action not in available_actions:
            self.sdk.log(f'Unsupported Discussions action: {action}')
            return

        # call action handler
        await available_actions[action](chat['chat'], payload)

    async def created(self, chat_id, payload):
        """
        Discussion Created action
        :param chat_id: Current user chat token
        :param payload: GitHub payload
        :return:
        """

        message = (
            f'🗣{self.discussion.category.name}: {self.sender.login} created new discussion «<code>{html.escape(self.discussion.title)}</code>» [<a href="{self.repository.html_url}">{self.repository.name}</a>]'
            + "\n\n"
        )


        message += self.discussion.html_url

        await self.send(
            chat_id,
            message,
            'HTML'
        )

    async def deleted(self, chat_id, payload):
        """
        Discussion deleted action
        :param chat_id: Current user chat token
        :param payload: GitHub payload
        :return:
        """

        message = (
            f'🤭️ {self.sender.login} deleted discussion «<code>{html.escape(self.discussion.title)}</code>» [<a href="{self.repository.html_url}">{self.repository.name}</a>]'
            + "\n\n"
        )


        await self.send(
            chat_id,
            message,
            'HTML'
        )

