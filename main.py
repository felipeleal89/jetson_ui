from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

class MainUI(BoxLayout):
    def play(self):
        print("▶️ Play pressed")

    def stop(self):
        print("⛔ Emergency Stop!")

class SonoplastApp(App):
    def build(self):
        return MainUI()

if __name__ == "__main__":
    SonoplastApp().run()
