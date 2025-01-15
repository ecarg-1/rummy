import board, digitalio
import displayio, terminalio
import adafruit_displayio_ssd1306
from adafruit_display_text import label
import time
'''
Things to fix:
- when entering player names, it times out to quickly
'''
# Setting up pins and keys
o1, o2, o3 = digitalio.DigitalInOut(board.D13), digitalio.DigitalInOut(board.D12), digitalio.DigitalInOut(board.D11)
i1, i2, i3, i4 = digitalio.DigitalInOut(board.D10), digitalio.DigitalInOut(board.D9), digitalio.DigitalInOut(board.D7), digitalio.DigitalInOut(board.D0)
button_dict = {(o1, i1): '1', (o2, i1): '2', (o3, i1): '3', (o1, i2): '4', (o2, i2): '5', (o3, i2): '6', (o1, i3): '7', (o2, i3): '8', (o3, i3): '9', (o1, i4): 'B', (o2, i4): '0', (o3, i4): 'E'}
outputs = [o1, o2, o3]
for o in outputs:
    o.direction = digitalio.Direction.OUTPUT
    o.value = False
inputs = [i1, i2, i3, i4]
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
    time.sleep(3)
    clear(splash)

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

'''
This function gets a numeric input that represents the number of players. You can press enter when done or backspace if a number was mistyped.
'''
def get_player_ct(splash) -> int:
    string, string_y = 'Enter player count: ', 10
    send_to_oled(string, string_y, splash)
    send_to_oled('', 20, splash)
    cur_num = ''
    options = button_dict.values()
    num_done = False
    while not num_done:
        for key in options:
            if key_is_pressed(key):
                if key == 'B' and cur_num: cur_num = cur_num[:-1]
                elif key == 'E': num_done = True
                else: cur_num += key
                splash.pop()
                send_to_oled(cur_num, 20, splash)
                debounce()
    clear(splash)
    return int(cur_num)

'''
This function updates the oled while the player number x types in their name. It returns their name in a string to later be put in a dictionary. You can use enter and backspace.
'''
get_name_keys = [str(i) for i in range(2, 10)]
get_name_nums = ['2','22','222','3','33','333','4','44','444','5','55','555','6','66','666','7','77','777','7777','8','88','888','9','99','999','9999']
let_dict = {get_name_nums[i]: i+97 for i in range(len(get_name_nums))} 
def get_name(splash, player_num:int) -> str:
    cur_name = ''
    send_to_oled('Player ' + str(player_num) + ' name:', 10, splash)
    send_to_oled('', 20, splash)
    send_to_oled('', 20, splash)
    name_done = False
    while not name_done:
        cur_str = ''
        key_done = False
        while not key_done:
            for key in button_dict.values():
                if key_is_pressed(key):
                    if key == 'E' and cur_name: name_done, key_done = True, True
                    if key == 'B' and cur_name: 
                        cur_name, key_done = cur_name[:-1], True
                    else: 
                        cur_str += key
                        last_key_press_time = time.time()
                    debounce()
                    splash.pop()
                    send_to_oled(cur_str, 20, splash)
                if cur_str and time.time() - last_key_press_time > .7: key_done = True
        if cur_str in get_name_nums:
            if cur_name: cur_name += chr(let_dict[cur_str])
            else: cur_name += chr(let_dict[cur_str] -32)
        splash.pop()
        send_to_oled(cur_name, 30, splash)
    clear(splash)
    return cur_name

'''
This function gets a player's score. It uses the players entered names to prompt them. You can press enter when done and backspace to delete.
'''
get_score_keys = [str(i) for i in range(10)]
def get_score(splash, name:str) -> int:
    cur_num = ''
    score_done = False
    send_to_oled(name +"'s score: ", 10, splash)
    send_to_oled('', 20, splash)
    while not score_done:
        for key in button_dict.values():
            if key_is_pressed(key):
                if key == 'B' and cur_num: cur_num = cur_num[:-1]
                elif key == 'E' and cur_num: score_done = True
                else: cur_num += key
                splash.pop()
                send_to_oled(cur_num, 20, splash)
                debounce()
    clear(splash)
    return int(cur_num)

'''
This function gets the player count and the player names.
'''
def start_up(splash) -> dict:
    #get num of players
    player_ct = get_player_ct(splash)
    player_names = dict()
    for _ in range(player_ct):
        name = get_name(splash, _+1)
        if name in player_names.keys(): #Will add a number starting at 1 and going up if any duplicate names (because I'm using a dictionary to keep score)
            n = 1
            while True:
                if name + str(n) not in player_names.keys(): 
                    player_names[name+str(n)] = 0
                    break
                n += 1
        else: player_names[name] = 0
    clear(splash)
    return player_names

'''
This function displays the round number and then gets each players score after the round is over. It returns a bool that determines if another round should be player or if the ending sequence should run.
'''
def run_round(splash, round_num:int) -> bool:
    send_to_oled('Round ' + str(round_num), 25, splash)
    send_to_oled('in progress...', 35, splash)
    while True:
        if key_is_pressed('E'): 
            debounce()
            break
        if key_is_pressed('B'): 
            clear(splash)
            debounce()
            return True
    clear(splash)
    for player in player_names: player_names[player] += get_score(splash, player)
    clear(splash)
    return False

'''
This function cycles through each player's score at the end.
'''
def ending_sequence(splash):
    send_to_oled('', 30, splash)
    for player in player_names:
        splash.pop()
        send_to_oled(player + "'s score: " + str(player_names[player]), 25, splash)
        time.sleep(2)
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
while True:
    game_over = False
    while not game_over:
        player_names = start_up(splash)
        r = 1
        while not game_over:
            game_over = run_round(splash, r)
            r+= 1
        while True:
            ending_sequence(splash)
            if key_is_pressed('E') : break
