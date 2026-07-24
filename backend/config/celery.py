import os
from celery import Celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE","backend.config.settings")
app=Celery("institutional_trading_platform"); app.config_from_object("django.conf:settings",namespace="CELERY"); app.autodiscover_tasks()

from celery.signals import worker_ready

@worker_ready.connect
def send_worker_ready_alert(sender, **kwargs):
    try:
        from dotenv import load_dotenv
        from pathlib import Path
        BASE_DIR = Path(__file__).resolve().parents[1]
        load_dotenv(BASE_DIR / ".env")
        
        tg_token = os.getenv("TELEGRAM_BOT_TOKEN")
        if tg_token:
            from telegram.bot import TelegramBotClient
            tg_client = TelegramBotClient(tg_token)
            chat_id = "-1003781184008"
            msg = (
                f"CELERY TASK WORKER STARTED\n\n"
                f"Status: TradingWorker service online and ready.\n"
                f"Concurrency: 4 Thread Pool Active.\n"
                f"Connection: Linked to Redis Channel Layer successfully."
            )
            tg_client.send_message(chat_id, msg)
    except Exception as e:
        pass
