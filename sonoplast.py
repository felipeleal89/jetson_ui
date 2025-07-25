from kivy.app import App
from kivy.uix.boxlayout import BoxLayout


class SonoplastUI(BoxLayout):
    def play(self):
        print("<INFO> Play pressed")

    def stop(self):
        print("<WARN> Emergency Stop!")

class SonoplastApp(App):
    def build(self):
        return SonoplastUI()

if __name__ == "__main__":
    SonoplastApp().run()
