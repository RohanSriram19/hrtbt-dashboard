from flask import Flask, request, jsonify
from twitch_bot import TwitchChatBot
import threading
import asyncio

app = Flask(__name__)

# Global references to the bot and its message buffer
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

    # Function to initialize and run the bot in a new event loop
    def run_bot():
        global bot
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # Create the bot instance inside the thread with the event loop context
        bot = TwitchChatBot(token=token, channel=channel, message_buffer=message_buffer)

        # Optionally wait for readiness (not strictly required for basic message listening)
        loop.run_until_complete(bot._ready_event.wait())
        bot.run()

    # Start the thread that runs the bot
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()

    return jsonify({"status": f"Bot started for channel '{channel}'."})

@app.route('/stop')
def stop_bot():
    global bot, bot_thread

    if bot:
        # Forcefully close the WebSocket connection
        bot._ws.close()
        bot = None
        return jsonify({"status": "Bot stopped."})
    else:
        return jsonify({"status": "No bot was running."})

@app.route('/messages')
def get_messages():
    # Return up to the last 100 chat messages
    return jsonify(message_buffer[-100:])

if __name__ == '__main__':
    app.run(debug=True)

