import threading, asyncio
from telegram_bot import launch_tg_bot
from backend.app import app



def main():
    tg_bot_thread = threading.Thread(target=asyncio.run, args=(launch_tg_bot(),))
    backend_app_thread = threading.Thread(target=app.run, args=("0.0.0.0",),)

    tg_bot_thread.start()
    backend_app_thread.start()
    backend_app_thread.join()
    

main()
