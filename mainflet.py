import flet as ft
import json
from random import randint
from time import sleep

info_json = json.load(open("DogRaceSim/assets/data.json","rb"))
names = info_json['names']
colors = info_json['colors']
color_emojis = info_json['color_emojis']
race_pos_text = info_json['race_pos_text']
last_names = info_json['last_names']
first_names = info_json['first_names']
dog_list = []
dog_winner = []
print_text = ""

dog_color_flet = {
    "RED":ft.Colors.RED,
    "ORANGE":ft.Colors.ORANGE,
    "YELLOW":ft.Colors.YELLOW,
    "GREEN":ft.Colors.GREEN,
    "BLUE":ft.Colors.BLUE,
    "PURPLE":ft.Colors.PURPLE,
    "BROWN":ft.Colors.BROWN,
}

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

dog_preview_collumn = ft.Column(controls=[])
def show_dog_preview():
    i = 0
    for dog in dog_list:
        i += 1
        dog_preview_collumn.controls.append(
            ft.Card(
                ft.Row(
                    [
                        ft.Text(f"\n🐕 Dog #{i} - {dog['name']} {color_emojis[dog['color']]}\n",color=dog_color_flet[dog['color']]),
                        
                    ]
                ),
            )
        )

def main(page: ft.Page):

    page.fonts = {
        "roboto":"fonts/roboto.ttf",
        "VT323":"fonts/VT323.ttf",
        "Cascadia":"fonts/CascadiaMono.ttf"
    }


    def start_race(e,length=94):
        page.controls.clear()
        dog_control_list = ft.Column([])
        dog_positions = ft.Text("")
        for dog in dog_list:
            dog_control_list.controls.append(
                ft.Text(f'{color_emojis[dog['color']]}{" "*dog['position']}🐕{" "*(length-dog['position'])}🏁',size=20,style=ft.TextStyle(letter_spacing=-1))
            )
            dog_control_list.controls.append(
                ft.Text(f"{dog['name']} {color_emojis[dog['color']]}",color=dog_color_flet[dog['color']],size=10,font_family='roboto')
            )
        page.controls.append(dog_control_list)
        page.controls.append(dog_positions)
        page.update()
        while len(dog_winner) == 0:
            for i in range(len(dog_list)):
                dog = dog_list[i]
                if randint(0,5) < 3:
                    dog['position'] += 1
                    if dog['position'] == length:
                        dog_winner.append(dog['id'])
                elif randint(0,5) == 5:
                    if dog['position'] > 0:
                        dog['position'] -= 1
                dog_control_list.controls[i*2].value = f'{color_emojis[dog['color']]}{" "*dog['position']}🐕{" "*(length-dog['position'])}🏁'
                dog_control_list.controls[(i*2)+1].value = f"{" "*(2+(dog['position']*2))}{dog['name']}"

# Prepare dog positions
            dog_positions = sorted(dog_list, key=lambda x: x['position'], reverse=True)
            race_pos = 0
            race_positions_text = ""
            for dog in dog_positions:
                race_pos += 1
                race_positions_text += f"{race_pos_text[str(race_pos)]})🐕 {dog['name']} {color_emojis[dog['color']]} ({dog['position']} paces) \n"
                dog_list[dog['id']]['race_pos'] = race_pos
            print_text += race_positions_text
# Output text prepared
            dog_positions.value = print_text
            page.update()
            sleep(0.1)

    def main_menu(e):
        prepare_dogs()
        show_dog_preview()
        page.controls.clear()
        page.add(
            ft.Row([ft.Text("Todays racers!",size=40)],alignment=ft.MainAxisAlignment.CENTER),
            dog_preview_collumn,
            ft.Row(
                [
                    ft.Divider(height=10,thickness=10,visible=True),
                    ft.Button("Start race",scale=2,on_click=start_race)
                ],
                alignment = ft.MainAxisAlignment.CENTER
            )
            )
        page.update()

    page.add(
        ft.Button("Start 🐕🏁",on_click=main_menu))
    
ft.app(main,view=ft.AppView.FLET_APP)