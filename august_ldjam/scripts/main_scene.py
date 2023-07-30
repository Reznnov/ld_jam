import pyglet
import math
import time
import webbrowser
import os
import json

# Задаем размеры экрана
screen_width = 1920
screen_height = 1080

# Создаем окно приложения
window = pyglet.window.Window(screen_width, screen_height)



class SettingsMenu:
    def __init__(self, background_image, parent_window):
        self.parent_window = parent_window
        self.background = pyglet.image.load(background_image)
        self.background_sprite = pyglet.sprite.Sprite(self.background, x=0, y=0)

        # Загрузка изображений кнопок
        settings_text_speed_image = pyglet.image.load('/home/reznnov/rabota/assets/images/main_menu_sprites/prefs_text_speed.png')
        settings_volume_of_music_image = pyglet.image.load('/home/reznnov/rabota/assets/images/main_menu_sprites/prefs_volume_of_music.png')
        settings_volume_of_sound_image = pyglet.image.load('/home/reznnov/rabota/assets/images/main_menu_sprites/prefs_volume_of_sounds.png')

        # Создание спрайтов для кнопок
        self.settings_text_speed_button = pyglet.sprite.Sprite(settings_text_speed_image, x=screen_width // 2 + 300, y=screen_height // 2 + 100)
        self.settings_volume_of_music_button = pyglet.sprite.Sprite(settings_volume_of_music_image, x=screen_width // 2 + 300, y=screen_height // 2)
        self.settings_volume_of_sound_button = pyglet.sprite.Sprite(settings_volume_of_sound_image, x=screen_width // 2 + 300, y=screen_height // 2 - 100)


    def draw(self):
        self.background_sprite.draw()

class AuthorsMenu:
    def __init__(self, background_image, parent_window):
        self.parent_window = parent_window
        self.background = pyglet.image.load(background_image)
        self.background_sprite = pyglet.sprite.Sprite(self.background, x=0, y=0)
        self.labels = []

        self.author_info = [
            'Имя Фамилия',  # Имя автора
            'Описание заслуг автора',
            'Ссылка на соцсеть 1',
            'Ссылка на соцсеть 2',
            'Ссылка на соцсеть 3',
            ]
        self.create_author_info(self.author_info, 100)


    def create_author_info(self, author_info, label_x):
        label_y = 750  # Начальное смещение по вертикали

        for info in author_info:
            label = pyglet.text.Label(info,
                                      font_name='Arial',
                                      font_size=30,
                                      x=label_x,
                                      y=label_y,
                                      anchor_x='left',
                                      anchor_y='top',
                                      color=(255, 255, 255, 255))
            self.labels.append(label)

            if author_info.index(info) == 0:
                label_y -= 100  # Отступ после имени автора
            elif author_info.index(info) == 1:
                label_y -= 50  # Отступ после описания заслуг автора
            else:
                label_y -= 50  # Отступ между ссылками

    def draw(self):
        self.background_sprite.draw()
        for label in self.labels:
            label.draw()


    def on_mouse_press(self, x, y, button, modifiers):
        for label in self.labels:
            # Проверяем, что клик был по ссылке на соцсеть 1
            if label.text == 'Ссылка на соцсеть 1':
                if label.x <= x <= label.x + 400 and label.y - 100 <= y <= label.y:
                    webbrowser.open('https://vk.com/redbreadstudio')



class MainMenu:
    def __init__(self, background_image):
        self.background_index = 0
        self.background = pyglet.image.load(background_image)
        self.background_sprite = pyglet.sprite.Sprite(self.background, x=0, y=0)
        self.authors_menu = None
        self.settings_menu = None
        self.show_authors = False
        self.show_settings = False

        # Загрузка изображений кнопок
        new_game_button_image = pyglet.image.load('/home/reznnov/rabota/assets/images/main_menu_sprites/start_idle.png')
        save_button_image = pyglet.image.load('/home/reznnov/rabota/assets/images/main_menu_sprites/load_idle.png')
        galery_button_image = pyglet.image.load('/home/reznnov/rabota/assets/images/main_menu_sprites/galery_idle.png')
        settings_button_image = pyglet.image.load('/home/reznnov/rabota/assets/images/main_menu_sprites/prefs_idle.png')
        credits_button_image = pyglet.image.load('/home/reznnov/rabota/assets/images/main_menu_sprites/credits_idle.png')
        q_button_image = pyglet.image.load('/home/reznnov/rabota/assets/images/main_menu_sprites/q_idle.png')

        new_game_button_image_hover = pyglet.image.load('/home/reznnov/rabota/assets/images/main_menu_sprites/start_hover.png')
        save_button_image_hover = pyglet.image.load('/home/reznnov/rabota/assets/images/main_menu_sprites/load_hover.png')
        galery_button_image_hover = pyglet.image.load('/home/reznnov/rabota/assets/images/main_menu_sprites/galery_hover.png')
        settings_button_image_hover = pyglet.image.load('/home/reznnov/rabota/assets/images/main_menu_sprites/prefs_hover.png')
        credits_button_image_hover = pyglet.image.load('/home/reznnov/rabota/assets/images/main_menu_sprites/credits_hover.png')
        q_button_image_hover = pyglet.image.load('/home/reznnov/rabota/assets/images/main_menu_sprites/q_hover.png')


        self.buttons_idle = []
        self.buttons_hover = []

        # Создание спрайтов для кнопок
        self.new_game_button = pyglet.sprite.Sprite(new_game_button_image,
                                                    x=screen_width // 2 + 300, y=screen_height // 2 + 100)
        self.save_button = pyglet.sprite.Sprite(save_button_image,
                                                x=screen_width // 2 + 300, y=screen_height // 2)
        self.settings_button = pyglet.sprite.Sprite(settings_button_image,
                                                    x=screen_width // 2 + 300, y=screen_height // 2 - 100)
        self.galery_button = pyglet.sprite.Sprite(galery_button_image,
                                                  x=screen_width // 2 + 300, y=screen_height // 2 - 200)
        self.credits_button = pyglet.sprite.Sprite(credits_button_image,
                                                   x=screen_width // 2 + 300, y=screen_height // 2 - 300)
        self.q_button = pyglet.sprite.Sprite(q_button_image,
                                             x=screen_width // 2 + 300, y=screen_height // 2 - 400)

        # Создание спрайтов для кнопок
        self.new_game_button_hover = pyglet.sprite.Sprite(new_game_button_image_hover,
                                                    x=screen_width // 2 + 300, y=screen_height // 2 + 100)
        self.save_button_hover = pyglet.sprite.Sprite(save_button_image_hover,
                                                x=screen_width // 2 + 300, y=screen_height // 2)
        self.settings_button_hover = pyglet.sprite.Sprite(settings_button_image_hover,
                                                    x=screen_width // 2 + 300, y=screen_height // 2 - 100)
        self.galery_button_hover = pyglet.sprite.Sprite(galery_button_image_hover,
                                                  x=screen_width // 2 + 300, y=screen_height // 2 - 200)
        self.credits_button_hover = pyglet.sprite.Sprite(credits_button_image_hover,
                                                   x=screen_width // 2 + 300, y=screen_height // 2 - 300)
        self.q_button_hover = pyglet.sprite.Sprite(q_button_image_hover,
                                             x=screen_width // 2 + 300, y=screen_height // 2 - 400)

        self.buttons_idle.append(self.new_game_button)
        self.buttons_idle.append(self.save_button)
        self.buttons_idle.append(self.galery_button)
        self.buttons_idle.append(self.settings_button)
        self.buttons_idle.append(self.credits_button)
        self.buttons_idle.append(self.q_button)

        self.buttons_hover.append(self.new_game_button_hover)
        self.buttons_hover.append(self.save_button_hover)
        self.buttons_hover.append(self.galery_button_hover)
        self.buttons_hover.append(self.settings_button_hover)
        self.buttons_hover.append(self.credits_button_hover)
        self.buttons_hover.append(self.q_button_hover)

        for button_sprite in self.buttons_hover:
            button_sprite.opacity = 0




    def on_mouse_motion(self, x, y, dx, dy):
        for button_sprite in self.buttons_idle:
            if button_sprite.x < x < button_sprite.x + button_sprite.width and \
                    button_sprite.y < y < button_sprite.y + button_sprite.height:
                button_sprite.opacity = 0
            else:
                button_sprite.opacity = 255

        for button_sprite in self.buttons_hover:
            if button_sprite.x < x < button_sprite.x + button_sprite.width and \
                    button_sprite.y < y < button_sprite.y + button_sprite.height:
                button_sprite.opacity = 255
            else:
                button_sprite.opacity = 0

    def on_key_press(self, symbol, modifiers):
        # Обработка событий нажатия клавиш

        # Пример обработки нажатия клавиши Esc для скрытия меню авторов
        if symbol == pyglet.window.key.Q and self.show_authors:
            self.hide_authors_menu()
        if symbol == pyglet.window.key.Q and self.show_settings:
            self.hide_settings_menu()



    def update(self, dt):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        if self.credits_button.x < x < self.credits_button.x + self.credits_button.width and \
                self.credits_button.y < y < self.credits_button.y + self.credits_button.height:
            self.show_authors_menu()
        if self.settings_button.x < x < self.settings_button.x + self.settings_button.width and \
                self.settings_button.y < y < self.settings_button.y + self.settings_button.height:
            self.show_settings_menu()
        if self.authors_menu and self.show_authors:
            self.authors_menu.on_mouse_press(x, y, button, modifiers)
        #if self.settings_menu and self.show_settings:
            #self.settings_menu.on_mouse_press(x, y, button, modifiers)

    def show_settings_menu(self):
        # создаём экземляр класса SettingsMenu
        self.settings_menu = SettingsMenu('/home/reznnov/rabota/assets/images/main_menu_sprites/prefs_bg.png', self)

        # меняем значение флаговой переменной
        self.show_settings = True

    def show_authors_menu(self):
        # Создаем экземпляр класса AuthorsMenu
        self.authors_menu = AuthorsMenu('/home/reznnov/rabota/assets/images/main_menu_sprites/credits_bg.png', self)

        # меняем значение флаговой переменной
        self.show_authors = True

    def draw(self):
        self.background_sprite.draw()
        for button_sprite in self.buttons_idle:
            button_sprite.draw()
        for button_sprite in self.buttons_hover:
            button_sprite.draw()  # добавь эту строку для отображения спрайтов с препиской _hover

        if self.show_authors and self.authors_menu:
            self.authors_menu.draw()
        if self.show_settings and self.settings_menu:
            self.settings_menu.draw()

    def hide_authors_menu(self):
        self.authors_menu = None
        self.show_authors = False

    def hide_settings_menu(self):
        self.settings_menu = None
        self.show_settings = False


class Scene:
    def __init__(self, background_image, character_images, character_coords, character_name=None, dialogue=None):
        # Создаем спрайты для заднего фона и персонажей
        self.background = pyglet.sprite.Sprite(background_image)

        self.characters = []
        for i in range(len(character_images)):
            character = pyglet.sprite.Sprite(character_images[i])
            character.x = character_coords[i][0]
            character.y = character_coords[i][1]
            self.characters.append(character)

        # Сохраняем диалоги для данной сцены
        self.dialogues = dialogue
        self.dialogue_index = 0 if dialogue else None

        # Создаем метку для отображения текста и имени персонажа
        self.label = pyglet.text.Label(self.dialogues[0],
                                       font_name='Arial',
                                       font_size=24,
                                       x=175, y=275,
                                       anchor_x='left', anchor_y='bottom')
        self.character_name = character_name
        if character_name:
            self.name_label = pyglet.text.Label(self.character_name,
                                                font_name='Arial',
                                                font_size=24,
                                                x=150, y=325,
                                                color=(59, 168, 173, 255),
                                                anchor_x='left', anchor_y='bottom')

        # Создаем спрайт для оверлея
        self.add_overlay()

    def add_overlay(self):
        # Создаем спрайт для оверлея
        overlay = pyglet.image.SolidColorImagePattern((0, 0, 0, 128)).create_image(window.width, window.height // 3)
        self.overlay = pyglet.sprite.Sprite(overlay, x=0, y=0)

    def hide_overlay(self):
        self.overlay.opacity = 0

    def hide_text(self):
        self.label.text = ""

    def draw(self):
        # Отображаем спрайты и метку
        self.background.draw()
        for character in self.characters:
            character.draw()
        self.overlay.draw()  # Отображаем оверлей
        if self.character_name:
            self.name_label.draw()
        self.label.draw()



main_menu = MainMenu('/home/reznnov/rabota/assets/images/main_menu_sprites/bg_main_menu.png')
all_scenes = []
scenes = []


# Индекс текущей сцены
current_part = 0
current_scene = 0
current_dialogue = 0
game_state = {'current_part': 0, 'current_scene': 0, 'current_dialogue': 0}


index = 0
show_authors_menu = False



def start_new_game():
    global game_state
    game_state = {'current_part': 0, 'current_scene': 0, 'current_dialogue': 0}
    return game_state

def continue_game():
    global game_state, current_part, current_scene, current_dialogue
    # Загрузка сохраненного состояния игры
    if os.path.getsize("../assets/config/save_file.txt") != 0:
        with open('../assets/config/save_file.txt', "r") as f:
            game_state = json.load(f)
            current_part = game_state["current_part"]
            current_scene = game_state["current_scene"]
            current_dialogue = game_state['current_dialogue']
    else:
        current_part = 0
        current_scene = 0
        current_dialogue = 0
    return game_state

def save_game(game_state):
    with open('../assets/config/save_file.txt', 'w') as f:
        json.dump(game_state, f)


def load_game():
    with open('../assets/config/save_file.txt', 'r') as f:
        game_state = json.load(f)
        return game_state


def set_windowed():
    global window
    window.set_fullscreen(False)
    window.set_size(screen_width, screen_height)

def set_fullscreen():
    global window
    window.set_fullscreen(True)

@window.event()
def on_key_press(symbol, modifiers):
    global index
    if symbol == pyglet.window.key.F and index % 2 == 0:
        set_fullscreen()
        index += 1
    elif symbol == pyglet.window.key.F and index % 2 != 0:
        set_windowed()
        index += 1
    main_menu.on_key_press(symbol, modifiers)


@window.event
def on_draw():
    window.clear()
    main_menu.draw()
    # Добавляем отображение меню авторов при необходимости


@window.event
def on_mouse_press(x, y, button, modifiers):
    main_menu.on_mouse_press(x, y, button, modifiers)

@window.event
def on_mouse_motion(x, y, dx, dy):
    main_menu.on_mouse_motion(x, y, dx, dy)


def update(dt):
    main_menu.update(dt)
    main_menu.draw()

pyglet.clock.schedule_interval(update, 1 / 60)

pyglet.app.run()