from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.button import ButtonBehavior
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.graphics import Color, Rectangle

# Global constants
GRID_SIZE = 20
SMALL_ASSET_SIZE = 50
MEDIUM_ASSET_SIZE = 100
LARGE_ASSET_SIZE = 150
EXTRA_LARGE_ASSET_SIZE = 200
WINDOW_SIZE_X = 1280
WINDOW_SIZE_Y = 720
MARGIN = 5


# Configure window dimensions and style
Window.size = (WINDOW_SIZE_X, WINDOW_SIZE_Y)
Window.title = "SonoBlast"
Window.fullscreen = True  # Uncomment for fullscreen on deploy

# Image-based button with fixed size (used for volume control)
class VolumeButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (SMALL_ASSET_SIZE, SMALL_ASSET_SIZE)


# Custom volume slider: visually styled with no cursor
class VolumeSlider(Slider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.min = 0
        self.max = 10
        self.value = 5
        self.step = 1
        self.size_hint = (None, None)
        self.size = (960, 8)
        self.cursor_size = (0, 0)
        self.disabled = True  # Disable direct touch

        # Custom canvas for white track and pink fill
        with self.canvas.before:
            self.bg_color = Color(1, 1, 1, 1)  # white background
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
            self.fg_color = Color(1, 0.5, 1, 1)  # pink progress
            self.fg_rect = Rectangle(pos=self.pos, size=(self.width * ((self.value - self.min) / float(self.max - self.min)), self.height))

        self.bind(pos=self.update_canvas, size=self.update_canvas, value=self.update_canvas)

    def update_canvas(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.fg_rect.pos = self.pos
        self.fg_rect.size = (self.width * ((self.value - self.min) / float(self.max - self.min)), self.height)


# Custom slider for track progress: enabled and styled
class TrackSlider(Slider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.min = 0
        self.max = 100
        self.value = 20
        self.step = 1
        self.size_hint = (None, None)
        self.size = (480, 8)
        self.cursor_size = (0, 0)
        self.disabled = True  # Disable direct touch

        # Custom track background and fill
        with self.canvas.before:
            self.bg_color = Color(1, 1, 1, 1)  # white background
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
            self.fg_color = Color(1, 0.5, 1, 1)  # pink progress
            self.fg_rect = Rectangle(pos=self.pos, size=(self.width * ((self.value - self.min) / float(self.max - self.min)), self.height))

        self.bind(pos=self.update_canvas, size=self.update_canvas, value=self.update_canvas)

    def update_canvas(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.fg_rect.pos = self.pos
        self.fg_rect.size = (self.width * ((self.value - self.min) / float(self.max - self.min)), self.height)


# Custom image buttons
class PlayButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.state_on = False
        self.source = "images/play.png"
        self.size_hint = (None, None)
        self.size = (120, 120)

    def on_press(self):
        self.state_on = not self.state_on
        self.source = "images/pause.png" if self.state_on else "images/play.png"

class Cover(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.state_on = False
        self.source = "images/dots.png"
        self.size_hint = (None, None)
        self.size = (200, 200)
        
class ReverseButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.state_on = False
        self.source = "images/rev_dis.png"
        self.size_hint = (None, None)
        self.size = (120, 120)

    def on_press(self):
        self.state_on = not self.state_on
        self.source = "images/rev_en.png"

    def on_release(self):
        self.state_on = not self.state_on
        self.source = "images/rev_dis.png"


class ForwardButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.state_on = False
        self.source = "images/forw_dis.png"
        self.size_hint = (None, None)
        self.size = (120, 120)

    def on_press(self):
        self.state_on = not self.state_on
        self.source = "images/forw_en.png"

    def on_release(self):
        self.state_on = not self.state_on
        self.source = "images/forw_dis.png"


# Main UI container
class SonoplastUI(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Set background color
        with self.canvas.before:
            Color(0.15, 0, 0.18, 1)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)

        # Add main media buttons
        self.rev_btn = ReverseButton(pos=(240, self.height - 560))
        self.play_btn = PlayButton(pos=(540, self.height - 560))
        self.fwd_btn = ForwardButton(pos=(840, self.height - 560))
        self.cover_btn = Cover(pos=(640-150, self.height - 300))
        self.add_widget(self.rev_btn)
        self.add_widget(self.play_btn)
        self.add_widget(self.fwd_btn)
        self.add_widget(self.cover_btn)

        # Add labels
        self.sono_label = Label(
            text="Sono",
            markup=True,
            font_size=100,
            font_name="fonts/RobotoCondensed-Regular.ttf",
            color=(1, 0.5, 1, 1),
            size_hint=(None, None),
        )
        self.add_widget(self.sono_label)

        self.blast_label = Label(
            text="Blast",
            markup=True,
            font_size=100,
            font_name="fonts/RobotoCondensed-ExtraBold.ttf",
            color=(1, 0.5, 1, 1),
            size_hint=(None, None),
        )
        self.add_widget(self.blast_label)

        self.desc_label = Label(
            text="a sonoloplast player_",
            font_size=32,
            font_name="fonts/Orbitron-Regular.ttf",
            color=(1, 1, 1, 1),
            size_hint=(None, None),
        )
        self.add_widget(self.desc_label)

        # Volume slider and control buttons
        self.volume_slider = VolumeSlider(pos=(340, self.height - 680))
        self.add_widget(self.volume_slider)

        self.vol_down = VolumeButton(source="images/vol_down.png", pos=(MARGIN, WINDOW_SIZE_Y - MARGIN - self.height))
        self.vol_down.bind(on_release=lambda _: self.adjust_volume(-1))
        self.add_widget(self.vol_down)

        self.vol_up = VolumeButton(source="images/vol_up.png", pos=(WINDOW_SIZE_X - MARGIN - self.width, WINDOW_SIZE_Y - MARGIN - self.height))
        self.vol_up.bind(on_release=lambda _: self.adjust_volume(1))
        self.add_widget(self.vol_up)

        # Track progress slider
        self.track_slider = TrackSlider(pos=(140, self.height - 720 + 20))
        self.add_widget(self.track_slider)

        self.bind(size=self.reposition_elements)

    def adjust_volume(self, delta):
        # Increment or decrement volume
        new_val = self.volume_slider.value + delta
        self.volume_slider.value = max(self.volume_slider.min, min(self.volume_slider.max, new_val))

    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def reposition_elements(self, *args):
        # Called when window is resized
        self.rev_btn.pos = (560 - 180, self.height - 590)
        self.play_btn.pos = (560 ,self.height - 590)
        self.fwd_btn.pos = (560 + 180, self.height - 590)
        self.volume_slider.pos = (125, self.height - 630)
        self.vol_down.pos = (MARGIN, self.height - (WINDOW_SIZE_Y - MARGIN - self.vol_down.height))
        self.vol_up.pos = ((WINDOW_SIZE_X - MARGIN - self.vol_up.width), self.height - (WINDOW_SIZE_Y - MARGIN - self.vol_up.height))
        self.track_slider.pos = (400, self.height - 400)
        self.cover_btn.pos = (540, self.height - 360)

        # Update label positions after texture updates
        self.sono_label.texture_update()
        self.sono_label.size = self.sono_label.texture_size
        self.sono_label.pos = (430, self.height - 120)

        self.blast_label.texture_update()
        self.blast_label.size = self.blast_label.texture_size
        self.blast_label.pos = (430 + self.sono_label.texture_size[0], self.height - 120)

        self.desc_label.texture_update()
        self.desc_label.size = self.desc_label.texture_size
        self.desc_label.pos = (460, self.height - 135)


class SonoplastApp(App):
    def build(self):
        return SonoplastUI()


if __name__ == "__main__":
    SonoplastApp().run()
