from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.button import ButtonBehavior
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from time import time

# === Constants ===
GRID_SIZE = 40
SMALL_ASSET_SIZE = GRID_SIZE * 1.5
MEDIUM_ASSET_SIZE = GRID_SIZE * 3
LARGE_ASSET_SIZE = GRID_SIZE * 4
EXTRA_LARGE_ASSET_SIZE = GRID_SIZE * 6

WINDOW_SIZE_X = 1280
WINDOW_SIZE_Y = 720
MARGIN = GRID_SIZE // 2
CENTER_X = WINDOW_SIZE_X // 2

SECTOR_TITLE_Y = GRID_SIZE * 16.5
SECTOR_COVER_Y = SECTOR_TITLE_Y - (GRID_SIZE * 9.5)
SECTOR_CONTROLS_Y = SECTOR_COVER_Y - (GRID_SIZE * 4.5)
SECTOR_TRACK_Y = SECTOR_CONTROLS_Y - (GRID_SIZE * 2)

# Volume offsets
VOLUME_SLIDER_OFFSET_X = GRID_SIZE * 9
VOLUME_BUTTON_OFFSET_X = GRID_SIZE * 7
VOLUME_SLIDER_OFFSET_Y = SMALL_ASSET_SIZE / 1.3
VOLUME_BUTTON_OFFSET_Y = SMALL_ASSET_SIZE / 3

Window.size = (WINDOW_SIZE_X, WINDOW_SIZE_Y)
Window.title = "SonoBlast"
Window.fullscreen = True

class VolumeButton(ButtonBehavior, Image):
    """@brief Image-based button for volume control."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (SMALL_ASSET_SIZE, SMALL_ASSET_SIZE)


class VolumeSlider(Slider):
    """@brief Custom slider with extended touch and canvas-based cursor."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.min = 0
        self.max = 10
        self.value = 5
        self.step = 1
        self.size_hint = (None, None)
        self.size = (GRID_SIZE * 6, GRID_SIZE // 4)
        self.cursor_size = (0, 0)
        self.background_width = 0
        
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
            Color(1, 0.5, 1, 1)
            self.fg_rect = Rectangle(pos=self.pos, size=(self.width * (self.value / self.max), self.height))

        with self.canvas.after:
            self.custom_cursor = Rectangle(source="images/cursor.png", size=(GRID_SIZE, GRID_SIZE))
        self.bind(pos=self.update_canvas, size=self.update_canvas, value=self.update_canvas)

        self.update_canvas()

    def update_canvas(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.fg_rect.size = (self.width * ((self.value - self.min) / float(self.max - self.min)), self.height)
        self.fg_rect.pos = self.pos

        ratio = (self.value - self.min) / float(self.max - self.min)
        cursor_x = self.x + ratio * self.width - self.custom_cursor.size[0] / 2
        cursor_y = self.y + self.height / 2 - self.custom_cursor.size[1] / 2
        self.custom_cursor.pos = (cursor_x, cursor_y)

    def on_touch_down(self, touch):
        margin = GRID_SIZE
        if self.x <= touch.x <= self.right and self.y - margin <= touch.y <= self.top + margin:
            ratio = max(0.0, min(1.0, (touch.x - self.x) / self.width))
            self.value = self.min + ratio * (self.max - self.min)
            return True
        
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):

        return self.on_touch_down(touch)


class TrackSlider(Slider):
    """@brief Non-interactive track position slider."""
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
            Color(1, 1, 1, 1)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
            Color(1, 0.5, 1, 1)
            self.fg_rect = Rectangle(pos=self.pos, size=(self.width * (self.value / self.max), self.height))

        self.bind(pos=self.update_canvas, size=self.update_canvas, value=self.update_canvas)

    def update_canvas(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

        self.fg_rect.size = (self.width * ((self.value - self.min) / float(self.max - self.min)), self.height)
        self.fg_rect.pos = self.pos


class ToggleImageButton(ButtonBehavior, Image):
    """@brief Base class for toggle image buttons (e.g., forward/reverse)."""
    def __init__(self, source_off, source_on, **kwargs):
        super().__init__(**kwargs)
        self.state_on = False
        self.source_off = source_off
        self.source_on = source_on
        self.source = self.source_off
        self.size_hint = (None, None)

    def on_press(self):
        self.state_on = True
        self.source = self.source_on

    def on_release(self):
        self.state_on = False
        self.source = self.source_off


class PlayButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.state_on = False
        self.source = "images/play.png"
        self.size_hint = (None, None)
        self.size = (LARGE_ASSET_SIZE, LARGE_ASSET_SIZE)

        self.debounce_time = 0.4  # seconds
        self.last_pressed = 0

    def on_press(self):
        now = time()
        if now - self.last_pressed < self.debounce_time:
            return  # Ignore press if it's too soon
        self.last_pressed = now

        self.state_on = not self.state_on
        self.source = "images/pause.png" if self.state_on else "images/play.png"


class Cover(ButtonBehavior, Image):
    """@brief Decorative or interactive cover image."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = "images/dots.png"
        self.size_hint = (None, None)
        self.size = (EXTRA_LARGE_ASSET_SIZE, EXTRA_LARGE_ASSET_SIZE)


class SonoplastUI(FloatLayout):
    """@brief Main UI layout for the SonoBlast player."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.15, 0, 0.18, 1)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)

        self.create_controls()
        self.create_labels()
        self.create_volume_controls()
        self.create_track_slider()

    def create_controls(self):
        self.rev_btn = ToggleImageButton("images/rev_dis.png", "images/rev_en.png",
                                         size=(MEDIUM_ASSET_SIZE, MEDIUM_ASSET_SIZE),
                                         pos=(CENTER_X - (LARGE_ASSET_SIZE / 2) - MEDIUM_ASSET_SIZE - GRID_SIZE / 2,
                                              SECTOR_CONTROLS_Y + (LARGE_ASSET_SIZE / 2 - MEDIUM_ASSET_SIZE / 2)))
        self.play_btn = PlayButton(pos=(CENTER_X - (LARGE_ASSET_SIZE / 2), SECTOR_CONTROLS_Y))
        self.fwd_btn = ToggleImageButton("images/forw_dis.png", "images/forw_en.png",
                                         size=(MEDIUM_ASSET_SIZE, MEDIUM_ASSET_SIZE),
                                         pos=(CENTER_X + (LARGE_ASSET_SIZE / 2) + GRID_SIZE / 2,
                                              SECTOR_CONTROLS_Y + (LARGE_ASSET_SIZE / 2 - MEDIUM_ASSET_SIZE / 2)))
        self.cover_btn = Cover(pos=(CENTER_X - (EXTRA_LARGE_ASSET_SIZE / 2), SECTOR_COVER_Y))

        for btn in [self.rev_btn, self.play_btn, self.fwd_btn, self.cover_btn]:
            self.add_widget(btn)

    def create_labels(self):
        self.sono_label = Label(text="Sono", markup=True, font_size=GRID_SIZE * 2.5,
                                font_name="fonts/RobotoCondensed-Regular.ttf", color=(1, 0.5, 1, 1), size_hint=(None, None))
        self.blast_label = Label(text="Blast", markup=True, font_size=GRID_SIZE * 2.5,
                                 font_name="fonts/RobotoCondensed-ExtraBold.ttf", color=(1, 0.5, 1, 1), size_hint=(None, None))
        self.registerd_label = Label(text="®", font_size=GRID_SIZE,
                                     font_name="fonts/RobotoCondensed-Regular.ttf", color=(1, 0.5, 1, 1), size_hint=(None, None))
        self.desc_label = Label(text="a sonoplast player_", font_size=GRID_SIZE,
                                font_name="fonts/Orbitron-Regular.ttf", color=(1, 1, 1, 1), size_hint=(None, None))
        self.time_label = Label(text="00:00", font_size=GRID_SIZE / 1.5,
                                font_name="fonts/RobotoCondensed-Regular.ttf", color=(1, 1, 1, 1), size_hint=(None, None))
        self.time_fim_label = Label(text="00:00", font_size=GRID_SIZE / 1.5,
                                    font_name="fonts/RobotoCondensed-Regular.ttf", color=(1, 1, 1, 1), size_hint=(None, None))

        for lbl in [self.sono_label, self.blast_label, self.registerd_label, self.desc_label, self.time_label, self.time_fim_label]:
            lbl.texture_update()
            lbl.size = lbl.texture_size
            self.add_widget(lbl)

        self.sono_label.pos = (CENTER_X - self.sono_label.width - GRID_SIZE / 3, SECTOR_TITLE_Y - self.sono_label.height + GRID_SIZE)
        self.blast_label.pos = (self.sono_label.right, SECTOR_TITLE_Y - self.blast_label.height + GRID_SIZE)
        self.registerd_label.pos = (self.blast_label.right, self.blast_label.top - self.registerd_label.height)
        self.desc_label.pos = (CENTER_X - self.desc_label.width / 2, SECTOR_TITLE_Y - self.blast_label.height)
        self.time_label.pos = (CENTER_X - GRID_SIZE * 4 - self.time_label.width - GRID_SIZE / 2,
                               SECTOR_TRACK_Y + self.time_label.height * 1.2)
        self.time_fim_label.pos = (CENTER_X + GRID_SIZE * 4 + GRID_SIZE / 2,
                                   SECTOR_TRACK_Y + self.time_fim_label.height * 1.2)

    def create_volume_controls(self):
        self.volume_slider = VolumeSlider(pos=(CENTER_X + VOLUME_SLIDER_OFFSET_X, SECTOR_TRACK_Y + VOLUME_SLIDER_OFFSET_Y))
        self.vol_up = VolumeButton(source="images/vol_up.png", pos=(CENTER_X + VOLUME_BUTTON_OFFSET_X, SECTOR_TRACK_Y + VOLUME_BUTTON_OFFSET_Y))
        self.vol_up.bind(on_release=lambda _: self.adjust_volume(1))

        self.add_widget(self.volume_slider)
        self.add_widget(self.vol_up)

    def create_track_slider(self):
        self.track_slider = TrackSlider(pos=(CENTER_X - GRID_SIZE * 4, SECTOR_TRACK_Y + VOLUME_SLIDER_OFFSET_Y))
        self.add_widget(self.track_slider)

    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def adjust_volume(self, delta):
        new_val = self.volume_slider.value + delta
        self.volume_slider.value = max(self.volume_slider.min, min(self.volume_slider.max, new_val))


class SonoplastApp(App):
    """@brief Entry point for the SonoBlast Kivy app."""
    def build(self):
        return SonoplastUI()


if __name__ == "__main__":
    SonoplastApp().run()
