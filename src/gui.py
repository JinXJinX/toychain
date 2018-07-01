from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.config import Config
Config.set('graphics', 'width', '450')
Config.set('graphics', 'height', '600')
# Create both screens. Please note the root.manager.current: this is how
# you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.


# Declare both screens
class MenuScreen(Screen):
    pass


class TransferScreen(Screen):
    pass


class InfoScreen(Screen):
    pass


class ToyChainApp(App):

    def build(self):
        # Create the screen manager
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(TransferScreen(name='transfer'))
        sm.add_widget(InfoScreen(name='info'))
        return sm


if __name__ == '__main__':
    ToyChainApp().run()
