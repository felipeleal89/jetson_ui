from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window

Window.original_size = (1280, 720)
Window.resizable = False
Window.title = "Sonoplast"

class SonoplastUI(FloatLayout):
    def play(self):
        print("<INFO> Play pressed")

    def stop(self):
        print("<WARN> Emergency Stop!")

class SonoplastApp(App):
    def build(self):
        return SonoplastUI()

if __name__ == "__main__":
    SonoplastApp().run()
