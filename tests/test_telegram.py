import timtools.notify
import timtools.settings

import notify_api.notifier


def test_telegram_creation():
    timtools.settings.replace_config_with_dummy()
    telegram_obj = notify_api.notifier.get_sender()
    assert isinstance(telegram_obj, timtools.notify.TelegramNotify)
