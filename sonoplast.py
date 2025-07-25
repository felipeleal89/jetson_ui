from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior

Window.size = (1280, 720)
Window.title = "SonoBlast"
Window.fullscreen = True


class PlayButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = "images/play.png"
        self.state_on = False
    def on_press(self):
        
        self.state_on = not self.state_on
        if self.state_on:
            self.source = "images/play.png"
            print("<INFO> Play enabled")
        else:
            self.source = "images/pause.png"
            print("<INFO> Pause enabled")

class SonoplastUI(FloatLayout):
    pass

class SonoplastApp(App):
    def build(self):
        return SonoplastUI()

if __name__ == "__main__":
    SonoplastApp().run()
