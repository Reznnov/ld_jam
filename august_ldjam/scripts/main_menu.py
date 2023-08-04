import pyglet
#import math
import json
import webbrowser

# Задаем размеры экрана
screen_width = 1920
screen_height = 1080

# Создаем окно приложения
window = pyglet.window.Window(screen_width, screen_height, fullscreen=False)


class FadeInAnimation:
    def __init__(self, sprite, fade_duration):
        self.sprite = sprite
        self.fade_duration = fade_duration
        self.fade_elapsed_time = 0.0
        self.fade_start = 0
        self.fade_end = 255

    def update(self, dt):
        self.fade_elapsed_time += dt

        if self.fade_elapsed_time <= self.fade_duration:
            alpha = int((self.fade_elapsed_time / self.fade_duration) * self.fade_end)
            self.sprite.opacity = alpha

class FadeOutAnimation:
    def __init__(self, sprite, fade_duration):
        self.sprite = sprite
        self.fade_duration = fade_duration
        self.fade_elapsed_time = 0.0
        self.fade_start = 255
        self.fade_end = 0

    def update(self, dt):
        self.fade_elapsed_time += dt

        if self.fade_elapsed_time <= self.fade_duration:
            alpha = int((self.fade_elapsed_time / self.fade_duration) * (self.fade_end - self.fade_start))
            self.sprite.opacity = self.fade_start + alpha

class SlideAnimation:
    def __init__(self, sprite, start_x, target_x, duration):
        self.sprite = sprite
        self.start_x = start_x
        self.target_x = target_x
        self.duration = duration
        self.elapsed_time = 0.0

    def update(self, dt):
        self.elapsed_time += dt

        if self.elapsed_time <= self.duration:
            t = self.elapsed_time / self.duration
            self.sprite.x = self.start_x + (self.target_x - self.start_x) * t


#class Text:
    #def __init__(self, text, text_font=None, text_size=None, text_color=None, text_animation=None, text_):

class SettingsMenu:
    settings_slider_image = pyglet.image.load('/home/reznnov/rabota/august_ldjam/images/Settings_menu/prefs_slider.png')
    settings_slider_button_1 = pyglet.sprite.Sprite(settings_slider_image, x=screen_width // 2 + 50, y=screen_height // 2 + 12)
    settings_slider_button_2 = pyglet.sprite.Sprite(settings_slider_image, x=screen_width // 2 + 50, y=screen_height // 2 - 88)
    settings_slider_button_3 = pyglet.sprite.Sprite(settings_slider_image, x=screen_width // 2 + 50, y=screen_height // 2 - 188)
    def __init__(self, background_image, parent_window):
        self.parent_window = parent_window
        self.background = pyglet.image.load(background_image)
        self.background_sprite = pyglet.sprite.Sprite(self.background, x=0, y=0)

        # Флаг для обозначения состояния перетаскивания settings_slider_button_1
        self.dragging_settings_slider_button_1 = False
        self.dragging_settings_slider_button_2 = False
        self.dragging_settings_slider_button_3 = False

        # Загрузка сохраненных позиций слайдеров при запуске приложения
        self.load_slider_positions('slider_positions.json')
        self.load_screen_mode_from_json('screen_mode.json')
        self.load_music_volume_from_json('music_volume.json')

        # Переменная для хранения значения громкости музыки
        self.music_volume = 0.0

        # Загрузка изображений кнопок
        settings_text_speed_image = pyglet.image.load('/home/reznnov/rabota/august_ldjam/images/Settings_menu/prefs_text_speed.png')
        settings_volume_of_music_image = pyglet.image.load('/home/reznnov/rabota/august_ldjam/images/Settings_menu/prefs_volume_of_music.png')
        settings_volume_of_sound_image = pyglet.image.load('/home/reznnov/rabota/august_ldjam/images/Settings_menu/prefs_volume_of_sounds.png')
        settings_line_image = pyglet.image.load('/home/reznnov/rabota/august_ldjam/images/Settings_menu/prefs_line.png')
        settings_go_to_full_screen_image = pyglet.image.load('/home/reznnov/rabota/august_ldjam/images/Settings_menu/prefs_go_to_full.png')
        settings_go_to_window_screen_image = pyglet.image.load('/home/reznnov/rabota/august_ldjam/images/Settings_menu/prefs_go_to_window.png')

        # Создание спрайтов для кнопок
        self.settings_text_speed_button = pyglet.sprite.Sprite(settings_text_speed_image, x=screen_width // 2 - 200, y=screen_height // 2 + 50)
        self.settings_volume_of_music_button = pyglet.sprite.Sprite(settings_volume_of_music_image, x=screen_width // 2 - 200, y=screen_height // 2 - 50)
        self.settings_volume_of_sound_button = pyglet.sprite.Sprite(settings_volume_of_sound_image, x=screen_width // 2 - 200, y=screen_height // 2 - 150)

        self.settings_line_button_1 = pyglet.sprite.Sprite(settings_line_image, x=screen_width // 2 - 160, y=screen_height // 2 + 20)
        self.settings_line_button_2 = pyglet.sprite.Sprite(settings_line_image, x=screen_width // 2 - 160, y=screen_height // 2 - 80)
        self.settings_line_button_3 = pyglet.sprite.Sprite(settings_line_image, x=screen_width // 2 - 160, y=screen_height // 2 - 180)

        self.settings_go_to_full_screen_button = pyglet.sprite.Sprite(settings_go_to_full_screen_image, x=screen_width // 2 - 30, y=screen_height // 2 - 340)
        self.settings_go_to_window_screen_button = pyglet.sprite.Sprite(settings_go_to_window_screen_image, x=screen_width // 2 - 30, y=screen_height // 2 - 340)

        self.settings_go_to_window_screen_button.visible = False


        self.settings_text_speed_button.scale = 0.55
        self.settings_volume_of_music_button.scale = 0.55
        self.settings_volume_of_sound_button.scale = 0.55
        self.settings_line_button_1.scale = 0.6
        self.settings_line_button_2.scale = 0.6
        self.settings_line_button_3.scale = 0.6
        self.settings_slider_button_1.scale = 0.6
        self.settings_slider_button_2.scale = 0.6
        self.settings_slider_button_3.scale = 0.6
        self.settings_go_to_full_screen_button.scale = 0.5
        self.settings_go_to_window_screen_button.scale = 0.5

    def update_music_volume(self):
        # Get the x-coordinate of settings_slider_button_2
        slider_button_2_x = self.settings_slider_button_2.x

        # Define the minimum and maximum x-coordinates for volume control
        min_x = 800
        max_x = 1220

        # Define the minimum and maximum volume values
        min_volume = 0.0
        max_volume = 1.0

        # Calculate the volume based on the x-coordinate
        if slider_button_2_x <= min_x:
            self.music_volume = min_volume
        elif slider_button_2_x >= max_x:
            self.music_volume = max_volume
        else:
            # Linear scaling to calculate the volume within the desired range
            self.music_volume = (slider_button_2_x - min_x) / (max_x - min_x) * (max_volume - min_volume) + min_volume

        # Применяем новую громкость к музыкальному плееру
        if main_menu.music_player:
            main_menu.music_player.volume = self.music_volume

        # Save the music volume to the JSON file
        self.save_music_volume_to_json('music_volume.json')


    def save_music_volume_to_json(self, filename):
        data = {
            'music_volume': self.music_volume
        }
        with open(filename, 'w') as file:
            json.dump(data, file)

    def load_slider_positions(self, filename):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            self.settings_slider_button_1.x = data['slider_button_1_x']
            self.settings_slider_button_2.x = data['slider_button_2_x']
            self.settings_slider_button_3.x = data['slider_button_3_x']
        except FileNotFoundError:
            # Обработка случая, когда файл не найден (например, при первом запуске приложения)
            pass

    def load_music_volume_from_json(self, filename):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                self.music_volume = data['music_volume']
                # Apply the loaded volume to the music player
                if main_menu.music_player:
                    main_menu.music_player.volume = self.music_volume
        except FileNotFoundError:
            # If the file is not found, set a default value for the music volume
            self.music_volume = 0.5  # Set your desired default volume value here
            # Apply the default volume to the music player
            if main_menu.music_player:
                main_menu.music_player.volume = self.music_volume

    def save_screen_mode_to_json(self, file_name):
        data = {
            'fullscreen': self.fullscreen
        }
        with open(file_name, 'w') as file:
            json.dump(data, file)

    def load_screen_mode_from_json(self, file_name):
        try:
            with open(file_name, 'r') as file:
                data = json.load(file)
                self.fullscreen = data['fullscreen']
                window.set_fullscreen(self.fullscreen)  # Установите режим полноэкранного окна
        except FileNotFoundError:
            # Если файл не найден, оставляем текущее состояние fullscreen без изменений
            pass

    def save_slider_positions(self, filename):
        data = {
            'slider_button_1_x': self.settings_slider_button_1.x,
            'slider_button_2_x': self.settings_slider_button_2.x,
            'slider_button_3_x': self.settings_slider_button_3.x,
            'music_volume': self.music_volume  # Include the music volume in the data
        }
        with open(filename, 'w') as f:
            json.dump(data, f)



    def on_mouse_press(self, x, y, button, modifiers):
        # Проверяем, попал ли курсор в settings_slider_button_1 и зажата левая кнопка мыши
        if button == pyglet.window.mouse.LEFT and \
                self.settings_slider_button_1.x <= x <= self.settings_slider_button_1.x + self.settings_slider_button_1.width and \
                self.settings_slider_button_1.y <= y <= self.settings_slider_button_1.y + self.settings_slider_button_1.height:

            self.dragging_settings_slider_button_1 = True

        if button == pyglet.window.mouse.LEFT and \
                self.settings_slider_button_2.x <= x <= self.settings_slider_button_2.x + self.settings_slider_button_2.width and \
                self.settings_slider_button_2.y <= y <= self.settings_slider_button_2.y + self.settings_slider_button_2.height:

            self.dragging_settings_slider_button_2 = True

        if button == pyglet.window.mouse.LEFT and \
                self.settings_slider_button_3.x <= x <= self.settings_slider_button_3.x + self.settings_slider_button_3.width and \
                self.settings_slider_button_3.y <= y <= self.settings_slider_button_3.y + self.settings_slider_button_3.height:

            self.dragging_settings_slider_button_3 = True

        if button == pyglet.window.mouse.LEFT and \
            self.settings_go_to_full_screen_button.x <= x <= self.settings_go_to_full_screen_button.x + self.settings_go_to_full_screen_button.width and \
            self.settings_go_to_full_screen_button.y <= y <= self.settings_go_to_full_screen_button.y + self.settings_go_to_full_screen_button.height and \
            self.settings_go_to_window_screen_button.visible is False:

            set_fullscreen()
            self.settings_go_to_window_screen_button.visible = True
            self.settings_go_to_full_screen_button.visible = False
        elif button == pyglet.window.mouse.LEFT and \
            self.settings_go_to_full_screen_button.x <= x <= self.settings_go_to_full_screen_button.x + self.settings_go_to_full_screen_button.width and \
            self.settings_go_to_full_screen_button.y <= y <= self.settings_go_to_full_screen_button.y + self.settings_go_to_full_screen_button.height and \
            self.settings_go_to_window_screen_button.visible is True:

            set_windowed()
            self.settings_go_to_window_screen_button.visible = False
            self.settings_go_to_full_screen_button.visible = True

    def on_mouse_release(self, x, y, button, modifiers):
        pass


    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.dragging_settings_slider_button_1 and buttons & pyglet.window.mouse.LEFT and \
                self.settings_slider_button_1.y - 20 <= y <= self.settings_slider_button_1.y + self.settings_slider_button_1.height + 20:
            # Определяем новую позицию X для слайдера
            new_x = x
            if new_x < 798:
                new_x = 798
            elif new_x > 1226:
                new_x = 1220
            # Обновляем координату X settings_slider_button_1 на основе новой позиции
            self.settings_slider_button_1.x = new_x
            self.save_slider_positions('slider_positions.json')

        if self.dragging_settings_slider_button_2 and buttons & pyglet.window.mouse.LEFT and \
                self.settings_slider_button_2.y - 20 <= y <= self.settings_slider_button_2.y + self.settings_slider_button_2.height + 20:
            # Обновляем координату X settings_slider_button_1 на основе текущей позиции мыши
            new2_x = x
            if new2_x < 798:
                new2_x = 798
            elif new2_x > 1226:
                new2_x = 1220
            # Обновляем координату X settings_slider_button_1 на основе новой позиции
            self.settings_slider_button_2.x = new2_x
            self.save_slider_positions('slider_positions.json')
            self.update_music_volume()

        if self.dragging_settings_slider_button_3 and buttons & pyglet.window.mouse.LEFT and \
                self.settings_slider_button_3.y - 20 <= y <= self.settings_slider_button_3.y + self.settings_slider_button_3.height + 20:
            # Обновляем координату X settings_slider_button_1 на основе текущей позиции мыши
            new3_x = x
            if new3_x < 798:
                new3_x = 798
            elif new3_x > 1226:
                new3_x = 1220
            # Обновляем координату X settings_slider_button_1 на основе новой позиции
            self.settings_slider_button_3.x = new3_x
            self.save_slider_positions('slider_positions.json')


    def draw(self):
        self.background_sprite.draw()
        self.settings_text_speed_button.draw()
        self.settings_volume_of_music_button.draw()
        self.settings_volume_of_sound_button.draw()
        self.settings_line_button_1.draw()
        self.settings_line_button_2.draw()
        self.settings_line_button_3.draw()
        self.settings_slider_button_1.draw()
        self.settings_slider_button_2.draw()
        self.settings_slider_button_3.draw()
        self.settings_go_to_full_screen_button.draw()
        self.settings_go_to_window_screen_button.draw()


class LoadMenu:
    def __init__(self, background_image, parent_window):
        self.parent_window = parent_window
        self.background = pyglet.image.load(background_image)
        self.background_sprite = pyglet.sprite.Sprite(self.background, x=0, y=0)


    def on_hide(self):
        self.is_showing = False


    def on_mouse_press(self, x, y, button, modifiers):
        pass

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

    def on_hide(self):
        self.is_showing = False

    def on_mouse_press(self, x, y, button, modifiers):
        for label in self.labels:
            # Проверяем, что клик был по ссылке на соцсеть 1
            if label.text == 'Ссылка на соцсеть 1':
                if label.x <= x <= label.x + 400 and label.y - 100 <= y <= label.y:
                    webbrowser.open('https://vk.com/redbreadstudio')

    def draw(self):
        self.background_sprite.draw()
        for label in self.labels:
            label.draw()

class MainMenu:
    def __init__(self, background_image):
        self.fullscreen = False
        self.background_index = 0
        self.background = pyglet.image.load(background_image)
        self.background_sprite = pyglet.sprite.Sprite(self.background, x=0, y=0)
        self.authors_menu = None
        self.settings_menu = None
        self.load_menu = None
        self.show_authors = False
        self.show_settings = False
        self.show_loads = False

        music_file = '/home/reznnov/rabota/august_ldjam/audio/2.mp3'  # Замените путь на путь к вашему аудио файлу
        self.music_player = pyglet.media.Player()
        self.music_player.queue(pyglet.media.load(music_file))
        self.load_music_volume_from_json('music_volume.json')
        self.music_player.play()

        # Загрузка изображений кнопок
        new_game_button_image = pyglet.image.load('/home/reznnov/rabota/august_ldjam/images/Main_menu/start_idle.png')
        save_button_image = pyglet.image.load('/home/reznnov/rabota/august_ldjam/images/Main_menu/load_idle.png')
        galery_button_image = pyglet.image.load('/home/reznnov/rabota/august_ldjam/images/Main_menu/galery_idle.png')
        settings_button_image = pyglet.image.load('/home/reznnov/rabota/august_ldjam/images/Main_menu/prefs_idle.png')
        credits_button_image = pyglet.image.load('/home/reznnov/rabota/august_ldjam/images/Main_menu/credits_idle.png')
        q_button_image = pyglet.image.load('/home/reznnov/rabota/august_ldjam/images/Main_menu/q_idle.png')

        new_game_button_image_hover = pyglet.image.load('/home/reznnov/rabota/august_ldjam/images/Main_menu/start_hover.png')
        save_button_image_hover = pyglet.image.load('/home/reznnov/rabota/august_ldjam/images/Main_menu/load_hover.png')
        galery_button_image_hover = pyglet.image.load('/home/reznnov/rabota/august_ldjam/images/Main_menu/galery_hover.png')
        settings_button_image_hover = pyglet.image.load('/home/reznnov/rabota/august_ldjam/images/Main_menu/prefs_hover.png')
        credits_button_image_hover = pyglet.image.load('/home/reznnov/rabota/august_ldjam/images/Main_menu/credits_hover.png')
        q_button_image_hover = pyglet.image.load('/home/reznnov/rabota/august_ldjam/images/Main_menu/q_hover.png')


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

    def load_music_volume_from_json(self, filename):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                self.music_volume = data['music_volume']
                # Apply the loaded volume to the music player
                if self.music_player:
                    self.music_player.volume = self.music_volume
        except FileNotFoundError:
            # If the file is not found, set a default value for the music volume
            self.music_volume = 0.5  # Set your desired default volume value here
            # Apply the default volume to the music player
            if self.music_player:
                self.music_player.volume = self.music_volume

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
            self.settings_menu.save_slider_positions('slider_positions.json')
            self.hide_settings_menu()
        if symbol == pyglet.window.key.Q and self.show_loads:
            self.hide_loads_menu()

    def update(self, dt):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        if self.credits_button.x < x < self.credits_button.x + self.credits_button.width and \
                self.credits_button.y < y < self.credits_button.y + self.credits_button.height:
            self.show_authors_menu()
        if self.settings_button.x < x < self.settings_button.x + self.settings_button.width and \
                self.settings_button.y < y < self.settings_button.y + self.settings_button.height:
            self.show_settings_menu()
        if self.save_button.x < x < self.save_button.x + self.save_button.width and \
                self.save_button.y < y < self.save_button.y + self.save_button.height:
            self.show_loads_menu()
        if self.authors_menu and self.show_authors:
            self.authors_menu.on_mouse_press(x, y, button, modifiers)
        if self.settings_menu and self.show_settings:
            self.settings_menu.on_mouse_press(x, y, button, modifiers)
        if self.load_menu and self.show_loads:
            self.load_menu.on_mouse_press(x, y, button, modifiers)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.settings_menu and self.show_settings:
            self.settings_menu.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        if self.settings_menu and self.show_settings:
            self.settings_menu.on_mouse_release(x, y, button, modifiers)

    def show_settings_menu(self):
        # создаём экземляр класса SettingsMenu
        self.settings_menu = SettingsMenu('/home/reznnov/rabota/august_ldjam/images/Settings_menu/prefs_bg.png', self)
        # меняем значение флаговой переменной
        self.show_settings = True

    def show_authors_menu(self):
        # Создаем экземпляр класса AuthorsMenu
        self.authors_menu = AuthorsMenu('/home/reznnov/rabota/august_ldjam/images/Authors_menu/credits_bg.png', self)
        # меняем значение флаговой переменной
        self.show_authors = True

    def show_loads_menu(self):
        self.load_menu = LoadMenu('/home/reznnov/rabota/august_ldjam/images/load_menu/load_bg.png', self)
        self.show_loads = True

    def hide_authors_menu(self):
        self.authors_menu = None
        self.show_authors = False

    def hide_settings_menu(self):
        self.settings_menu = None
        self.show_settings = False


    def hide_loads_menu(self):
        self.load_menu = None
        self.show_loads = False

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
        if self.show_loads and self.load_menu:
            self.load_menu.draw()


main_menu = MainMenu('/home/reznnov/rabota/august_ldjam/images/Main_menu/bg_main_menu.png')

index = 0


def load_screen_mode_from_json(file_name):
    try:
        with open(file_name, 'r') as file:
            data = json.load(file)
            fullscreen = data['fullscreen']
            window.set_fullscreen(fullscreen)  # Установите режим полноэкранного окна
    except FileNotFoundError:
        # Если файл не найден, оставляем текущее состояние fullscreen без изменений
        pass

load_screen_mode_from_json('screen_mode.json')
def save_screen_mode_to_json(fullscreen, file_name):
    data = {
        'fullscreen': fullscreen
    }
    with open(file_name, 'w') as file:
        json.dump(data, file)


def set_windowed():
    window.set_fullscreen(False)
    fullscreen = False
    window.set_size(screen_width, screen_height)
    save_screen_mode_to_json(fullscreen, 'screen_mode.json')

def set_fullscreen():
    fullscreen = True
    window.set_fullscreen(True)
    save_screen_mode_to_json(fullscreen, 'screen_mode.json')

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


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    main_menu.on_mouse_drag(x, y, dx, dy, buttons, modifiers)


def update(dt):
    main_menu.update(dt)
    main_menu.draw()

pyglet.clock.schedule_interval(update, 1 / 60)

pyglet.app.run()
