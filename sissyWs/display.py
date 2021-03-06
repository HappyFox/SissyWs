import collections
import enum

try:
    import rpi_ws281x
except ImportError:
    rpi_ws281x = None

import blessed

import sissyWs
import sissyWs.display


class Color(enum.Enum):
    PRIM = 1
    SEC = 2


Point = collections.namedtuple("Point", ["x", "y"])


class Pixel:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def pos(self, offset=None):
        if offset:
            x = self.x + offset.x
            y = self.y + offset.y
            return Point(x, y)
        return Point(self.x, self.y)


Face = collections.namedtuple("Face", ["eyes", "rest"])


FACES = {
    "😐": Face(
        [
            Pixel(3, 3, Color.PRIM),
            Pixel(3, 4, Color.PRIM),
            Pixel(3, 2, Color.PRIM),
            Pixel(4, 3, Color.PRIM),
            Pixel(2, 3, Color.PRIM),
            Pixel(12, 3, Color.PRIM),
            Pixel(12, 4, Color.PRIM),
            Pixel(12, 2, Color.PRIM),
            Pixel(13, 3, Color.PRIM),
            Pixel(11, 3, Color.PRIM),
        ],
        [
            Pixel(5, 13, Color.PRIM),
            Pixel(6, 13, Color.PRIM),
            Pixel(7, 13, Color.PRIM),
            Pixel(8, 13, Color.PRIM),
            Pixel(9, 13, Color.PRIM),
            Pixel(10, 13, Color.PRIM),
        ],
    ),
    "😖": Face(
        [
            Pixel(3, 3, Color.PRIM),
            Pixel(3, 4, Color.PRIM),
            Pixel(3, 2, Color.PRIM),
            Pixel(4, 3, Color.PRIM),
            Pixel(2, 3, Color.PRIM),
            Pixel(12, 3, Color.PRIM),
            Pixel(12, 4, Color.PRIM),
            Pixel(12, 2, Color.PRIM),
            Pixel(13, 3, Color.PRIM),
            Pixel(11, 3, Color.PRIM),
        ],
        [
            Pixel(3, 12, Color.PRIM),
            Pixel(4, 11, Color.PRIM),
            Pixel(5, 12, Color.PRIM),
            Pixel(6, 11, Color.PRIM),
            Pixel(7, 12, Color.PRIM),
            Pixel(8, 11, Color.PRIM),
            Pixel(9, 12, Color.PRIM),
            Pixel(10, 11, Color.PRIM),
            Pixel(11, 12, Color.PRIM),
            Pixel(12, 11, Color.PRIM),
        ],
    ),
    "😀": Face(
        [
            Pixel(3, 3, Color.PRIM),
            Pixel(3, 4, Color.PRIM),
            Pixel(3, 2, Color.PRIM),
            Pixel(4, 3, Color.PRIM),
            Pixel(2, 3, Color.PRIM),
            Pixel(12, 3, Color.PRIM),
            Pixel(12, 4, Color.PRIM),
            Pixel(12, 2, Color.PRIM),
            Pixel(13, 3, Color.PRIM),
            Pixel(11, 3, Color.PRIM),
        ],
        [
            Pixel(3, 11, Color.PRIM),
            Pixel(4, 11, Color.PRIM),
            Pixel(5, 11, Color.PRIM),
            Pixel(6, 11, Color.PRIM),
            Pixel(7, 11, Color.PRIM),
            Pixel(8, 11, Color.PRIM),
            Pixel(9, 11, Color.PRIM),
            Pixel(10, 11, Color.PRIM),
            Pixel(11, 11, Color.PRIM),
            Pixel(12, 11, Color.PRIM),
            Pixel(3, 12, Color.PRIM),
            Pixel(12, 12, Color.PRIM),
            Pixel(3, 13, Color.PRIM),
            Pixel(12, 13, Color.PRIM),
            Pixel(4, 14, Color.PRIM),
            Pixel(5, 14, Color.PRIM),
            Pixel(6, 14, Color.PRIM),
            Pixel(7, 14, Color.PRIM),
            Pixel(8, 14, Color.PRIM),
            Pixel(9, 14, Color.PRIM),
            Pixel(10, 14, Color.PRIM),
            Pixel(11, 14, Color.PRIM),
        ],
    ),
}


LOOK_OFFSETS = {
    "↖": Point(-1, -1),
    "↑": Point(0, -1),
    "↗": Point(1, -1),
    "→": Point(1, 0),
    "↘": Point(1, 1),
    "↓": Point(0, 1),
    "↙": Point(-1, 1),
    "←": Point(-1, 0),
    "⬤": Point(0, 0),
}


def get_display():
    if rpi_ws281x:
        return NeoDisplay.get_display()
    return TermDisplay.get_display()


class Display:

    display = None

    @classmethod
    def get_display(cls):
        if cls.display:
            return cls.display

        cls.display = cls()
        return cls.display

    def __init__(self):
        self.colors = {
            Color.PRIM: (255, 255, 255),
            Color.SEC: (125, 125, 125),
        }

        self.current_display = set()
        self.current_face = None
        self.current_face_offset = Point(0, 0)

    def add_pix_pending_list(self, pix_list, offset=Point(0, 0)):
        for pix in pix_list:
            color = self.colors[pix.color]

            position = pix.pos(offset)
            self.current_display.add(position)
            self.set_pix(position.x, position.y, color)

    def clear(self):
        for pix in self.current_display:
            self.clear_pix(pix.x, pix.y)

        self.current_display.clear()

    def close(self):
        pass

    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        pass

    def look_left(self, direction):
        print(direction)

    def set_primary_color(self, color):
        self.colors[Color.PRIM] = color
        self.draw_face()

    def set_secondary_color(self, color):
        self.colors[Color.SEC] = color
        self.draw_face()

    def show_face(self, face_key):
        self.current_face = sissyWs.display.FACES[face_key]
        self.draw_face()

    def draw_face(self):
        self.clear()
        self.add_pix_pending_list(self.current_face.eyes, self.current_face_offset)
        self.add_pix_pending_list(self.current_face.rest)
        self.show()

    def look_direction(self, direction):
        self.current_face_offset = LOOK_OFFSETS[direction]
        self.draw_face()

    def look_clear(self):
        self.current_face_offset = Point(0, 0)
        self.draw_face()

    def show(self):
        raise NotImplementedError()


class TermDisplay(Display):

    SIZE_X = 16
    SIZE_Y = 16

    def __init__(self):
        Display.__init__(self)
        self.term = blessed.Terminal()

        self.pending_text = ""

    def _draw_border(self):
        for idx in range(self.SIZE_X + 2):  # plus 2 for the border
            self.set_pix(idx, 0, (122, 245, 0), False)
            self.set_pix(idx, self.SIZE_Y + 1, (122, 245, 0), False)
        for idx in range(self.SIZE_Y + 2):  # plus 2 for the border
            self.set_pix(0, idx, (122, 245, 0), False)
            self.set_pix(self.SIZE_X + 1, idx, (122, 245, 0), False)
        self.show()

    def _move(self, x, y, adjusted=True):
        if adjusted:
            x += 1
            y += 1
        self.pending_text += self.term.move_xy(x, y)

    def clear_pix(self, x, y, adjusted=True):
        self._move(x, y, adjusted)
        self.pending_text += " "

    def __enter__(self):
        print(self.term.enter_fullscreen, end="", flush=True)
        print(self.term.hide_cursor, end="", flush=True)
        self.clear()
        self._draw_border()

    def __exit__(self, type, value, traceback):
        print(self.term.normal_cursor, end="", flush=True)
        print(self.term.exit_fullscreen, end="", flush=True)

    def set_pix(self, x, y, color, adjusted=True):
        self._move(x, y, adjusted)
        self.pending_text += self.term.color(self.term.rgb_downconvert(*color))
        self.pending_text += "█"

    def show(self):
        print(self.pending_text, end="", flush=True)


class NeoDisplay(Display):
    # LED strip configuration:
    LED_COUNT = 256  # 12        # Number of LED pixels.
    LED_PIN = 12  # GPIO pin connected to the pixels (must support PWM!).
    LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA = 10  # DMA channel to use for generating signal (try 10)
    LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
    # True to invert the signal (when using NPN transistor level shift)
    LED_INVERT = False

    def __init__(self):
        Display.__init__(self)
        self.strip = rpi_ws281x.Adafruit_NeoPixel(
            self.LED_COUNT,
            self.LED_PIN,
            self.LED_FREQ_HZ,
            self.LED_DMA,
            self.LED_INVERT,
            self.LED_BRIGHTNESS,
        )
        # Intialize the library (must be called once before other functions).
        self.strip.begin()

    def _pix_pos(self, x, y):
        pos = 120

        if y > 7:
            pos = 248
            y -= 8

        pos -= x * 8
        pos += y

        return pos

    def clear_pix(self, x, y):
        black = rpi_ws281x.Color(0, 0, 0)
        pos = self._pix_pos(x, y)
        self.strip.setPixelColor(pos, black)

    def set_pix(self, x, y, color):
        pos = self._pix_pos(x, y)
        rpi_color = rpi_ws281x.Color(*color)
        self.strip.setPixelColor(pos, rpi_color)

    def show(self):
        self.strip.show()
