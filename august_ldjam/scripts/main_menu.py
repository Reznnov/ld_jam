import pyglet
import math
import time
import webbrowser

# Задаем размеры экрана
screen_width = 1920
screen_height = 1080

# Создаем окно приложения
window = pyglet.window.Window(screen_width, screen_height)


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

class AuthorsMenu:
    def __init__(self, background_image, parent_window):
        self.parent_window = parent_window
        self.background = pyglet.image.load(background_image)
        self.background_sprite = pyglet.sprite.Sprite(self.background, x=0, y=0)
        self.authors_names = ['Вася пупкин', 'то сё туда сда', 'ссылка']
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


    def on_hide(self):
        self.is_showing = False

    def on_mouse_press(self, x, y, button, modifiers):
        for label in self.labels:
            # Проверяем, что клик был по ссылке на соцсеть 1
            if label.text == 'Ссылка на соцсеть 1':
                if label.x <= x <= label.x + label.content_width and label.y <= y <= label.y + label.content_height:
                    webbrowser.open('https://vk.com/redbreadstudio')



class MainMenu:
    def __init__(self, background_image):
        self.background_index = 0
        self.background = pyglet.image.load(background_image)
        self.background_sprite = pyglet.sprite.Sprite(self.background, x=0, y=0)
        self.authors_menu = None
        self.show_authors = False

        # Загрузка изображений кнопок
        new_game_button_image = pyglet.image.load('/home/reznnov/rabota/assets/images/main_menu_sprites/start_idle (3).png')
        save_button_image = pyglet.image.load('/home/reznnov/rabota/assets/images/main_menu_sprites/load_idle (3).png')
        galery_button_image = pyglet.image.load('/home/reznnov/rabota/assets/images/main_menu_sprites/galery_idle (3).png')
        settings_button_image = pyglet.image.load('/home/reznnov/rabota/assets/images/main_menu_sprites/prefs_idle (3).png')
        credits_button_image = pyglet.image.load('/home/reznnov/rabota/assets/images/main_menu_sprites/credits_idle (3).png')
        q_button_image = pyglet.image.load('/home/reznnov/rabota/assets/images/main_menu_sprites/q_idle (3).png')

        new_game_button_image_hover = pyglet.image.load('/home/reznnov/rabota/assets/images/main_menu_sprites/start_hover (3).png')
        save_button_image_hover = pyglet.image.load('/home/reznnov/rabota/assets/images/main_menu_sprites/load_hover (3).png')
        galery_button_image_hover = pyglet.image.load('/home/reznnov/rabota/assets/images/main_menu_sprites/galery_hover (3).png')
        settings_button_image_hover = pyglet.image.load('/home/reznnov/rabota/assets/images/main_menu_sprites/prefs_hover (3).png')
        credits_button_image_hover = pyglet.image.load('/home/reznnov/rabota/assets/images/main_menu_sprites/credits_hover (3).png')
        q_button_image_hover = pyglet.image.load('/home/reznnov/rabota/assets/images/main_menu_sprites/q_hover (3).png')


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


    def update(self, dt):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        if self.credits_button.x < x < self.credits_button.x + self.credits_button.width and \
                self.credits_button.y < y < self.credits_button.y + self.credits_button.height:
            self.show_authors_menu()
        if self.authors_menu and self.show_authors:
            self.authors_menu.on_mouse_press(x, y, button, modifiers)

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

    def hide_authors_menu(self):
        self.authors_menu = None
        self.show_authors = False



main_menu = MainMenu('/home/reznnov/rabota/assets/images/main_menu_sprites/bg_main_menu.png')

index = 0
show_authors_menu = False



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
