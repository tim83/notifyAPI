"""Module containing functions for sending notification for motion related triggers"""
import socket
from pathlib import Path

import sshtools.device

MOTION_MEDIA_LOCATION: Path = Path("/var/lib/motioneye/Camera1")
MOTION_NOTIFY_LOG_FILE: Path = Path("/tmp/motion-log.log")


def send_notification() -> bool:
    """Checks if a notification should be sent"""
    dev_phone: sshtools.device.Device = sshtools.device.Device("phone")
    return not (dev_phone.is_present and dev_phone.is_local)


def get_device_hostname() -> str:
    """Returns the hostname of the current machine"""
    return socket.gethostname()


def get_most_recent_movie() -> Path:
    """Returns the most recent motion recording"""
    date_dirs = [f for f in MOTION_MEDIA_LOCATION.iterdir() if f.is_dir()]
    date_dir: Path
    for date_dir in sorted(date_dirs, reverse=True):
        for movie in sorted(date_dir.iterdir(), reverse=True):
            if movie.suffix == ".mp4":
                return movie
    raise FileNotFoundError("No movie file found")
