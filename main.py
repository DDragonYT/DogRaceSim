import os;clear = lambda: os.system('cls');clear()
from random import randint
from time import sleep
from colorama import Fore
from colorama import Style
import json

clear()
info_json = json.load(open("DogRaceSim/assets/data.json","rb"))
names = info_json['names']
colors = info_json['colors']
color_emojis = info_json['color_emojis']
race_pos_text = info_json['race_pos_text']
last_names = info_json['last_names']
first_names = info_json['first_names']

color_text = {
    "RED":Fore.RED+Style.NORMAL,
    "ORANGE":Fore.YELLOW+Style.NORMAL,
    "YELLOW":Fore.LIGHTYELLOW_EX+Style.NORMAL,
    'GREEN':Fore.GREEN+Style.NORMAL,
    "BLUE":Fore.BLUE+Style.NORMAL,
    "PURPLE":Fore.MAGENTA+Style.DIM,
    'BROWN':Fore.YELLOW+Style.DIM,
    "PINK":Fore.LIGHTMAGENTA_EX+Style.NORMAL,
    "WHITE":Fore.WHITE+Style.NORMAL,
    "CYAN":Fore.CYAN+Style.NORMAL,
    "GREY":Fore.WHITE+Style.DIM,
}

dog_list = []

def prepare_dogs(max_dogs=5,min_dogs=7,nsfw=True):
    dog_list.clear()
    # dog_names = names.copy()
    if nsfw:
        dog_first_names = first_names.copy()
        dog_last_names = last_names.copy()
    else:
        dog_first_names = names.copy()
        dog_last_names = dog_first_names
    dog_colors = colors.copy()
    dogs_this_race = randint(max_dogs,min_dogs)
    for i in range(dogs_this_race):
        dog_name_words = []
        for var in [dog_first_names,dog_last_names]:
            name_id = randint(0,len(var)-1)
            dog_name_words.append(var[name_id])
            var.remove(var[name_id])
        dog_color = dog_colors[randint(0,len(dog_colors)-1)]
        dog_colors.remove(dog_color)

        dog = {
            'name':f"{dog_name_words[0]} {dog_name_words[1]}",
            'color': dog_color,
            'position': 0,
            'race_pos': 0,
            'id':i
        }

        dog_list.append(dog)

def dog_race(length=20):
    top_bar =f"{"-"*(round((length-10)/2))}THE RACE:{"-"*(round((length-10)/2))}\n"
    dog_winner = []
    key = "Todays Racers: \n"
    print("""The dog race is ready!
Our competitors today are:""")
    prepare_dogs()
    dog_positions = []
    i = 0
    for dog in dog_list:
        i+=1
        print(f"🐕 Dog #{i} - {dog['name']} {color_emojis[dog['color']]}")
        key += f"{color_emojis[dog['color']]} - {[dog['name']]}\n"
        dog_positions.append(0)

    print("Press enter to begin the race")
    input("")
    
    tick = 0
    while len(dog_winner) == 0:
        print_text = top_bar
        tick+=1

        for dog in dog_list:
            if tick > 30:
                if randint(0,5) < 3:
                    dog['position'] += 1
                    if dog['position'] == length:
                        dog_winner.append(dog['id'])
                elif randint(0,5) == 5:
                    if dog['position'] > 0:
                        dog['position'] -= 1
            print_text += f'{color_emojis[dog['color']]}{" "*dog['position']}🐕{" "*(length-dog['position'])}🏁\n{" "*(2+dog['position'])}{color_text[dog['color']]}{dog['name']}{Fore.WHITE+Style.NORMAL}\n'

        if tick < 25:
            print_text += f'{str(3-round(tick/10)).center(length)}\n'
        elif 25 < tick < 35:
            print_text += f"G{"O"*(tick-25)}!!\n".center(length)
        else:
            print_text +=" \n"
        print_text+= f'\n \n{"-"*length}\n'
        
        if tick > 30:
            dog_positions = sorted(dog_list, key=lambda x: x['position'], reverse=True)
            race_pos = 0
            race_positions_text = ""
            for dog in dog_positions:
                race_pos += 1
                race_positions_text += f"{race_pos_text[str(race_pos)]})🐕 {dog['name']} {color_emojis[dog['color']]} ({dog['position']} paces) \n"
                dog_list[dog['id']]['race_pos'] = race_pos
            print_text += race_positions_text

        clear()
        print(print_text.center(12))
        
        
        sleep(0.1)
    winner_text = ""
    for dog_id in dog_winner:
        if len(winner_text) != 0:
            winner_text += ", "
        winner_text += dog_list[dog_id]['name']
    winner_text += ' won the race!!!'
    print(winner_text)
    input("")
    input("")
    clear()
    dog_race(80)

if __name__ == "__main__":
    dog_race(80)