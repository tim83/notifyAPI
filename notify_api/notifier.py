"""Module wrapping the timtools telegram class"""
import timtools.notify


def get_sender() -> timtools.notify.TelegramNotify:
    """Returns a TelegramNotify instance from timtools"""
    return timtools.notify.TelegramNotify()
