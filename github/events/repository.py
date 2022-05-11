from data_types.organization import Organization
from data_types.repository import Repository
from data_types.user import User
from .base import EventBase


class EventRepository(EventBase):

    def __init__(self, sdk):
        super(EventRepository, self).__init__(sdk)
        self.hook = None
        self.repository = None
        self.sender = None

    """
    RepositoryEvent

    Triggered when someone creates a new repository in your organization.

    https://docs.github.com/en/developers/webhooks-and-events/webhook-events-and-payloads#repository
    """

    async def process(self, payload, chat):
        """
        Processes Repository event
        :param payload: JSON object with payload
        :param chat: current chat object
        :return:
        """

        self.sdk.log(f"Repository event payload taken {payload}")

        try:

            self.repository = Repository(payload['repository'])
            self.organization = Organization(payload['organization'])
            self.sender = User(payload['sender'])

        except Exception as e:
            self.sdk.log(f'Cannot process RepositoryEvent payload because of {e}')

        action = payload['action']

        available_actions = {
            'created': self.created,
        }

        if action not in available_actions:
            self.sdk.log(f'Unsupported Repositories action: {action}')
            return

        # call action handler
        await available_actions[action](chat['chat'], payload)

    async def created(self, chat_id, payload):
        """
        Repository created action
        :param chat_id: Current user chat token
        :param payload: GitHub payload
        :return:
        """
        await self.send(
            chat_id,
            f'🦍 <a href="{self.sender.html_url}">{self.sender.login}</a> created a repository <a href="{self.repository.html_url}">{self.repository.full_name}</a> in the {self.organization.login} organization',
            'HTML',
        )

