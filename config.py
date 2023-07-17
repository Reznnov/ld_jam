import pyglet
import math
import time

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


class MainMenu:
    def __init__(self, background_image):
        self.background = pyglet.image.load(background_image)
        self.background_sprite = pyglet.sprite.Sprite(self.background, x=0, y=0)

        # Загрузка изображений кнопок
        new_game_button_image = pyglet.image.load('/home/reznnov/rabota/assets/images/test/start_idle.png')
        save_button_image = pyglet.image.load('/home/reznnov/rabota/assets/images/test/load_idle.png')
        galery_button_image = pyglet.image.load('/home/reznnov/rabota/assets/images/test/galery_idle.png')
        achiv_button_image = pyglet.image.load('/home/reznnov/rabota/assets/images/test/achiv_idle.png')
        settings_button_image = pyglet.image.load('/home/reznnov/rabota/assets/images/test/prefs_idle.png')
        credits_button_image = pyglet.image.load('/home/reznnov/rabota/assets/images/test/credits_idle.png')
        q_button_image = pyglet.image.load('/home/reznnov/rabota/assets/images/test/q_idle.png')
        kartinka_1 = pyglet.image.load('/home/reznnov/rabota/assets/images/test/3.png')
        kartinka_2 = pyglet.image.load('/home/reznnov/rabota/assets/images/test/2.png')

        self.buttons = []

        # Создание спрайтов для кнопок
        self.new_game_button = pyglet.sprite.Sprite(new_game_button_image,
                                                    x=screen_width // 2 + 600, y=screen_height // 2 + 100)
        self.save_button = pyglet.sprite.Sprite(save_button_image,
                                                x=screen_width // 2 + 575, y=screen_height // 2 + 20)
        self.settings_button = pyglet.sprite.Sprite(settings_button_image,
                                                    x=screen_width // 2 + 550, y=screen_height // 2 - 60)
        self.galery_button = pyglet.sprite.Sprite(galery_button_image,
                                                  x=screen_width // 2 + 525, y=screen_height // 2 - 140)
        self.achiv_button = pyglet.sprite.Sprite(achiv_button_image,
                                                 x=screen_width // 2 + 500, y=screen_height // 2 - 220)
        self.credits_button = pyglet.sprite.Sprite(credits_button_image,
                                                   x=screen_width // 2 + 475, y=screen_height // 2 - 300)
        self.q_button = pyglet.sprite.Sprite(q_button_image,
                                             x=screen_width // 2 + 450, y=screen_height // 2 - 380)
        self.kartinka_1_button = pyglet.sprite.Sprite(kartinka_1,
                                                      x=screen_width // 2, y=screen_height // 2 - 160)
        self.kartinka_2_button = pyglet.sprite.Sprite(kartinka_2,
                                                      x=screen_width // 2 - 170, y=screen_height // 2 - 700)
        self.kartinka_1_button.visible = False
        self.kartinka_2_button.visible = False

        # Создание спрайта для полоски
        poloska_image = pyglet.image.load('/home/reznnov/rabota/assets/images/test/1.png')
        poloska2_image = pyglet.image.load('/home/reznnov/rabota/assets/images/test/1.png')
        self.poloska_sprite = pyglet.sprite.Sprite(poloska_image,
                                                   x=screen_width, y=screen_height // 2 - 540)
        self.poloska2_sprite = pyglet.sprite.Sprite(poloska2_image,
                                                   x=screen_width, y=screen_height // 2 - 540)

        # Установка начальной прозрачности кнопок
        self.new_game_button.opacity = 0
        self.save_button.opacity = 0
        self.settings_button.opacity = 0
        self.galery_button.opacity = 0
        self.achiv_button.opacity = 0
        self.credits_button.opacity = 0
        self.q_button.opacity = 0

        self.buttons.append(self.new_game_button)
        self.buttons.append(self.save_button)
        self.buttons.append(self.galery_button)
        self.buttons.append(self.achiv_button)
        self.buttons.append(self.settings_button)
        self.buttons.append(self.credits_button)
        self.buttons.append(self.q_button)

        self.fade_duration = 1.0  # Длительность анимации появления кнопок (в секундах)
        self.fade_out_duration = 0.5

        self.animations = []
        self.animations_out = []
        for button_sprite in self.buttons:
            animation = FadeInAnimation(button_sprite, self.fade_duration)
            self.animations.append(animation)
            animation_out = FadeOutAnimation(button_sprite, self.fade_out_duration)
            self.animations_out.append(animation_out)


        self.poloska_reached_target = False
        self.poloska_moving = False  # Флаг, указывающий, находится ли полоска в процессе перемещения
        self.poloska2_moving = False
        self.pusk = True

        # Анимация появления первой полоски и кнопок
        self.animation_duration = 1.4  # Длительность анимации полоски в секундах
        self.animation_elapsed_time = 0.0  # Прошедшее время анимации полоски
        self.easing_duration = 1.6  # Длительность эффекта плавного перехода в секундах

        # Анимация первой полоски после нажатия на галерею
        self.poloska_duration = 1.4
        self.poloska_elapsed_time = 0.0
        self.poloska_easing_duration = 1.6

        # Анимация появления второй полоски полоски после нажатия на галерею
        self.poloska2_duration = 1.4
        self.poloska2_elapsed_time = 0.0
        self.poloska2_easing_duration = 1.6

        self.scroll_speed = 5  # Скорость скролла
        self.scroll_direction = 0  # Направление скролла (0 - нет скролла, 1 - скролл вниз, -1 - скролл вверх)

    def update(self, dt):
        self.animation_elapsed_time += dt

        if self.poloska_moving:
            self.poloska_elapsed_time += dt
            self.poloska2_elapsed_time += dt
            for animation_out in self.animations_out:
                animation_out.update(dt)
            start_x = screen_width // 2 + 300  # Начальная позиция полоски при нажатии на кнопку галереи
            target_x = screen_width // 2 - 1700  # Целевая позиция полоски при нажатии на кнопку галереи

            t = min(1.0, self.poloska_elapsed_time / self.poloska_duration)
            t = 0.5 - 0.5 * math.cos(t * math.pi)  # Функция плавного перехода по параболе

            current_x = start_x + ((target_x - start_x) * t)
            self.poloska_sprite.x = current_x
            if current_x < -450:
                self.poloska2_moving = True

            if current_x == target_x:
                self.poloska_moving = False
                self.background_sprite.image = pyglet.image.load('../assets/images/test/6.png')
                self.kartinka_1_button.visible = True
                self.kartinka_2_button.visible = True
        if self.poloska2_moving:
            target2_x = screen_width // 2 + 600  # Целевая позиция полоски

            t2 = min(1.0, self.poloska2_elapsed_time / self.poloska2_easing_duration)
            t2 = 0.5 - 0.5 * math.cos(t2 * math.pi)

            current2_x = screen_width + ((target2_x - screen_width) * t2)
            self.poloska2_sprite.x = current2_x

            if current2_x == target2_x:
                self.poloska2_moving = False

        if not self.poloska_reached_target:
            target_x = screen_width // 2 + 300  # Целевая позиция полоски

            t = min(1.0, self.animation_elapsed_time / self.easing_duration)
            t = 0.5 - 0.5 * math.cos(t * math.pi)

            current_x = screen_width + ((target_x - screen_width) * t)
            self.poloska_sprite.x = current_x

            if current_x == target_x:
                self.poloska_reached_target = True

        if self.poloska_reached_target:
            for animation in self.animations:
                animation.update(dt)





    # Обработчик события прекращения скролла колесика мыши
    def on_mouse_scroll_stop(self, x, y):
        self.scroll_direction = 0  # Отсутствие скролла

    def draw(self):
        self.background_sprite.draw()
        self.poloska_sprite.draw()
        self.poloska2_sprite.draw()
        for button_sprite in self.buttons:
            button_sprite.draw()
        self.kartinka_1_button.draw()
        self.kartinka_2_button.draw()


main_menu = MainMenu('../assets/images/test/5.png')

angle_radians = math.radians(72.52522574374433)
index = 0

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


@window.event
def on_draw():
    window.clear()
    main_menu.draw()


@window.event
def on_mouse_press(x, y, button, modifiers):
    if main_menu.galery_button.x < x < main_menu.galery_button.x + main_menu.galery_button.width and \
            main_menu.galery_button.y < y < main_menu.galery_button.y + main_menu.galery_button.height:
        if button == pyglet.window.mouse.LEFT:
            main_menu.poloska_moving = True

@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    if scroll_y > 0:
        main_menu.kartinka_1_button.y += 540* math.sin(angle_radians)  # Смещение вверх
        main_menu.kartinka_2_button.y += 540 * math.sin(angle_radians)  # Смещение вверх
        main_menu.kartinka_1_button.x += 540 * math.cos(angle_radians)  # Смещение вправо
        main_menu.kartinka_2_button.x += 540 * math.cos(angle_radians)
    elif scroll_y < 0:
        main_menu.kartinka_1_button.y -= 540 * math.sin(angle_radians)  # Смещение вниз
        main_menu.kartinka_2_button.y -= 540 * math.sin(angle_radians)  # Смещение вниз
        main_menu.kartinka_1_button.x -= 540 * math.cos(angle_radians)  # Смещение влево
        main_menu.kartinka_2_button.x -= 540 * math.cos(angle_radians)  # Смещение влево


@window.event
def on_mouse_scroll_stop(x, y):
    main_menu.on_mouse_scroll_stop(x, y)


def update(dt):
    main_menu.update(dt)


pyglet.clock.schedule_interval(update, 1 / 60)

pyglet.app.run()
