import multiprocessing
from bot.discord_bot import run_bot

if __name__ == "__main__":
    # Start the bot process
    bot_process = multiprocessing.Process(target=run_bot)
    bot_process.start()

    # Join the bot process
    bot_process.join()
