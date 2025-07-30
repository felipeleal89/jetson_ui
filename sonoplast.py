from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.button import ButtonBehavior
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.graphics import Color, Rectangle

# === Global constants ===
GRID_SIZE = 35
SMALL_ASSET_SIZE = GRID_SIZE * 2           
MEDIUM_ASSET_SIZE = GRID_SIZE * 2          
LARGE_ASSET_SIZE = GRID_SIZE * 4        
EXTRA_LARGE_ASSET_SIZE = GRID_SIZE * 8      
WINDOW_SIZE_X = 1280
WINDOW_SIZE_Y = 720
MARGIN = GRID_SIZE // 2

# Vertical sectors (from top down)
SECTOR_TITLE_Y = (GRID_SIZE * 17)
SECTOR_COVER_Y =  SECTOR_TITLE_Y - (GRID_SIZE * 10)
SECTOR_TRACK_Y = SECTOR_COVER_Y - (GRID_SIZE * 1)
SECTOR_CONTROLS_Y = SECTOR_TRACK_Y - (GRID_SIZE * 2.5)
SECTOR_VOLUME_Y = SECTOR_CONTROLS_Y - (GRID_SIZE * 2.5)

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
        self.size = (GRID_SIZE * 12, GRID_SIZE // 8)
        self.cursor_size = (0, 0)
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

class TrackSlider(Slider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.min = 0
        self.max = 100
        self.value = 20
        self.step = 1
        self.size_hint = (None, None)
        self.size = (GRID_SIZE * 12, GRID_SIZE // 8)
        self.cursor_size = (0, 0)
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
        self.size = (MEDIUM_ASSET_SIZE, MEDIUM_ASSET_SIZE)

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
        self.rev_btn = ReverseButton(pos=(center_x - (GRID_SIZE * 5) - (MEDIUM_ASSET_SIZE // 2), SECTOR_CONTROLS_Y))
        self.play_btn = PlayButton(pos=(center_x - (MEDIUM_ASSET_SIZE // 2), SECTOR_CONTROLS_Y))
        self.fwd_btn = ForwardButton(pos=(center_x + (GRID_SIZE * 5) - (MEDIUM_ASSET_SIZE // 2), SECTOR_CONTROLS_Y))
        self.cover_btn = Cover(pos=(center_x - (EXTRA_LARGE_ASSET_SIZE // 2), SECTOR_COVER_Y))

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

        self.add_widget(self.sono_label)
        self.add_widget(self.blast_label)
        self.add_widget(self.desc_label)

        # === Volume Controls ===
        self.vol_down = VolumeButton(source="images/vol_down.png", pos=(center_x - (GRID_SIZE * 8) - SMALL_ASSET_SIZE, SECTOR_VOLUME_Y))
        self.vol_down.bind(on_release=lambda _: self.adjust_volume(-1))
        self.add_widget(self.vol_down)

        self.volume_slider = VolumeSlider(pos=(center_x - (GRID_SIZE * 6), SECTOR_VOLUME_Y + MEDIUM_ASSET_SIZE // 2))
        self.add_widget(self.volume_slider)

        self.vol_up = VolumeButton(source="images/vol_up.png", pos=(center_x + (GRID_SIZE * 8), SECTOR_VOLUME_Y))
        self.vol_up.bind(on_release=lambda _: self.adjust_volume(1))
        self.add_widget(self.vol_up)

        # === Track Slider ===
        self.track_slider = TrackSlider(pos=(center_x - (GRID_SIZE * 6), SECTOR_TRACK_Y))
        self.add_widget(self.track_slider)

        # === Final label positioning ===
        self.sono_label.texture_update()
        self.blast_label.texture_update()
        self.desc_label.texture_update()

        self.sono_label.size = self.sono_label.texture_size
        self.blast_label.size = self.blast_label.texture_size
        self.desc_label.size = self.desc_label.texture_size

        self.sono_label.pos = (center_x - self.sono_label.width, SECTOR_TITLE_Y)
        self.blast_label.pos = (self.sono_label.right, SECTOR_TITLE_Y)
        self.desc_label.pos = (center_x - (self.desc_label.width // 2), SECTOR_TITLE_Y - GRID_SIZE)

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
