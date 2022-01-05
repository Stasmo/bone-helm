# Manually copied from mu

import board
import busio
import math
import neopixel
import time
import storage
import json

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

from adafruit_led_animation.animation.sparkle import Sparkle
from adafruit_led_animation.animation.sparklepulse import SparklePulse
from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle
from adafruit_led_animation.animation.rainbow import Rainbow

BLERadio.name = "Bone helm"
ble = BLERadio()
ble.name = "Bone helm"
bleuart = UARTService()

bleuart_advertisement = ProvideServicesAdvertisement(bleuart)

ble.start_advertising(bleuart_advertisement)

RED = (255, 0, 0)
PURPLE = (255, 0, 255)
CLEAR = (0, 0, 0)

SELECTED_COLOR = CLEAR

NUM_PIXELS_EYES = 42
NUM_PIXELS_LEFT = 50
NUM_PIXELS_RIGHT = 49

FRAMES_PER_SECOND = 60
SECONDS_PER_FRAME = 1 / FRAMES_PER_SECOND
LAST_FRAME = time.monotonic()
BRIGHTNESS = 1
ORDER = neopixel.GRB

EYES = neopixel.NeoPixel(
    board.D10,
    NUM_PIXELS_EYES,
    pixel_order=ORDER,
    brightness=BRIGHTNESS,
    auto_write=False,
)
LEFT_HORN = neopixel.NeoPixel(
    board.D11, NUM_PIXELS_LEFT, brightness=BRIGHTNESS, auto_write=False
)
RIGHT_HORN = neopixel.NeoPixel(
    board.D9, NUM_PIXELS_RIGHT, brightness=BRIGHTNESS, auto_write=False
)


BLINK_DELAY = 0.5
BLINK_ON = False
BLINK_LAST_SWITCH = time.monotonic()

BREATH_ANIMATION_LENGTH_SECONDS = 4
BREATH_ANIMATION_PERCENTAGE_COMPLETE = 0

RADIATE_ANIMATION_LENGTH_SECONDS = 8
RADIATE_ANIMATION_PERCENTAGE_COMPLETE = 0

MAGMA_ANIMATION_RADIUS = 10
MAGMA_ANIMATION_SPEED = 4


WAVE_ANIMATION_SPEED = 1

uart = busio.UART(board.TX, board.RX, baudrate=115200)


def fill_all(color=RED):
    EYES.fill(color)
    LEFT_HORN.fill(color)
    RIGHT_HORN.fill(color)


def show_all():
    EYES.show()
    LEFT_HORN.show()
    RIGHT_HORN.show()


fill_all(SELECTED_COLOR)
show_all()


CURRENT_ANIMATION = "radiate"

def progress_animation():
    if CURRENT_ANIMATION == "blink":
        progress_blink_animation()
    if CURRENT_ANIMATION == "breath":
        progress_breath_animation()
    if CURRENT_ANIMATION == "radiate":
        progress_radiate_animation()
    if CURRENT_ANIMATION == "sparkle":
        progress_sparkle_animation()
    if CURRENT_ANIMATION == "sparkle_pulse":
        progress_sparkle_pulse_animation()
    if CURRENT_ANIMATION == "rainbow_sparkle":
        progress_rainbow_sparkle_animation()
    if CURRENT_ANIMATION == "magma":
        progress_magma_animation()
    if CURRENT_ANIMATION == "wave":
        progress_wave_animation()
    if CURRENT_ANIMATION == "rainbow":
        progress_rainbow_animation()


def dim_color(color, brightness):
    return (int(color[0] * brightness), int(color[1] * brightness), int(color[2] * brightness))


rainbow_speed = 0.01
rainbow_period = 5
rainbow_eyes = Rainbow(EYES, rainbow_speed, rainbow_period)
rainbow_left = Rainbow(LEFT_HORN, rainbow_speed, rainbow_period)
rainbow_right = Rainbow(RIGHT_HORN, rainbow_speed, rainbow_period)


def progress_rainbow_animation():
    rainbow_eyes.animate()
    rainbow_left.animate()
    rainbow_right.animate()


def progress_sparkle_animation():
    sparkle_eyes.animate()
    sparkle_left_horn.animate()
    sparkle_right_horn.animate()


def progress_sparkle_pulse_animation():
    sparkle_pulse_eyes.animate()
    sparkle_pulse_left_horn.animate()
    sparkle_pulse_right_horn.animate()


def progress_rainbow_sparkle_animation():
    rainbow_sparkle_eyes.animate()
    rainbow_sparkle_left_horn.animate()
    rainbow_sparkle_right_horn.animate()


def progress_breath_animation():
    global BREATH_ANIMATION_PERCENTAGE_COMPLETE
    BREATH_ANIMATION_PERCENTAGE_COMPLETE = (
        time.monotonic() % BREATH_ANIMATION_LENGTH_SECONDS
    ) / BREATH_ANIMATION_LENGTH_SECONDS
    sine_wave = math.sin(math.pi * BREATH_ANIMATION_PERCENTAGE_COMPLETE)

    fill_all(dim_color(SELECTED_COLOR, sine_wave))
    show_all()


def progress_radiate_animation():
    global RADIATE_ANIMATION_PERCENTAGE_COMPLETE
    RADIATE_ANIMATION_PERCENTAGE_COMPLETE = (
        time.monotonic() % RADIATE_ANIMATION_LENGTH_SECONDS
    ) / RADIATE_ANIMATION_LENGTH_SECONDS

    sine_wave = (1 + math.sin(math.pi * 2 * RADIATE_ANIMATION_PERCENTAGE_COMPLETE)) / 2
    new_color = dim_color(SELECTED_COLOR, 0.3 + sine_wave * 0.7)
    EYES.fill(new_color)
    EYES.show()

    for x in range(NUM_PIXELS_LEFT):
        if x < sine_wave * NUM_PIXELS_LEFT:
            LEFT_HORN[x] = new_color
        else:
            LEFT_HORN[x] = (10, 0, 0)
    max_left = math.floor(NUM_PIXELS_LEFT * sine_wave)
    if max_left < NUM_PIXELS_LEFT - 1:
        LEFT_HORN[max_left + 1] = dim_color(new_color, 0.5)
    if max_left < NUM_PIXELS_LEFT - 2:
        LEFT_HORN[max_left + 2] = dim_color(new_color, 0.25)
    if max_left < NUM_PIXELS_LEFT - 3:
        LEFT_HORN[max_left + 3] = dim_color(new_color, 0.1)
    LEFT_HORN.show()

    for x in range(NUM_PIXELS_RIGHT):
        if x < sine_wave * NUM_PIXELS_RIGHT:
            RIGHT_HORN[x] = new_color
        else:
            RIGHT_HORN[x] = (10, 0, 0)
    max_right = math.floor(NUM_PIXELS_RIGHT * sine_wave)
    if max_right < NUM_PIXELS_RIGHT - 1:
        RIGHT_HORN[max_right + 1] = dim_color(new_color, 0.5)
    if max_right < NUM_PIXELS_RIGHT - 2:
        RIGHT_HORN[max_right + 2] = dim_color(new_color, 0.25)
    if max_right < NUM_PIXELS_RIGHT - 3:
        RIGHT_HORN[max_right + 3] = dim_color(new_color, 0.1)
    RIGHT_HORN.show()


def progress_magma_animation():
    percentage = (time.monotonic() % (5 / MAGMA_ANIMATION_SPEED)) / (
        5 / MAGMA_ANIMATION_SPEED
    )
    for x in range(NUM_PIXELS_RIGHT):
        brightness = 0.25 + math.sin(math.pi * 2 * percentage + x) / 1.5
        RIGHT_HORN[NUM_PIXELS_RIGHT - x - 1] = dim_color(SELECTED_COLOR, brightness)
    for x in range(NUM_PIXELS_LEFT):
        brightness = 0.25 + math.sin(math.pi * 2 * percentage + x) / 1.5
        LEFT_HORN[NUM_PIXELS_LEFT - x - 1] = dim_color(SELECTED_COLOR, brightness)
    for x in range(NUM_PIXELS_EYES):
        brightness = 0.25 + math.sin(math.pi * 2 * percentage + x) / 1.5
        EYES[NUM_PIXELS_EYES - x - 1] = dim_color(SELECTED_COLOR, brightness)
    RIGHT_HORN.show()
    LEFT_HORN.show()
    EYES.show()


def progress_wave_animation():
    percentage = (time.monotonic() % (10 / WAVE_ANIMATION_SPEED)) / (
        10 / WAVE_ANIMATION_SPEED
    )
    for x in range(NUM_PIXELS_RIGHT):
        brightness = math.sin(math.pi * 2 * percentage + x / NUM_PIXELS_RIGHT)
        RIGHT_HORN[NUM_PIXELS_RIGHT - x - 1] = dim_color(SELECTED_COLOR, brightness)
    for x in range(NUM_PIXELS_LEFT):
        brightness = math.sin(math.pi * 2 * percentage + x / NUM_PIXELS_LEFT)
        LEFT_HORN[NUM_PIXELS_LEFT - x - 1] = dim_color(SELECTED_COLOR, brightness)
    for x in range(NUM_PIXELS_EYES):
        brightness = 0.5 + math.sin(math.pi * 2 * percentage) / 2
        EYES[x] = dim_color(SELECTED_COLOR, brightness)
    RIGHT_HORN.show()
    LEFT_HORN.show()
    EYES.show()


def progress_blink_animation():
    global BLINK_ON, BLINK_LAST_SWITCH
    if BLINK_LAST_SWITCH + BLINK_DELAY < time.monotonic():
        if BLINK_ON:
            fill_all(CLEAR)
        else:
            fill_all(SELECTED_COLOR)
        show_all()
        BLINK_ON = not BLINK_ON
        BLINK_LAST_SWITCH = time.monotonic()


def handle_ble():
    global CURRENT_ANIMATION, SELECTED_COLOR
    if not ble.connected:
        if not ble.advertising:
            ble.start_advertising(bleuart_advertisement)
        pass
    else:
        if bleuart.in_waiting:
            s = bleuart.readline()
            data = s.decode()
            if s.startswith("a:"):
                CURRENT_ANIMATION = data.replace("a:", "")
                save_settings()
            if s.startswith("b:"):
                new_brightness = float(data.replace("b:", ""))
                set_brightness(new_brightness)
                save_settings()
            if s.startswith("c:"):
                parts = data.replace("c:", "").split(",")
                SELECTED_COLOR = (int(parts[0]), int(parts[1]), int(parts[2]))
                save_settings()
            if s.startswith("d:"):
                print("Got debug message: " + data)
                bleuart.write(data.encode("utf-8"))
            if s.startswith("s:"):
                details = {
                    "animation": CURRENT_ANIMATION,
                    "brightness": BRIGHTNESS,
                    "color": SELECTED_COLOR,
                    "type": "details"
                }
                details_json = json.dumps(details)
                print(details_json)
                bleuart.write(details_json)


def set_brightness(new_brightness):
    LEFT_HORN.brightness = new_brightness
    RIGHT_HORN.brightness = new_brightness
    EYES.brightness = new_brightness

sparkle_speed = 0.5
num_sparkles = 10

sparkle_eyes = Sparkle(
    pixel_object=EYES,
    speed=sparkle_speed,
    color=SELECTED_COLOR,
    num_sparkles=num_sparkles,
)
sparkle_left_horn = Sparkle(
    pixel_object=LEFT_HORN,
    speed=sparkle_speed,
    color=SELECTED_COLOR,
    num_sparkles=num_sparkles,
)
sparkle_right_horn = Sparkle(
    pixel_object=RIGHT_HORN,
    speed=sparkle_speed,
    color=SELECTED_COLOR,
    num_sparkles=num_sparkles,
)

sparkle_pulse_speed = 0.2
sparkle_pulse_period = 0.5

sparkle_pulse_eyes = SparklePulse(
    pixel_object=EYES,
    speed=sparkle_pulse_speed,
    period=sparkle_pulse_period,
    color=SELECTED_COLOR,
)
sparkle_pulse_left_horn = SparklePulse(
    pixel_object=LEFT_HORN,
    speed=sparkle_pulse_speed,
    period=sparkle_pulse_period,
    color=SELECTED_COLOR,
)
sparkle_pulse_right_horn = SparklePulse(
    pixel_object=RIGHT_HORN,
    speed=sparkle_pulse_speed,
    period=sparkle_pulse_period,
    color=SELECTED_COLOR,
)


rainbow_sparkle_speed = 0.01
rainbow_sparkle_period = 5

rainbow_sparkle_eyes = RainbowSparkle(
    pixel_object=EYES,
    speed=rainbow_sparkle_speed,
    period=rainbow_sparkle_period,
)
rainbow_sparkle_left_horn = RainbowSparkle(
    pixel_object=LEFT_HORN,
    speed=rainbow_sparkle_speed,
    period=rainbow_sparkle_period,
)
rainbow_sparkle_right_horn = RainbowSparkle(
    pixel_object=RIGHT_HORN,
    speed=rainbow_sparkle_speed,
    period=rainbow_sparkle_period,
)

def read_settings():
    global CURRENT_ANIMATION, SELECTED_COLOR
    try:
        data = ""
        with open("/helmet_settings.txt", "r") as fp:
            data = fp.read()
        parts = data.split('@')
        print(str(parts))
        for part in parts:
            if part.startswith('a:'):
                CURRENT_ANIMATION = part.replace('a:', '')
            if part.startswith('b:'):
                new_brightness = float(part.replace('b:', ''))
                set_brightness(new_brightness)
            if part.startswith('c:'):
                new_color = part.replace('c:', '').replace('(','').replace(')','')
                SELECTED_COLOR = tuple(map(float, new_color.split(',')))
    except Exception as e:
        print(e)
        print('Could not read settings')

def save_settings():
    try:
        storage.remount("/", False)
        with open("/helmet_settings.txt", "w+") as fp:
            fp.write("a:" + CURRENT_ANIMATION + "@b:" + str(BRIGHTNESS) + "@c:" + str(SELECTED_COLOR))
    except Exception as e:
        print(e)
        print("Could not write to disk")
    finally:
        storage.remount("/", True)

read_settings()

while True:
    progress_animation()
    handle_ble()
    next_frame = LAST_FRAME + SECONDS_PER_FRAME
    time_to_wait = next_frame - time.monotonic()
    LAST_FRAME = next_frame
    if time_to_wait > 0:
        time.sleep(time_to_wait)
