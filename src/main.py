import os
from dotenv import load_dotenv
from utils.logging_config import setup_logging
import asyncio

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

async def main():
    
    import infractions_bot.bot as nb
    bot = nb.bot
    try:

        bot.load_extension('infractions_bot.cogs.infractions')
        bot.load_extension('infractions_bot.cogs.infraction_info')
        bot.load_extension('infractions_bot.cogs.mod_commands')

        #dev cog
        bot.load_extension('infractions_bot.cogs.ping')
        
    except Exception as e:
        print('cog not loaded')
        print(e)

    await bot.start(BOT_TOKEN)

if __name__ == "__main__":
    setup_logging()
    asyncio.run(main())