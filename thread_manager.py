import threading
import bot
import google_app
import bdfile



def run_bot_in_thread():

    bot.main()
    google_app.main()
    bdfile.main()


thread = threading.Thread(target=run_bot_in_thread)
thread.start()