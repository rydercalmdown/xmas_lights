import requests
import neopixel
import board
import time
import random


total_pixels = 550
lower_bank_start = 250
inactivity_timeout = []
last_known_state = [[] for x in range(total_pixels)]
all_pixels = neopixel.NeoPixel(
    board.D18,
    total_pixels,
    brightness=1,
    auto_write=False,
    pixel_order=neopixel.RGB)


def flash_bank(upper=True, num_times=3, delay=0.2):
    if upper:
        pixel_bank = range(0, lower_bank_start - 1)
    else:
        pixel_bank = range(lower_bank_start, total_pixels - 1)
    for _ in range(0, num_times):
        for i in pixel_bank:
            all_pixels[i] = [255, 255, 255]
        all_pixels.show() 
        for i in pixel_bank:
            all_pixels[i] = [0, 0, 0]
        all_pixels.show()
        time.sleep(delay)


def wigwag_vertical(num_times=10, delay=1):
    primary = [255, 255, 255]
    secondary = [0, 0, 0]
    lower = range(0, lower_bank_start - 1)
    upper = range(lower_bank_start, total_pixels - 1)
    for _ in range(0, num_times):
        for i in upper:
            all_pixels[i] = primary
        for i in lower:
            all_pixels[i] = secondary
        all_pixels.show()
        time.sleep(delay)
        for i in upper:
            all_pixels[i] = secondary
        for i in lower:
            all_pixels[i] = primary
        all_pixels.show()
        time.sleep(delay)


def get_led_array():
    """Return the LED array"""
    url = "https://lights.rydercalmdown.com/state/"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()


def blue_white():
    """ """
    for i in range(0, lower_bank_start):
        all_pixels[i]


def flash_leds(num_times=5, delay=0.1):
    """Flashes all the LEDs"""
    for _ in range(0, num_times):
        all_pixels.fill((255, 255, 255))
        all_pixels.show()
        time.sleep(delay)
        all_pixels.fill((0, 0, 0))
        all_pixels.show()
        time.sleep(delay)


def get_standard_colours():
    """Returns a dictionary of colours"""
    return {
        'red': (255, 0, 0),
        'yellow': (255, 150, 0),
        'green': (0, 255, 0),
        'cyan': (0, 255, 255),
        'blue': (0, 0, 255),
        'purple': (180, 0, 255),
    }


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b)


def rainbow_cycle(num_times=1):
    for _ in range(0, num_times):
        for j in range(255):
            for i in range(0, lower_bank_start - 1):
                pixel_index = (i * 256 // lower_bank_start - 1) + j
                all_pixels[i] = wheel(pixel_index & 255)
            all_pixels.show()


def explode_from_centre(num_times=1):
    """Explode from the centre"""

    def set_pixel_colour(rgb, halfway_point, i, extra=0):
        try:
            diminisher = round(1-(extra*0.1), 1)
            rgb_calc = [int(round(x*diminisher)) for x in rgb]
            if extra >= 9:
                rgb_calc = [0, 0, 0]
            all_pixels[halfway_point + i - extra] = rgb_calc
            all_pixels[halfway_point - i + extra] = rgb_calc
        except IndexError:
            pass

    for color, rgb in get_standard_colours().items():
        halfway_point = round(total_pixels / 2)
        all_pixels[halfway_point] = rgb
        all_pixels.show()
        for i in range(0, halfway_point):
            for x in range(1, 10):
                set_pixel_colour(rgb, halfway_point, i, x)
            all_pixels.show()


def rainbow_chase(num_times=1):
    """Rainbow chase"""
    original_standard = [value for key, value in get_standard_colours().items()]
    standard_colours = []
    multiplier = 2
    for x in range(0, 1):
        for x in original_standard:
            standard_colours.append(x)

    def set_pixel_colour(rgb, offset, i, extra=0):
        """Determine's the pixels colour"""
        try:
            factor = extra
            diminisher = round(1-(factor*0.1), 1)
            rgb_calc = [int(round(x*diminisher)) for x in rgb]
            if extra >= 9:
                rgb_calc = [0, 0, 0]
            all_pixels[offset + i - extra] = rgb_calc
        except IndexError:
            pass

    for i in range(0, total_pixels - 1):
        for offset in range(0, len(standard_colours) - 1):
            for extra in range(1, 10):
                rgb = standard_colours[offset]
                set_pixel_colour(rgb, offset*20, i, extra)
        all_pixels.show()


def fast_chase(bar_size=5):
    for i in range(0, total_pixels):
        if (i % 2 == 0):
            rgb = [255, 255, 255]
            all_pixels[i] = rgb
            if i != 0:
                all_pixels[i - 1] = rgb
                all_pixels[i - 2] = [0, 0, 0]
                all_pixels[i - 3] = [0, 0, 0]
            all_pixels.show()


def get_lighting_sections(num_sections):
    pixels_per_section = int(total_pixels / num_sections)
    sections = []
    for i in range(0, num_sections):
        section_lower = i * pixels_per_section
        section_upper = (i+1) * pixels_per_section
        s = range(section_lower, section_upper)
        sections.append(s)
    return sections


def pinwheel(num_times=4, delay=0.01, num_sections=10):
    """Pinwheel across quadrants"""
    sections = get_lighting_sections(num_sections)
    for _ in range(num_times):
        current = 0
        rgb = random.choice([v for k, v in get_standard_colours().items()])
        for _ in sections:
            all_pixels.fill([0, 0, 0])
            for i in sections[current]:
                all_pixels[i] = rgb
            all_pixels.show()
            time.sleep(delay)
            current += 1


def call_the_police(num_times=5):
    """Red, blue, white flashes"""
    delay = 0.01
    sections = get_lighting_sections(10)
    colours = [[255, 0, 0], [0, 0, 255], [150, 150, 150]]
    for _ in range(num_times):
        for colour in colours:
            for i in sections[1]:
                all_pixels[i] = colour
            all_pixels.show()
            time.sleep(delay)
        all_pixels.fill([0, 0, 0])
        all_pixels.show()
        time.sleep(delay)
        for colour in colours:
            for i in sections[4]:
                all_pixels[i] = colour
            all_pixels.show()
            time.sleep(delay)
        all_pixels.fill([0, 0, 0])
        all_pixels.show()
        time.sleep(delay)


def colour_flash(num_times=2):
    upper_bank = range(0, lower_bank_start - 1)
    lower_bank = range(lower_bank_start, total_pixels - 1)
    for _ in range(0, num_times):
        for _, rgb in get_standard_colours().items():
            for i in upper_bank:
                all_pixels[i] = rgb
            for i in lower_bank:
                all_pixels[i] = [0, 0, 0]
            all_pixels.show()
            temp_bank = upper_bank
            upper_bank = lower_bank
            lower_bank = temp_bank
            time.sleep(0.15)
    all_pixels.fill([0, 0, 0])


def twinkle(num_times=50, delay=0.01, num_choices=10):
    """Explode from the centre"""
    all_pixels.fill([0, 0, 0])
    all_pixels.show()
    for _ in range(0, num_times):
        choices = [random.randint(0, total_pixels - 1) for x in range(0, num_choices)]
        for i in choices:
            brightness = random.randint(1, 255)
            all_pixels[i] = [brightness, brightness, brightness]
        all_pixels.show()
        time.sleep(delay)
        for i in choices:
            all_pixels[i] = [0, 0, 0]
        all_pixels.show()
        time.sleep(delay)


def shuffle(num_times=20):
    rgb = [0, 0, 255]
    rgb_opposite = [0, 0, 0]
    for _ in range(0, num_times):
        for i in range(0, total_pixels):
            if i % 2 == 0:
                all_pixels[i] = rgb
            else:
                all_pixels[i] = rgb_opposite
        all_pixels.show()
        time.sleep(0.2)
        rgb_temp = rgb
        rgb = rgb_opposite
        rgb_opposite = rgb_temp


def fade_out_all_pixels():
    """Fades out current pixels from their current value"""
    fade_cycles = 12
    for cycle in range(0, fade_cycles):
        for i in range(0, total_pixels):
            all_pixels[i] = [int(x*0.8) for x in all_pixels[i]]
        all_pixels.show()
    for i in range(0, total_pixels):
        all_pixels[i] = [0, 0, 0]
    all_pixels.show()
    time.sleep(0.5)


def do_feature(feature):
    """Entrypoint for doing a custom feature of the lights"""
    print('custom feature: {}'.format(feature))
    fade_out_all_pixels()
    if feature == 'flash':
        colour_flash()
    elif feature == 'chase':
        rainbow_chase()
    elif feature == 'twinkle':
        twinkle()
    elif feature == 'pinwheel':
        pinwheel()


def pulse(num_times=20):
    # TODO - fix
    """Pulses randomly"""
    for _ in range(num_times):
        num_choices = random.randint(5, 25)
        choices = [random.randint(0, total_pixels - 1) for x in range(0, num_choices)]
        # fade block up
        for p in range(1, 255):
            rgb = [p, p, p]
            for i in choices:
                all_pixels[i] = rgb
            all_pixels.show()
        # fade block down
        for p in list(range(1, 255)).reverse():
            rgb = [p, p, p]
            for i in choices:
                all_pixels[i] = rgb
            all_pixels.show()
        time.sleep(0.1)


def run_default():
    """Runs a short default animation while waiting"""
    print('timeout reached, running default')
    shuffle(5)
    print('finished')


def main():
    """Runs the application"""
    led_array = get_led_array()
    if led_array.get('feature'):
        do_feature(led_array['feature'])
        return
    has_state_changed = False
    for i, rgb in led_array.items():
        i = int(i)
        rgb = list(rgb)
        if last_known_state[i] != rgb:
            has_state_changed = True
        last_known_state[i] = rgb
    if has_state_changed:
        for i, rgb in led_array.items():
            i = int(i)
            rgb = list(rgb)
            all_pixels[i] = rgb
        all_pixels.show()
        inactivity_timeout.clear()
    else:
        inactivity_timeout.append(1)
        if len(inactivity_timeout) > 300:
            run_default()
    print(len(inactivity_timeout))


if __name__ == '__main__':
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print('exiting')
