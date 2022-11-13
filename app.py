"""
Webserver to act as an API that acts upon receiving a webhook request from motioneye
"""

import os

import timtools.log
from flask import Flask

import notifyAPI.motion
import notifyAPI.notifier

app = Flask(__name__)

logger = timtools.log.get_logger(
    name="notifyAPI.app",
    filename=notifyAPI.motion.MOTION_NOTIFY_LOG_FILE,
)

timtools.log.set_verbose(True)


def get_notification_sender():
    """
    Obtains the instance responsible for sending messages to the user
    :return: A TelegramNotifier Class
    """
    return notifyAPI.notifier.get_sender()


@app.route("/")
def index():
    """Index page"""
    return ""


@app.route("/test")
def test_message():
    """Generic success message for heath checks"""
    return "OK"


@app.route("/motion_detected")
def motion_detected():
    """
    Send the message that motion is detected to the user, if the user is not present
    """
    if notifyAPI.motion.send_notification():
        logger.info("Bewegingsmelding versturen")
        sender = get_notification_sender()
        hostname: str = notifyAPI.motion.get_device_hostname()
        sender.send_text(hostname + " heeft beweging gedetecteerd.")
        return "Notification sent"

    logger.info("Telefoon aanwezig op wifi-netwerk. Bewegingsmelding niet verzonden")
    return "Phone present, notification not sent"


@app.route("/file_saved")
def file_saved():
    """
    Send the file with the last detected motion to the user
    """
    if notifyAPI.motion.send_notification():
        logger.info("Laatste opname versturen")
        last_movie = notifyAPI.motion.get_most_recent_movie()
        logger.debug('"%s" wordt verstuurd', last_movie)

        sender = get_notification_sender()
        sender.send_file(str(last_movie))

        return f"File '{last_movie}' sent"

    logger.info("Telefoon in wifi-netwerk. Bewegingsmelding niet verzonden")
    return "Phone present, file not sent"


if __name__ == "__main__":
    app.run(
        debug=bool(os.environ.get("DEBUG", False)),
        port=int(os.environ.get("PORT", 5000)),
        host=str(os.environ.get("HOST", "0.0.0.0")),
    )
