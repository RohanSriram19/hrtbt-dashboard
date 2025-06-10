from flask import Flask, request, jsonify
from twitch_bot import TwitchChatBot
from collections import Counter
import threading
import asyncio

app = Flask(__name__)

bot = None
bot_thread = None
message_buffer = []

@app.route('/start')
def start_bot():
    global bot, bot_thread, message_buffer

    if bot:
        return jsonify({"status": "Bot is already running."})

    channel = request.args.get('channel')
    token = request.args.get('token')

    if not channel or not token:
        return jsonify({"error": "Both 'channel' and 'token' query parameters are required."}), 400

    def run_bot():
        global bot
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        bot = TwitchChatBot(token=token, channel=channel, message_buffer=message_buffer)
        bot.run()

    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()

    return jsonify({"status": f"Bot started for channel '{channel}'."})

@app.route('/stop')
def stop_bot():
    global bot, bot_thread

    if bot:
        bot._ws.close()
        bot = None
        return jsonify({"status": "Bot stopped."})
    else:
        return jsonify({"status": "No bot was running."})

@app.route('/messages')
def get_messages():
    return jsonify(message_buffer[-100:])

@app.route('/summary')
def emotion_summary():
    emotion_counts = Counter(msg['emotion'] for msg in message_buffer if 'emotion' in msg)
    return jsonify(dict(emotion_counts))

if __name__ == '__main__':
    app.run(debug=True)
