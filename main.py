import board, digitalio
import displayio, terminalio
import adafruit_displayio_ssd1306
from adafruit_display_text import label
import time

# Setting up pins and keys
o1, o2 = digitalio.DigitalInOut(board.D12), digitalio.DigitalInOut(board.D11)
i1, i2 = digitalio.DigitalInOut(board.D10), digitalio.DigitalInOut(board.D9)
button_dict = {(o1, i1): '1', (o1, i2): '4',(o2, i1): '2', (o2, i2): '3'}
outputs = [o1, o2]
for o in outputs:
    o.direction = digitalio.Direction.OUTPUT
    o.value = False
inputs = [i1, i2]
for i in inputs:
    i.direction = digitalio.Direction.INPUT
    i.pull = digitalio.Pull.DOWN

'''
The debounce function is used after a button press is registered to prevent duplicate button presses from being read
'''
def debounce(): time.sleep(.15)

'''
The clear function takes in the splash which contains the contents of the oled screen and fills it with a black screen. It also has a nice fading effect.
'''
def clear(splash): 
    bitmap = displayio.Bitmap(128, 64, 1)
    palette = displayio.Palette(1)
    palette[0] = 0x000000 #Black

    background = displayio.TileGrid(bitmap, pixel_shader=palette, x=0, y=0)
    splash.append(background)

'''
The center function is used to center text on the oled by determining the size of the string centering it within the width of the oled
'''
def center(text_label):
    width = text_label.bounding_box[2]
    center_x = 128//2 - width//2
    return center_x

'''
the send_to_oled function takes in a string, a y position, and the splash screen and appends it to the splash. It also uses the center function to automatically center the text
'''
def send_to_oled(text, y_pos, splash):
    line = label.Label(terminalio.FONT, text = text, y = y_pos)
    line.x = center(line)
    splash.append(line)

'''
This is the splash screen for when the device turns on. 
'''
def splash_screen(splash):
    clear(splash)

    lines = ["Grace's", "Rummy", "Score Keeper", 'V2']

    y_pos = 10
    for line in lines:
        send_to_oled(line, y_pos, splash)
        y_pos += 15

'''
This function is to mimic the emulator code that I wrote. The corresponding function would be keyboard.is_pressed(key). It returns true or false if the key is pressed
'''
def key_is_pressed(key:str):
    for o in outputs:
        o.value = True
        for i in inputs:
            if i.value and button_dict[(o, i)] == key: return True
        o.value = False
    return False

def get_player_ct(splash):
    string, string_y = 'Enter player count: ', 10
    send_to_oled(string, string_y, splash)
    send_to_oled('', 20, splash)
    cur_num = ''
    options = button_dict.values()
    num_done = False
    while not num_done:
        for key in options:
            if key_is_pressed(key):
                cur_num += key
                splash.pop()
                send_to_oled(cur_num, 20, splash)
                debounce()

def get_name(player_num:int) -> str:
    pass

def start_up(splash) -> dict:
    #get num of players
    clear(splash)

displayio.release_displays()                                                            #clears anything that would stop the program from running

i2c = board.I2C()                                                                       #Initialize I2C interface
print("I2C initialized successfully!")

display_bus = displayio.I2CDisplay(i2c, device_address=0x3c)                            #creates the display bus
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)         #creates the display 128x64 pixels with the display bus

splash = displayio.Group()                                                              #
display.root_group = splash                                                             #

#Starting the program
splash_screen(splash)
time.sleep(1.5)
clear(splash)
get_player_ct(splash)


while True:
    pass

# def check_buttons():
#     for o in outputs:
#         o.value = True
#         for i in inputs:
#             if i.value:
#                 debounce()
#                 print(button_dict[(o, i)])
#         o.value = False

# o1, o2 = digitalio.DigitalInOut(board.D12), digitalio.DigitalInOut(board.D11)
# i1, i2 = digitalio.DigitalInOut(board.D10), digitalio.DigitalInOut(board.D9)
# button_dict = {(o1, i1): 1, (o1, i2): 4,(o2, i1): 2, (o2, i2): 3}


# while True:
#     check_buttons()