import socket
import urllib.request
import datetime
from src.config.Configurator import Configurator as config
from src.log.Logger import logger


def waitForEventAndDownloadImage():
    # bind socket
    udp_address = config.get("doorbird", "udp_ip_address")
    udp_port = config.get("doorbird", "udp_port_two")
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_sock.bind((udp_address, int(udp_port)))
    logger.debug("UDP service started on address: {} and port: {}".format(udp_address, udp_port))
    old_message = ""
    while True:
        data = server_sock.recvfrom(1024)
        try:
            message = data[0].decode()

            if old_message == message
                logger.debug("Keep-alive msg: {}".format(message))

            old_message = message

        except:
            logger.debug("Message: An event has occured!")
            return downloadImage()


def downloadImage():
    # request picture from API and save it
    door_bird_url = config.get("doorbird", "door_bird_url")
    logger.debug("sending http request...")
    currentdate = datetime.datetime.now().timestamp()
    filepath = config.get("data", "data_path_unknown_faces")
    filename = filepath + str(currentdate) + '.jpg'
    urllib.request.URLopener().retrieve(door_bird_url, filename)
    return filename

