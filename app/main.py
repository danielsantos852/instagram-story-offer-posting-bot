# --- Imports ---
# Local
from bot import Bot


# --- Main Function ---
def main():
    
    # Get bot
    bot = Bot.get()

    # Run bot
    bot.run()


# Call main()
if __name__=='__main__': main()