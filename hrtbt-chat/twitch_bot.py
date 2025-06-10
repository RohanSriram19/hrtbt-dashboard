from twitchio.ext import commands
from sentiment import classify_emotion

class TwitchChatBot(commands.Bot):
    def __init__(self, token, channel, message_buffer):
        super().__init__(
            token=f'oauth:{token}',           # OAuth token for Twitch API authentication
            prefix='!',                       # Required by twitchio, but not used here
            initial_channels=[channel]        # Connects to the specified Twitch channel
        )
        self.channel = channel
        self.message_buffer = message_buffer  # Shared list to store processed chat messages

    async def event_ready(self):
        # Triggered when the bot has successfully connected to Twitch
        print(f'Connected to Twitch chat as {self.nick}')

    async def event_message(self, message):
        # Ignore messages sent by the bot itself
        if message.echo:
            return

        # Run emotion classification on the incoming message text
        emotion = classify_emotion(message.content)

        # Append the result to the shared message buffer
        self.message_buffer.append({
            "user": message.author.name,
            "text": message.content,
            "emotion": emotion
        })

        # Print the message and its detected emotion
        print(f'{message.author.name}: {message.content} ({emotion})')
