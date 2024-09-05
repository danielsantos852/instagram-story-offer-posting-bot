# --- Imports ---
# Local
from bot import Bot


# --- Main Function ---
def main():
    
    # Get bot
    bot = Bot.get()

    # Run bot (by offer)
    bot.run_by_offer(test_call=False)


# Call main()
if __name__=='__main__': main()