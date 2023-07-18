import time
import machine
import neopixel


# LED-Streifen-Konfiguration
LED_PIN = 26
NUM_LEDS = 36  # Gesamtzahl der LEDs auf dem Streifen
NUM_COLORS = 360
color = 0
color2 = 360
# Anzahl der LEDs in jedem virtuellen Teil
stripe_1 = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11
stripe_2 = 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23
stripe_3 = 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35
# Initialisierung des LED-Streifens
strip = neopixel.NeoPixel(machine.Pin(LED_PIN), NUM_LEDS)
bright = {0: 0.2, 1: 0.5, 2: 0.7, 3: 1.0}

'''
H: Farbton (Hue) im Bereich von 0 bis 360 Grad
S: Sättigung (Saturation) im Bereich von 0 bis 1
V: Helligkeit (Value) im Bereich von 0 bis 1
'''


# Funktion zur Konvertierung von HSV zu RGB mit weicheren Übergängen
def hsv_to_rgb(h, s, v):
    h = h / NUM_COLORS * 360  # Anpassung des Farbwerts auf den Bereich von 0 bis 360 Grad
    r, g, b = 0, 0, 0
    # Berechnung der RGB-Werte mit weicheren Übergängen
    if s <= 0:
        r, g, b = v, v, v
    else:
        if h >= 360:
            h = 0
        h /= 60
        i = int(h)
        f = h - i
        p = v * (1 - s)
        q = v * (1 - (s * f))
        t = v * (1 - (s * (1 - f)))

        if i == 0:
            r, g, b = v, t, p
        elif i == 1:
            r, g, b = q, v, p
        elif i == 2:
            r, g, b = p, v, t
        elif i == 3:
            r, g, b = p, q, v
        elif i == 4:
            r, g, b = t, p, v
        else:
            r, g, b = v, p, q

    return int(r * 255), int(g * 255), int(b * 255)


def update_led():
    global color, color2
    add = 5
    while color < 360:
        for i in range(0, 5):
            time.sleep_ms(200)
            color += 1
            color %= 360
            farbe = hsv_to_rgb(color + (i * add), 1.0, bright.get(i, 1))
            strip[stripe_1[i]] = farbe
            strip[stripe_2[i]] = farbe
            strip[stripe_3[i]] = farbe
            strip.write()
        for i in range(11, 6, -1):
            time.sleep_ms(200)
            color2 -= 1
            color2 %= 360
            farbe = hsv_to_rgb(color2 - (add * (len(stripe_1) - i)), 1.0, 1.0)
            strip[stripe_1[i]] = farbe
            strip[stripe_2[i]] = farbe
            strip[stripe_3[i]] = farbe
            strip.write()
    color = color * - 1
    color2 = color2 * - 1


# Hauptprogramm
while True:
    update_led()
