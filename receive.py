import socket
from struct import unpack_from
import json
import time
import asyncio
import threading


class Bomb:
    def __init__(self):
        self._ticking = False
        self.counter_thread = None
        self.sensorThread = None
        self.keypadThread = None
        self.defused = False
        self.timer = 0
        self.modifier = 1
        self.loop = asyncio.get_event_loop()

        self.startListening()
        self.keypadListen()
        self.sensorListen()

    def terminate(self):
        self._ticking = False

    def activateCounter(self):
        self._ticking = True
        self.counter_thread = threading.Thread(target=self.countdown, args=(2 * 60,))
        self.counter_thread.start()

    def startListening(self):
        self.loop.run_until_complete(self.onRequestReceived())

    def sensorListen(self):
        self.sensorThread = threading.Thread(target=self.onSensorDetectsMovement)
        self.sensorThread.start()

    def keypadListen(self):
        self.keypadThread = threading.Thread(target=self.onKeypadSubmit)
        self.keypadThread.start()

    def countdown(self, t):
        self.timer = t
        while self.timer and self._ticking:
            mins, secs = divmod(self.timer, 60)
            timeformat = '{}:{}'.format(mins, secs)
            print(timeformat)
            time.sleep(1 / self.modifier)
            self.timer -= 1
            self.beepSound()
        if not self.defused:
            self.detonate()

    def activate(self):
        self.activateCounter()

    def onKeypadSubmit(self):
        # get input from the keypad
        pass
        # if code is correct
        #   self.terminate()
        # else
        #   self.modifier += 0.5

    def onSensorDetectsMovement(self):
        pass
        # get input from the sensor
        # if movement too much
        #   self.detonate()

    def beepSound(self):
        # make the buzzer beep
        pass

    async def onRequestReceived(self):

        BOMB_PROT_ID = 0xC4C4
        s1 = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
        s1.setblocking(False)
        print("Listening for bomb frames...")
        while True:
            all_data = await self.loop.sock_recv(s1, 80)
            self.loop.create_task(self.handleRequest(all_data))

    async def handleRequest(self, all_data):
        layer2 = unpack_from("!6B6BH", all_data)
        if layer2[-1] != 0xc4c4:
            return
        print("Received commands!")
        # print(all_data)
        commands = json.loads(all_data[14:].decode())
        if 'k3y' in commands and commands['k3y'] == "valhalaa":
            command = commands["command"]
            if command == "defuse":
                self.defused = True
                self.terminate()
                print("Bomb defused")
            elif command == "arm":
                self.activate()
            else:
                print("unknown command")
        else:
            self.modifier += 0.5

        print("Listening for bomb frames...")

    def detonate(self):
        # trigger explosion / led inidication
        self.terminate()
        print("Boom!")


bomb = Bomb()

exit()
