import time
import os
import keyboard
'''
This is an emulator for my Rummy Score Keeper.
It uses the keyboard library to simulate pressing a 12-key keypad in real time
'''
def debounce(): time.sleep(.15)
def get_name(player_num: int) -> str:
    keys = ['2','3','4','5','6','7','8','9','0']
    nums = ['2','22','222','3','33','333','4','44','444','5','55','555','6','66','666','7','77','777','7777','8','88','888','9','99','999','9999']
    let_dict = {nums[i]: i+97 for i in range(len(nums))} 
    cur_name = ''               #letters input by user
    print('Player',player_num,' name:',cur_name) #prints the current name
    name_done = False           #indicates it the name is done (which is set to True once 'enter' is pressed)
    while not name_done:        #loops until enter is pressed
        cur_str = ''            #current string of numbers representing a letter
        key_done = False        #indicates if a key has been pressed
        while not key_done:     #loops until a key is pressed to do the appropriate action
            for k in keys:      #this is a way of saying or for every key in keys
                if keyboard.is_pressed(k):
                    cur_str += keyboard.read_key() #the input is added to current string
                    debounce()                #debounce
                    last_key = time.time()         #time last key was pressed to time out once no more keys are being pressed
            if keyboard.is_pressed('enter') and cur_name: name_done, key_done = True, True  #enter completes the name given at least 1 letter is typed
            if keyboard.is_pressed('backspace') and cur_name: 
                debounce()
                cur_name, key_done = cur_name[:-1], True  #deletes the last letter of the name
            if cur_str and time.time() - last_key > .5: key_done = True #time out also completes the key
        print(cur_str)  #print the current string (ex: 333)
        if cur_str in nums: #if the current string is in nums (aka if it's not backspace/enter/empty)
            if cur_name: cur_name += chr(let_dict[cur_str]) #adds the lowercase letters
            else: cur_name += chr(let_dict[cur_str] - 32) #capitalizes the first letter
        time.sleep(.5) #delays after printing the numbers
        os.system('cls') #clears the screen
        print('Player',player_num,' name:',cur_name) #prints the current name
    os.system('cls')
    return cur_name
def get_score(name:str) -> int:
    keys = ['1','2','3','4','5','6','7','8','9','0']
    cur_num = ''
    print(name,end='')
    print("'s score", cur_num)
    score_done = False
    while not score_done:
        for k in keys:
            if keyboard.is_pressed(k):
                os.system('cls')
                debounce()
                cur_num+=k
                print(name,end='')
                print("'s score", cur_num)
        if keyboard.is_pressed('backspace'): 
            debounce()
            cur_num = cur_num[:-1]
            os.system('cls')
            print(name,end='')
            print("'s score", cur_num)
        if keyboard.is_pressed('enter') and cur_num: 
            debounce()
            os.system('cls')
            return int(cur_num)
def splash_screen():
    print('Rummy Score Keeper')    #Prints start up screen
    time.sleep(2.5)                      #Waits 2.5 Seconds
    os.system('cls')    
def start_up() -> dict:
    #Getting # of players
    num_players = int(input('Enter # of players:'))   #prompts to enter num of players
    os.system('cls')
    # Prompts to get players names
    player_names = dict()
    for _ in range(num_players): 
        name = get_name(_+1)
        if name in player_names.keys(): #Will add a number starting at 1 and going up if any duplicate names (because I'm using a dictionary to keep score)
            n = 1
            while True:
                if name + str(n) not in player_names.keys(): 
                    player_names[name+str(n)] = 0
                    break
                n += 1
        else: player_names[name] = 0
    return player_names
def run_round(round:int) -> bool:
    print('Round', round,'in progress...')
    while True:
        if keyboard.is_pressed('enter'): break
        if keyboard.is_pressed('backspace'): return True
    os.system('cls')
    for player in player_names: player_names[player] += get_score(player)
    return False
def ending_sequence():
    for player in player_names:
        os.system('cls')
        print(player,end='')
        print("'s score:", player_names[player])
        time.sleep(1.5)

splash_screen()
while True:
    game_over = False
    while not game_over:
        player_names = start_up()
        r = 1
        while not game_over:
            game_over = run_round(r)
            r+= 1
        ending_sequence()




