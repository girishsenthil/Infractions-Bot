import os
from dotenv import load_dotenv
from utils.logging_config import setup_logging
import asyncio

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

async def main():
    # ► create the bot first
    import infractions_bot.new_bot as nb
    bot = nb.bot
    try:
        bot.load_extension('infractions_bot.cogs.infractions')
        bot.load_extension('infractions_bot.cogs.ping')
        # bot.load_extension('infractions_bot.cogs.getter')
    except:
        print('cogs not loaded')

    await bot.start(BOT_TOKEN)

if __name__ == "__main__":
    setup_logging()
    asyncio.run(main())