import collections
import enum

import rpi_ws281x

from rpi_ws281x import Adafruit_NeoPixel

# LED strip configuration:
LED_COUNT = 256  # 12        # Number of LED pixels.
LED_PIN = 12  # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
# True to invert the signal (when using NPN transistor level shift)
LED_INVERT = False


class Color(enum.Enum):
    PRIM = 1
    SEC = 2


Pixel = collections.namedtuple("Pixel", ["x", "y", "color"])
Face = collections.namedtuple("Face", ["eyes", "rest"])


FACES = {
    "😐" : [ Pixel(3,3, Color.PRIM),
        Pixel(3,4, Color.PRIM),
        Pixel(3,2, Color.PRIM),
        Pixel(4,3, Color.PRIM),
        Pixel(2,3, Color.PRIM),
        ],
    "😖" : [ Pixel(4,3, Color.PRIM),
        Pixel(4,4, Color.PRIM),
        Pixel(4,2, Color.PRIM),
        Pixel(5,3, Color.PRIM),
        Pixel(3,3, Color.PRIM),
        ],
    "😀" : [ Pixel(5,3, Color.PRIM),
        Pixel(5,4, Color.PRIM),
        Pixel(5,2, Color.PRIM),
        Pixel(6,3, Color.PRIM),
        Pixel(4,3, Color.PRIM),
        ],
    }

def get_display():
    return Display.get_display()

class Display:

    display = None

    @classmethod
    def get_display(cls):
        if cls.display:
            return cls.display

        cls.display = Display()
        return cls.display

    def __init__(self):
        self.strip = Adafruit_NeoPixel(
            LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS
        )
        # Intialize the library (must be called once before other functions).
        self.strip.begin()

        self.colors = {
            Color.PRIM: rpi_ws281x.Color(255, 255, 255),
            Color.SEC: rpi_ws281x.Color(125, 125, 125),
        }

        self.current_list = []

    def _pix_pos(self, pix):
        pos = 120

        x = pix.x
        y = pix.y

        if y > 7:
            pos = 248
            y -= 8

        pos -= x * 8
        pos += y

        return pos

    def show(self, pix_list):
        black = rpi_ws281x.Color(0,0,0)
        for pix in self.current_list:
            pos = self._pix_pos(pix)
            self.strip.setPixelColor(pos, black)

        for pix in pix_list:
            pos = self._pix_pos(pix)
            color = self.colors[pix.color]

            self.strip.setPixelColor(pos, color)
        self.current_list = pix_list

        self.strip.show()
