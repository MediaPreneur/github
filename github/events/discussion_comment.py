import html

from data_types.repository import Repository
from data_types.user import User
from data_types.discussion import Discussion
from data_types.discussion_comment import DiscussionComment
from .base import EventBase

class EventDiscussionComment(EventBase):

    def __init__(self, sdk):
        super(EventDiscussionComment, self).__init__(sdk)
        self.discussion = None
        self.repository = None
        self.comment = None
        self.sender = None
        self.sdk = sdk

    """
    DiscussionCommentEvent

    Triggered when an discussion comment is created.

    https://developer.github.com/v3/activity/events/types/#discussioncommentevent
    """


    async def process(self, payload, chat):
        """
        Processes DiscussionComment event
        :param payload: JSON object with payload
        :param chat: current chat object
        :return:
        """

        self.sdk.log("DiscussionComment event payload taken")

        try:
            self.discussion = Discussion(payload['discussion'])
            self.comment = DiscussionComment(payload['comment'])
            self.repository = Repository(payload['repository'])
            self.sender = User(payload['sender'])

        except Exception as e:
            self.sdk.log(f'Cannot process DiscussionCommentEvent payload because of {e}')

        action = payload['action']

        available_actions = {
            'created': self.created
        }

        if action not in available_actions:
            self.sdk.log(f'Unsupported DiscussionComment action: {action}')
            return

        # call action handler
        await available_actions[action](chat['chat'], payload)

    async def created(self, chat_id, payload):
        """
        DiscussionComment created action
        :param chat_id: Current user chat token
        :param payload: GitHub payload
        :return:
        """

        message = (
            f'🤓{self.sender.login} added <a href="{self.comment.html_url}">comment</a> to {self.discussion.category.name} discussion <code>«{html.escape(self.discussion.title)}»</code> [<a href="{self.repository.html_url}">{self.repository.name}</a>]'
            + "\n"
        )


        await self.send(
            chat_id,
            message,
            'HTML'
        )
