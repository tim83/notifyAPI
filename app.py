"""
Webserver to act as an API that acts upon receiving a webhook request
"""

import os

import sshtools.device
import sshtools.wakeup
import timtools.log
from flask import Flask

import notify_api.motion
import notify_api.notifier

app = Flask(__name__)

logger = timtools.log.get_logger(
    name="notify_api.app",
    filename=notify_api.motion.MOTION_NOTIFY_LOG_FILE,
)

timtools.log.set_verbose(True)


def get_notification_sender():
    """
    Obtains the instance responsible for sending messages to the user
    :return: A TelegramNotifier Class
    """
    return notify_api.notifier.get_sender()


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
    if notify_api.motion.send_notification():
        logger.info("Bewegingsmelding versturen")
        sender = get_notification_sender()
        hostname: str = notify_api.motion.get_device_hostname()
        sender.send_text(hostname + " heeft beweging gedetecteerd.")
        return "Notification sent"

    logger.info("Telefoon aanwezig op wifi-netwerk. Bewegingsmelding niet verzonden")
    return "Phone present, notification not sent"


@app.route("/file_saved")
def file_saved():
    """
    Send the file with the last detected motion to the user
    """
    if notify_api.motion.send_notification():
        logger.info("Laatste opname versturen")
        last_movie = notify_api.motion.get_most_recent_movie()
        logger.debug('"%s" wordt verstuurd', last_movie)

        sender = get_notification_sender()
        sender.send_file(str(last_movie))

        return f"File '{last_movie}' sent"

    logger.info("Telefoon in wifi-netwerk. Bewegingsmelding niet verzonden")
    return "Phone present, file not sent"


@app.route("/wakeup-thinkcentre")
def wakup_thinkcentre():
    """
    Wake-up thinkcentre upon recieving the request
    """
    thinkcentre = sshtools.device.Device("thinkcentre")
    sshtools.wakeup.wake(thinkcentre)

    sender = get_notification_sender()
    sender.send_text(f"Waking up {thinkcentre.hostname}")

    return f"{thinkcentre.hostname} had ben woken up"


if __name__ == "__main__":
    app.run(
        debug=bool(os.environ.get("DEBUG", False)),
        port=int(os.environ.get("PORT", 5000)),
        host=str(os.environ.get("HOST", "0.0.0.0")),
    )
