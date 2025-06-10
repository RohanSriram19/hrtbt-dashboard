from twitchio.ext import commands
from sentiment import classify_emotion

class TwitchChatBot(commands.Bot):
    def __init__(self, token, channel, message_buffer):
        super().__init__(
            token=f'oauth:{token}',
            prefix='!',
            initial_channels=[channel]
        )
        self.channel = channel
        self.message_buffer = message_buffer

    async def event_ready(self):
        print(f'Connected to Twitch chat as {self.nick}')

    async def event_message(self, message):
        print("Message received")  # Debug: this tells us the bot is getting messages

        if message.echo:
            return

        emotion = classify_emotion(message.content)

        self.message_buffer.append({
            "user": message.author.name,
            "text": message.content,
            "emotion": emotion
        })

        print(f'{message.author.name}: {message.content} ({emotion})')

