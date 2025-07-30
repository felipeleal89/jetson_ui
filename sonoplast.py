from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.button import ButtonBehavior
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.graphics import Color, Rectangle

# === Global constants ===
GRID_SIZE = 40                          # original size 40                   
SMALL_ASSET_SIZE = GRID_SIZE * 1.5          
MEDIUM_ASSET_SIZE = GRID_SIZE * 3        
LARGE_ASSET_SIZE = GRID_SIZE * 4        
EXTRA_LARGE_ASSET_SIZE = GRID_SIZE * 6      
WINDOW_SIZE_X = 1280
WINDOW_SIZE_Y = 720
MARGIN = GRID_SIZE // 2

# Vertical sectors (from top down)
SECTOR_TITLE_Y = (GRID_SIZE * 17)
SECTOR_COVER_Y =  SECTOR_TITLE_Y - (GRID_SIZE * 9.5)
SECTOR_CONTROLS_Y = SECTOR_COVER_Y - (GRID_SIZE * 5.5)
SECTOR_TRACK_Y = SECTOR_CONTROLS_Y - (GRID_SIZE * 2)

Window.size = (WINDOW_SIZE_X, WINDOW_SIZE_Y)
Window.title = "SonoBlast"
Window.fullscreen = True  # Uncomment for fullscreen on deploy

# === Custom UI Components ===

class VolumeButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (SMALL_ASSET_SIZE, SMALL_ASSET_SIZE)

class VolumeSlider(Slider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.min = 0
        self.max = 10
        self.value = 5
        self.step = 1
        self.size_hint = (None, None)
        self.size = (GRID_SIZE * 6, GRID_SIZE // 4)
        self.cursor_size = (0 , 0)
        self.background_width = 0
        with self.canvas.before:
            self.bg_color = Color(1, 1, 1, 1)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
            self.fg_color = Color(1, 0.5, 1, 1)
            self.fg_rect = Rectangle(pos=self.pos, size=(self.width * (self.value / self.max), self.height))

        with self.canvas.after:
            self.custom_cursor = Rectangle(
            source="images/cursor.png",  # sua imagem do cursor
            size=(GRID_SIZE, GRID_SIZE)  # ou (40, 40) se preferir fixo
        )

        self.bind(pos=self.update_canvas, size=self.update_canvas, value=self.update_canvas)

class VolumeSlider(Slider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.min = 0
        self.max = 10
        self.value = 5
        self.step = 1
        self.size_hint = (None, None)
        self.size = (GRID_SIZE * 6, GRID_SIZE // 4)
        self.cursor_size = (0, 0)  # desativa cursor padrão
        self.background_width = 0  # remove fundo padrão

        with self.canvas.before:
            self.bg_color = Color(1, 1, 1, 1)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
            self.fg_color = Color(1, 0.5, 1, 1)
            self.fg_rect = Rectangle(pos=self.pos, size=(self.width * (self.value / self.max), self.height))

        with self.canvas.after:
            self.custom_cursor = Rectangle(
                source="images/cursor.png",
                size=(GRID_SIZE, GRID_SIZE)
            )

        self.bind(pos=self.update_canvas, size=self.update_canvas, value=self.update_canvas)

    def update_canvas(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

        progress_width = self.width * ((self.value - self.min) / float(self.max - self.min))
        self.fg_rect.pos = self.pos
        self.fg_rect.size = (progress_width, self.height)

        ratio = (self.value - self.min) / float(self.max - self.min)
        cursor_x = self.x + ratio * self.width - self.custom_cursor.size[0] / 2
        cursor_y = self.y + self.height / 2 - self.custom_cursor.size[1] / 2
        self.custom_cursor.pos = (cursor_x, cursor_y)


class TrackSlider(Slider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.min = 0
        self.max = 100
        self.value = 20
        self.step = 1
        self.size_hint = (None, None)
        self.size = (GRID_SIZE * 8, GRID_SIZE // 4)
        self.cursor_size = (0, 0)
        self.background_width = 0
        self.disabled = True

        with self.canvas.before:
            self.bg_color = Color(1, 1, 1, 1)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
            self.fg_color = Color(1, 0.5, 1, 1)
            self.fg_rect = Rectangle(pos=self.pos, size=(self.width * (self.value / self.max), self.height))

        self.bind(pos=self.update_canvas, size=self.update_canvas, value=self.update_canvas)

    def update_canvas(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.fg_rect.pos = self.pos
        self.fg_rect.size = (self.width * ((self.value - self.min) / float(self.max - self.min)), self.height)

class PlayButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.state_on = False
        self.source = "images/play.png"
        self.size_hint = (None, None)
        self.size = (LARGE_ASSET_SIZE, LARGE_ASSET_SIZE)

    def on_press(self):
        self.state_on = not self.state_on
        self.source = "images/pause.png" if self.state_on else "images/play.png"

class Cover(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.state_on = False
        self.source = "images/dots.png"
        self.size_hint = (None, None)
        self.size = (EXTRA_LARGE_ASSET_SIZE, EXTRA_LARGE_ASSET_SIZE)

class ReverseButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.state_on = False
        self.source = "images/rev_dis.png"
        self.size_hint = (None, None)
        self.size = (MEDIUM_ASSET_SIZE, MEDIUM_ASSET_SIZE)

    def on_press(self):
        self.state_on = True
        self.source = "images/rev_en.png"

    def on_release(self):
        self.state_on = False
        self.source = "images/rev_dis.png"

class ForwardButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.state_on = False
        self.source = "images/forw_dis.png"
        self.size_hint = (None, None)
        self.size = (MEDIUM_ASSET_SIZE, MEDIUM_ASSET_SIZE)

    def on_press(self):
        self.state_on = True
        self.source = "images/forw_en.png"

    def on_release(self):
        self.state_on = False
        self.source = "images/forw_dis.png"

# === Main Layout ===

class SonoplastUI(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(0.15, 0, 0.18, 1)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)

        center_x = WINDOW_SIZE_X // 2

        # === Controls ===
        self.rev_btn = ReverseButton(pos=(center_x - (LARGE_ASSET_SIZE / 2) - (MEDIUM_ASSET_SIZE) - GRID_SIZE/2, SECTOR_CONTROLS_Y + (LARGE_ASSET_SIZE / 2) - (MEDIUM_ASSET_SIZE / 2)))
        self.play_btn = PlayButton(pos=(center_x - (LARGE_ASSET_SIZE / 2), SECTOR_CONTROLS_Y))
        self.fwd_btn = ForwardButton(pos=(center_x + (LARGE_ASSET_SIZE / 2) + GRID_SIZE/2, SECTOR_CONTROLS_Y + (LARGE_ASSET_SIZE / 2) - (MEDIUM_ASSET_SIZE / 2)))
        self.cover_btn = Cover(pos=(center_x - (EXTRA_LARGE_ASSET_SIZE / 2), SECTOR_COVER_Y))

        self.add_widget(self.rev_btn)
        self.add_widget(self.play_btn)
        self.add_widget(self.fwd_btn)
        self.add_widget(self.cover_btn)

        # === Labels ===
        self.sono_label = Label(
            text="Sono",
            markup=True,
            font_size=GRID_SIZE * 2.5,
            font_name="fonts/RobotoCondensed-Regular.ttf",
            color=(1, 0.5, 1, 1),
            size_hint=(None, None),
        )
        self.blast_label = Label(
            text="Blast",
            markup=True,
            font_size=GRID_SIZE * 2.5,
            font_name="fonts/RobotoCondensed-ExtraBold.ttf",
            color=(1, 0.5, 1, 1),
            size_hint=(None, None),
        )
        self.desc_label = Label(
            text="a sonoloplast player_",
            font_size=GRID_SIZE,
            font_name="fonts/Orbitron-Regular.ttf",
            color=(1, 1, 1, 1),
            size_hint=(None, None),
        )
        self.time_label = Label(
            text="00:00",
            font_size=GRID_SIZE / 1.5,
            font_name="fonts/RobotoCondensed-Regular.ttf",
            color=(1, 1, 1, 1),
            size_hint=(None, None),
        )
        self.time_fim_label = Label(
            text="00:00",
            font_size=GRID_SIZE / 1.5,
            font_name="fonts/RobotoCondensed-Regular.ttf",
            color=(1, 1, 1, 1),
            size_hint=(None, None),
        )

        self.add_widget(self.sono_label)
        self.add_widget(self.blast_label)
        self.add_widget(self.desc_label)
        self.add_widget(self.time_label)
        self.add_widget(self.time_fim_label)

        # === Volume Controls ===
        self.volume_slider = VolumeSlider(pos=(center_x + (GRID_SIZE * 9), SECTOR_TRACK_Y + SMALL_ASSET_SIZE / 1.3))
        self.add_widget(self.volume_slider)

        self.vol_up = VolumeButton(source="images/vol_up.png", pos=(center_x + (GRID_SIZE * 7), SECTOR_TRACK_Y + SMALL_ASSET_SIZE / 3))
        self.vol_up.bind(on_release=lambda _: self.adjust_volume(1))
        self.add_widget(self.vol_up)

        # === Track Slider ===
        self.track_slider = TrackSlider(pos=(center_x - GRID_SIZE * 4, SECTOR_TRACK_Y + SMALL_ASSET_SIZE / 1.3))
        self.add_widget(self.track_slider)

        # === Final label positioning ===
        self.sono_label.texture_update()
        self.blast_label.texture_update()
        self.desc_label.texture_update()
        self.time_label.texture_update()
        self.time_fim_label.texture_update()

        self.sono_label.size = self.sono_label.texture_size
        self.blast_label.size = self.blast_label.texture_size
        self.desc_label.size = self.desc_label.texture_size
        self.time_label.size = self.time_label.texture_size
        self.time_fim_label.size = self.time_fim_label.texture_size

        self.sono_label.pos = (center_x - self.sono_label.width, SECTOR_TITLE_Y - self.sono_label.height + GRID_SIZE)
        self.blast_label.pos = (self.sono_label.right, SECTOR_TITLE_Y - self.blast_label.height + GRID_SIZE)
        self.desc_label.pos = (center_x - (self.desc_label.width / 2), SECTOR_TITLE_Y - self.blast_label.height)
        self.time_label.pos = (center_x - self.track_slider.width / 2 - self.time_label.width - GRID_SIZE / 2, SECTOR_TRACK_Y + self.time_label.height)
        self.time_fim_label.pos = (center_x + self.track_slider.width / 2 + GRID_SIZE / 2, SECTOR_TRACK_Y + self.time_fim_label.height)

        self.bind(pos=self.update_bg, size=self.update_bg)

    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def adjust_volume(self, delta):
        new_val = self.volume_slider.value + delta
        self.volume_slider.value = max(self.volume_slider.min, min(self.volume_slider.max, new_val))

class SonoplastApp(App):
    def build(self):
        return SonoplastUI()

if __name__ == "__main__":
    SonoplastApp().run()
