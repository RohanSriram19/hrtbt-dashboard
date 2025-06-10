import asyncio
from twitchio.ext import commands
from sentiment import classify_and_store

class TwitchChatBot(commands.Bot):
    def __init__(self, token, channel, message_buffer):
        super().__init__(token=token, prefix='!', initial_channels=[channel])
        self.message_buffer = message_buffer

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')

    async def event_message(self, message):
        if message.echo:
            return

        text = message.content
        user = message.author.name

        # Classify and insert into MongoDB
        emotion = classify_and_store(user, text)
        print(f"{user}: {text} -> {emotion}")

        # Add to in-memory buffer for /messages and /summary endpoints
        self.message_buffer.append({
            "user": user,
            "text": text,
            "emotion": emotion
        })
