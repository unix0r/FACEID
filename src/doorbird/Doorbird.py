# -*- coding: utf-8 -*-

import binascii
import socket
import urllib.request
import datetime
from src.incidents.Mail import sendMail
from src.config.Configurator import Configurator as config
from src.log.Logger import logger


def waitForEventAndDownloadImage():
    # bind socket
    udp_address = config.get("doorbird", "udp_ip_address")
    udp_port = config.get("doorbird", "udp_port")
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_sock.bind((udp_address, int(udp_port)))
    server_sock.settimeout(int(config.get("doorbird", "keep_alive_timeout")))
    logger.info("UDP service started on address: {} and port: {}".format(udp_address, udp_port))
    old_message = ""
    old_event = ""

    while True:

        try:
            data = server_sock.recvfrom(1024)
        except:
            # Timeout: No Keep Alive Packets
            sendMail("No KeepAlive Pakcets from Doorbird! Check your Connection")
            logger.error("No KeepAlive Pakcets from Doorbird! Check your Connection")
            continue

        try:
			#read received udp data
            message = data[0].decode()

            if message != old_message:
                logger.debug("Keep-alive msg: {}".format(message))

            old_message = message

        except:
            hex_bytes = binascii.hexlify(data[0])
            event = hex_bytes.decode("ascii")

            if event != old_event:
                logger.info("Message: An event has occured!")
                old_event = event
                return downloadImage()
            old_event = event
    # server_sock.close()


def downloadImage():
    # request picture from API and save it
    door_bird_url = config.get("doorbird", "door_bird_url")
    currentdate = datetime.datetime.now().timestamp()
    filepath = config.get("data", "data_path_unknown_faces")
    filename = filepath + str(currentdate) + '.jpg'
    logger.debug("sending http request to: " + door_bird_url + " and saving to " + filename)

    try:
        urllib.request.URLopener().retrieve(door_bird_url, filename)
        return filename
    except:
        sendMail("Doorbird not available!: " + str(door_bird_url))
        logger.debug("Doorbird not available: ")
        return "ERROR"
