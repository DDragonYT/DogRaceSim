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

def prepare_dogs(max_dogs=7,min_dogs=7,nsfw=False):
    dog_list.clear()
    if nsfw:
        dog_first_names = first_names.copy()
        dog_last_names = last_names.copy()
    else:
        dog_first_names = names.copy()
        dog_last_names = dog_first_names
    dog_colors = colors.copy()
    dogs_this_race = randint(min_dogs,max_dogs)
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
    dog_preview_collumn.controls.clear()
    i = 0
    for dog in dog_list:
        i += 1
        dog_preview_collumn.controls.append(
            ft.Container(
                ft.Row(
                    [
                        ft.Text(f"\n🐕 Dog #{i} - {dog['name']} {color_emojis[dog['color']]}\n",color=dog_color_flet[dog['color']]),
                        
                    ]
                ),bgcolor=ft.Colors.GREY_900
            )
        )
def gen_winner_text():
    output_text = ""
    i = 1
    for id in dog_winner:
        i += 1
        dog = dog_list[id]
        output_text += dog['name']
        # if i != len(dog_winner):
        #     output_text += " and"
    output_text += " won the race!!"
    return output_text

def main(page: ft.Page):
    page.window.full_screen = True
    page.bgcolor = ft.Colors.GREY_800

    def start_race(e:ft.ControlEvent,length=94,dog_spacing=60,area_width=1300,area_height=455):
        animation_timing = e.control.data['animate_time']*10
        dog_speed = e.control.data['dog_speed']*5
        dog_winner.clear()
        position_spacing = (area_width/length)-2
        page.controls.clear()
        countdown = ft.Row([ft.Text("\n"*10+"Race starting in 3"+"\n"*10)],animate_scale=500,alignment=ft.MainAxisAlignment.CENTER,vertical_alignment=ft.VerticalAlignment.CENTER,run_alignment=ft.MainAxisAlignment.CENTER)
        dog_positions_control = ft.Container(
            ft.Text(""),
            width=area_width/2,
            height=(20*len(dog_list)),
            bgcolor=ft.Colors.GREY_900,
            shadow=ft.BoxShadow()
        )
        dog_control_list = ft.Container(
            ft.Stack(
            []),
            width=area_width,
            height=area_height,
            bgcolor=ft.Colors.GREY_900
        )
        for dog in dog_list:
            dog_control_list.content.controls.append(
                ft.Image('DogRaceSim/assets/dog_png.png',left=dog['position']*position_spacing,top=dog['id']*dog_spacing,scale=0.3,animate_position=animation_timing)
            )
        for dog in dog_list:
            dog_control_list.content.controls.append(
                ft.Text(dog['name'],color=dog_color_flet[dog['color']],left=dog['position']*position_spacing,top=(dog['id']*dog_spacing)+5,animate_position=animation_timing)
            )
        for dog in dog_list:
            dog_control_list.content.controls.append(
                ft.Text('🏁',left=area_width-120,top=dog['id']*dog_spacing+40,scale=2)
            )
            dog_control_list.content.controls.append(
                ft.Text(color_emojis[dog['color']],left=10,top=dog['id']*dog_spacing+40,scale=2)
            )
        page.controls.append(ft.Row([ft.Text("Race Display:",style=ft.TextThemeStyle.HEADLINE_MEDIUM,text_align=ft.TextAlign.CENTER)],alignment=ft.MainAxisAlignment.CENTER))
        page.controls.append(dog_control_list)
        bottom_row = ft.Row(
                    controls=[
                        ft.Column([ft.Text('The Positions:'),dog_positions_control],alignment=ft.MainAxisAlignment.CENTER),
                    ]
            )
        page.controls.append(bottom_row)
            
        dog_control_list.content.controls.append(countdown)
        page.update()
        dog_list_len = len(dog_list)
        sleep(0.3)
        for i in range(3):
            countdown.controls[0].value = f"{"\n"*10}Race starting in {3-i}{"\n"*10}"
            countdown.scale = 1+(i/2)
            page.update()
            sleep(1)
        countdown.controls[0].value = ""
        countdown.scale = 0
        while len(dog_winner) == 0:
            for i in range(len(dog_list)):
                dog = dog_list[i]
                if randint(0,5) < 3:
                    dog['position'] += 1
                    if dog['position'] == length:
                        dog_winner.append(dog['id'])
                        print(dog_control_list.content.controls[i].left)
                elif randint(0,5) == 5:
                    if dog['position'] > 0:
                        dog['position'] -= 1
                dog_control_list.content.controls[i].left = dog['position']*position_spacing
                dog_control_list.content.controls[i+dog_list_len].left = dog['position']*position_spacing
# Prepare dog positions
            dog_positions = sorted(dog_list, key=lambda x: x['position'], reverse=True)
            race_pos = 0
            race_positions_text = ""
            for dog in dog_positions:
                race_pos += 1
                if dog['position'] == dog_positions[0]['position']:
                    actual_race_pos = 1
                else:
                    actual_race_pos = race_pos
                race_positions_text += f"{race_pos_text[str(actual_race_pos)]})🐕 {dog['name']} {color_emojis[dog['color']]} ({dog['position']} paces) \n"
                dog_list[dog['id']]['race_pos'] = race_pos
# Output text prepared
            dog_positions_control.content.value = race_positions_text
            page.update()
            sleep(1/dog_speed)
        sleep(animation_timing/1000)
        bottom_row.controls.append(ft.Button("Next race 🏳️",on_click=main_menu))
        countdown.controls[0].value = f"{"\n"*10}{gen_winner_text()}{"\n"*10}"
        page.update()
        countdown.scale = 3
        page.update()

    def main_menu(e):
        show_dog_preview()
        dog_max = dog_number_max_input.value
        dog_min = dog_number_min_input.value
        animate_time = animate_time_input.value
        dog_speed = dog_speed_input.value
        prepare_dogs(max_dogs=dog_max,min_dogs=dog_min)
        show_dog_preview()
        page.controls.clear()
        page.add(
            ft.Row([ft.Text("Todays racers!",size=40)],alignment=ft.MainAxisAlignment.CENTER),
            dog_preview_collumn,
            ft.Row(
                [
                    ft.Divider(height=10,thickness=10,visible=True),
                    ft.Button("Start race",scale=2,on_click=start_race,data={
                        "animate_time":animate_time,
                        "dog_speed":dog_speed

                    })
                ],
                alignment = ft.MainAxisAlignment.CENTER
            )
            )
        page.update()
    animate_time_input =  ft.Dropdown(label="Animation time",options=[ft.DropdownOption(key=i,content=ft.Text(i)) for i in range(1,101)],value=100)
    dog_number_min_input =  ft.Dropdown(label="Min number of dogs",options=[ft.DropdownOption(key=i,content=ft.Text(i)) for i in range(1,8)],value=3)
    dog_number_max_input =  ft.Dropdown(label="Max number of dogs",options=[ft.DropdownOption(key=i,content=ft.Text(i)) for i in range(1,8)],value=7)
    dog_speed_input =  ft.Dropdown(label="Dog speed",options=[ft.DropdownOption(key=i,content=ft.Text(i)) for i in range(1,11)],value=3)



    page.add(
        ft.Row(
            [
                ft.Column(
                    [
                        ft.Text("That One Dog Racing game",theme_style=ft.TextTheme.title_large),
                        ft.Button("Start 🐕🏁",on_click=main_menu),
                        animate_time_input,
                        dog_number_max_input,
                        dog_number_min_input,
                        dog_speed_input
                    ],alignment=ft.MainAxisAlignment.CENTER
                )
            ],alignment=ft.MainAxisAlignment.CENTER
        )
        )
    
ft.app(main,view=ft.AppView.FLET_APP)