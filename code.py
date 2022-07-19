# Tested with:
# Adafruit MatrixPortal M4: https://www.adafruit.com/product/4745
# Adafruit 64x32 RGB LED Matrix: https://www.adafruit.com/product/2278 

import adafruit_display_text.label
import board
import busio
import displayio
import framebufferio
import neopixel
import rgbmatrix
import terminalio
import time

from adafruit_esp32spi import adafruit_esp32spi
from adafruit_esp32spi import adafruit_esp32spi_wifimanager
from digitalio import DigitalInOut
from secrets import secrets

# Initialize display (64x32)
displayio.release_displays()
matrix = rgbmatrix.RGBMatrix(
    width = 64,
    bit_depth = 4,
    rgb_pins = [
        board.MTX_R1,
        board.MTX_G1,
        board.MTX_B1,
        board.MTX_R2,
        board.MTX_G2,
        board.MTX_B2
    ],
    addr_pins = [
        board.MTX_ADDRA,
        board.MTX_ADDRB,
        board.MTX_ADDRC,
        board.MTX_ADDRD
    ],
    clock_pin = board.MTX_CLK,
    latch_pin = board.MTX_LAT,
    output_enable_pin = board.MTX_OE
)
display = framebufferio.FramebufferDisplay(matrix)

# Loading screen
bitmap_loading = displayio.OnDiskBitmap("bmp/loading.bmp")
background_loading = displayio.TileGrid(bitmap_loading, pixel_shader = bitmap_loading.pixel_shader)
group_loading = displayio.Group()
group_loading.append(background_loading)
display.show(group_loading)

# Initialize WiFi (enter credentials in secrets.py)
esp32_cs = DigitalInOut(board.ESP_CS)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)
status_light = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness = 0.2) 
wifi_mgr = adafruit_esp32spi_wifimanager.ESPSPI_WiFiManager(esp, secrets, status_light)

# BTC screen
bitmap_btc = displayio.OnDiskBitmap("bmp/BTC.bmp")
background_btc = displayio.TileGrid(bitmap_btc, pixel_shader = bitmap_btc.pixel_shader)
label_btc_ticker = adafruit_display_text.label.Label(terminalio.FONT, x = 43, y = 7, text = "BTC", color = 0xFF8800) # Orange
label_btc_dollar = adafruit_display_text.label.Label(terminalio.FONT, x = 25, y = 23, text = "$", color = 0xFF8800) # Orange
label_btc_price = adafruit_display_text.label.Label(terminalio.FONT, x = 31, y = 23, text = "00000")
group_btc = displayio.Group()
group_btc.append(background_btc)
group_btc.append(label_btc_ticker)
group_btc.append(label_btc_dollar)
group_btc.append(label_btc_price)
price_btc = 99999

# ETH screen
bitmap_eth = displayio.OnDiskBitmap("bmp/ETH.bmp")
background_eth = displayio.TileGrid(bitmap_eth, pixel_shader = bitmap_eth.pixel_shader)
label_eth_ticker = adafruit_display_text.label.Label(terminalio.FONT, x = 43, y = 7, text = "ETH", color = 0x800080) # Purple
label_eth_dollar = adafruit_display_text.label.Label(terminalio.FONT, x = 31, y = 23, text = "$", color = 0x800080) # Purple
label_eth_price = adafruit_display_text.label.Label(terminalio.FONT, x = 37, y = 23, text = "0000")
group_eth = displayio.Group()
group_eth.append(background_eth)
group_eth.append(label_eth_ticker)
group_eth.append(label_eth_dollar)
group_eth.append(label_eth_price)
price_eth = 9999

# Fetch prices using Binance API
def fetch_prices(wifi_mgr):
    try:
        response = wifi_mgr.get("https://api.binance.com/api/v3/ticker/price?symbols=[\"BTCUSDT\",\"ETHUSDT\"]")
        json = response.json()
        price_btc = int(float(json[0]["price"]))
        price_eth = int(float(json[1]["price"]))
        response.close()
        return price_btc, price_eth
    except OSError:
        wifi_mgr.reset()
        return 99999, 9999

# Fetch prices, update variables and sleep ~6 seconds
def update(wifi_mgr, label_btc, price_btc_last, label_eth, price_eth_last):
    price_btc_new, price_eth_new = fetch_prices(wifi_mgr)
    label_btc.text = str(price_btc_new)
    label_eth.text = str(price_eth_new)
    if (price_btc_new > price_btc_last):
        label_btc.color = 0x00FF00 # Green
    elif (price_btc_new < price_btc_last):
        label_btc.color = 0xFF0000 # Red
    if (price_eth_new > price_eth_last):
        label_eth.color = 0x00FF00 # Green
    elif (price_eth_new < price_eth_last):
        label_eth.color = 0xFF0000 # Red
    time.sleep(2)
    label_btc.color = 0xFFFFFF # White
    label_eth.color = 0xFFFFFF # White
    time.sleep(4)
    return price_btc_new, price_eth_new

# Main loop: Update prices every -6 seconds, change screen every ~30 seconds
state = 0
while True:
    if state == 0:
        display.show(group_btc)
        state = 1
    elif state == 1:
        display.show(group_eth)
        state = 0
    for i in range(5):
        price_btc, price_eth = update(wifi_mgr, label_btc_price, price_btc, label_eth_price, price_eth)