from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.config import Config
from kivy.uix.image import Image
from kivy.uix.button import ButtonBehavior

Window.size = (1280, 720)
Window.title = "SonoBlast"
Window.borderless = True
#Window.fullscreen = True


class PlayButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.state_on = False
    def on_press(self):
        self.state_on = not self.state_on
        self.source = (
            "images/pause.png" if self.state_on else "images/play.png"
        )

class ReverseButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.state_on = False
    def on_press(self):
        self.state_on = not self.state_on
        self.source = (
            "images/rev_en.png" if self.state_on else "images/rev_dis.png"
        )
    def on_release(self):
        self.state_on = not self.state_on
        self.source = (
            "images/rev_en.png" if self.state_on else "images/rev_dis.png"
        )

class ForwardButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.state_on = False
    def on_press(self):
        self.state_on = not self.state_on
        self.source = (
            "images/forw_en.png" if self.state_on else "images/forw_dis.png"
        )
    def on_release(self):
        self.state_on = not self.state_on
        self.source = (
            "images/forw_en.png" if self.state_on else "images/forw_dis.png"
        )

class SonoplastUI(FloatLayout):
    pass

class SonoplastApp(App):
    def build(self):
        return SonoplastUI()

if __name__ == "__main__":
    SonoplastApp().run()
