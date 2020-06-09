import pycom
import machine
import time
from ucollections import deque
import _thread
from umqtt import MQTTClient
import private


class Morse:
    encoding = {'a': '.-',     'b': '-...',   'c': '-.-.',   'd': '-..',    'e': '.',      'f': '..-.',
                'g': '--.',    'h': '....',   'i': '..',     'j': '.---',   'k': '-.-',    'l': '.-..',
                'm': '--',     'n': '-.',     'o': '---',    'p': '.--.',   'q': '--.-',   'r': '.-.',
                's': '...',    't': '-',      'u': '..-',    'v': '...-',   'w': '.--',    'x': '-..-',
                'y': '-.--',   'z': '--..',   '1': '.----',  '2': '..---',  '3': '...--',  '4': '....-',
                '5': '.....',  '6': '-....',  '7': '--...',  '8': '---..',  '9': '----.',  '0': '-----',
                '.': '.-.-.-', ',': '--..--', '?': '..--..', '!': '-.-.--', '/': '--.-.',  '(': '-.--.',
                ')': '-.--.-', '&': '.-...',  ':': '---...', ';': '-.-.-.', '=': '-...-',  '+': '.-.-.',
                '-': '-....-', '_': '..--.-', "'": '.----.', '"': '.-..-.', '$': '...-..-', '@': '.--.-.',
                ' ': '^'
                }
    colors = {'R': 0x1f0000, 'O': 0x1f1000, 'Y': 0x1f1900, 'G': 0x000f00,
              'B': 0x00001f, 'I': 0x090010, 'V': 0x1d101d, 'W': 0x1f1f1f}
    color = colors['W']
    unit_len = 75
    char_queue = deque((), 2048, 1)
    char_queue_lock = _thread.allocate_lock()

    def __init__(self):
        print("Morse()")
        pycom.heartbeat(False)
        _thread.start_new_thread(lambda: self.output_loop(), ())

    def add_to_queue(self, char):
        while True:
            try:
                with self.char_queue_lock:
                    self.char_queue.append(char)
                return
            except IndexError:
                machine.idle()

    def enqueue_message(self, msg, color='W'):
        if msg[0:2] == '!!':
            color_char = msg[2:3]
            msg = msg[3:]
            if color_char in self.colors:
                color = color_char
            else:
                print("Illegal color code (" + color_char + ")")
        code = ','.join(
            map(lambda x: self.encoding.get(x, ''), list(msg.lower())))
        code = color + code + '^,'
        for c in list(code):
            self.add_to_queue(c)

    def light(self, length):
        pycom.rgbled(self.color)
        time.sleep_ms(length)
        pycom.rgbled(0)

    def output(self, c):
        if c == '.':
            self.light(self.unit_len)
            time.sleep_ms(self.unit_len)
        elif c == '-':
            self.light(3 * self.unit_len)
            time.sleep_ms(self.unit_len)
        elif c == ',':
            time.sleep_ms(2 * self.unit_len)
        elif c == '^':
            time.sleep_ms(5 * self.unit_len)
        elif c in self.colors:
            self.color = self.colors[c]
        else:
            print('Unknown character (' + c + ')')

    def output_loop(self):
        while True:
            with self.char_queue_lock:
                if self.char_queue:
                    c = self.char_queue.popleft()
                else:
                    c = ''
            if c != '':
                self.output(c)
            machine.idle()


def message_received(topic, msg):
    msg = msg.decode("utf-8")
    print("Message received: " + msg)
    morse.enqueue_message(msg)


print("Connecting to " + private.aio_server)
client = MQTTClient(client_id=private.client_id, server=private.aio_server,
                    user=private.aio_user, password=private.aio_key, keepalive=30, ssl=False)
client.set_callback(message_received)
client.connect()
client.subscribe(private.aio_feed)

morse = Morse()
morse.enqueue_message("ok", 'G')

timer = time.ticks_ms()
print("Running...")
while True:
    client.check_msg()
    if time.ticks_diff(time.ticks_ms(), timer) > 30000:
        client.ping()
        timer = time.ticks_ms()
    machine.idle()
    time.sleep_ms(100)
