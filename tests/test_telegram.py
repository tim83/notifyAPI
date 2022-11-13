import timtools.notify
import timtools.settings
import notifyAPI.notifier


def test_telegram_creation():
    timtools.settings.replace_config_with_dummy()
    telegram_obj = notifyAPI.notifier.get_sender()
    assert isinstance(telegram_obj, timtools.notify.TelegramNotify)
