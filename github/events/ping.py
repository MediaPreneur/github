from data_types.hook import Hook
from data_types.organization import Organization
from data_types.repository import Repository
from data_types.user import User
from .base import EventBase


class EventPing(EventBase):

    def __init__(self, sdk):
        super(EventPing, self).__init__(sdk)
        self.hook = None
        self.repository = None
        self.sender = None

    """
    PingEvent

    Triggered when new webhook added.

    https://developer.github.com/webhooks/#ping-event
    """

    async def process(self, payload, chat):
        """
        Processes Ping event
        :param payload: JSON object with payload
            zen - Random string of GitHub zen
            hook_id - The ID of the webhook that triggered the ping
            hook - The webhook configuration
        :param chat: current chat object
        :return:
        """

        self.sdk.log(f"Ping event payload taken {payload}")

        if "repository" in payload:
            await self.process_repository_event(payload, chat)
        elif "organization" in payload:
            await self.process_organization_event(payload, chat)
        else:
            self.sdk.log('Payload from GitHub does not contain neigher repository nor organization')
            self.sdk.hawk.catch()

    async def process_repository_event(self, payload, chat):
        try:
            self.repository = Repository(payload['repository'])
            self.sender = User(payload['sender'])
            self.hook = Hook(payload['hook'])

        except Exception as e:
            self.sdk.log(f'Cannot process PingEvent payload because of {e}')

        await self.send(
            chat['chat'],
            f'👏 Repository {self.repository.full_name} successfully linked. Boom.',
            'HTML',
        )

    async def process_organization_event(self, payload, chat):
        try:
            self.organization = Organization(payload['organization'])
            self.hook = Hook(payload['hook'])

        except Exception as e:
            self.sdk.log(f'Cannot process PingEvent payload because of {e}')

        await self.send(
            chat['chat'],
            f'👏 Organization {self.organization.login} successfully linked. Boom.',
            'HTML',
        )
