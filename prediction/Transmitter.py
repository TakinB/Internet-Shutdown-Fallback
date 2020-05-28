"""
Example for using the RFM9x Radio with Raspberry Pi.

Learn Guide: https://learn.adafruit.com/lora-and-lorawan-for-raspberry-pi
Author: Brent Rubell for Adafruit Industries
"""
# Import Python System Libraries
import time
# Import Blinka Libraries
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
# Import the SSD1306 module.
import adafruit_ssd1306
# Import RFM9x
import adafruit_rfm9x
import RPi.GPIO as GPIO
import textwrap

maxChar = 140

testString_BBC = "Hundreds of thousands of protesters have returned to the streets in Sudan's capital city Khartoum to demand an end to military rule. Security forc`++++++es have fire tear gas to disperse the crowd. Also on the programe: We speak with a North Korean defector about US president."
testString_ALJAZ = "Human Rights Watch (HRW) has accused Sudan's security forces of planning deadly attacks on protesters in the country earlier this year, warning that the violence could amount to crimes against humanity. "
# Button setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # ButA
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # ButB
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # ButC

# Configure LoRa Radio
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
rfm9x.tx_power = 23
prev_packet = None


def sendChunks(splittedString):
    for i in range(len(splittedString)):
        rfm9x.send(bytes(splittedString[i], "utf-8"))
        print(splittedString[i])
        time.sleep(1)
    rfm9x.send(bytes("PROTOCOLE", "utf-8"))


while True:
    button_stateA = GPIO.input(17)
    button_stateB = GPIO.input(27)
    button_stateC = GPIO.input(22)

    textSplitter_BBC = textwrap.wrap(testString_BBC, maxChar)
    textSplitter_ALJAZ = textwrap.wrap(testString_ALJAZ, maxChar)

    if not button_stateA == True:
        # button_a_data = bytes("AAbbc","utf-8")
        # rfm9x.send(button_a_data)
        sendChunks(textSplitter_BBC)
        print('404 A')
        time.sleep(0.1)

    if not button_stateB == True:
        sendChunks(textSplitter_ALJAZ)
        print('404 B')
        time.sleep(1)

    if not button_stateC == True:
        button_c_data = bytes("REFRESH", "utf-8")
        rfm9x.send(button_c_data)
        print('404 C')
        time.sleep(0.1)


