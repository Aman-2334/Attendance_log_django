from django_eventstream.channelmanager import DefaultChannelManager
from django.contrib.auth import get_user

class EventChannelManager(DefaultChannelManager):
    def can_read_channel(self, user, channel):
        print(f"can read channel, {user}, {channel}")
        if user is None:
            return False
        return True
