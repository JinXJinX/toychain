from argparse import ArgumentParser

import server
from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.config import Config
Config.set('graphics', 'width', '450')
Config.set('graphics', 'height', '600')
Config.set('graphics', 'resizable', False)

app = server.app


class MenuScreen(Screen):
    def on_start(self):
        Clock.schedule_interval(self.update, 2)
        # self.ids.account

    def update(self):
        self.ids.balance = '900'


class TransferScreen(Screen):
    def on_pre_enter(self):
        ids = self.ids
        ids.to_address.text = ''
        ids.amount.text = ''
        ids.fee.text = ''

    def send_coin(self):
        ids = self.ids
        to_address = ids.to_address.text
        amount = ids.amount.text
        fee = ids.fee.text

        try:
            amount = int(amount)
            fee = int(fee)
        except ValueError as e:
            return

        if not (to_address and amount and fee):
            return

        # TODO send coin
        self.manager.current = 'suc'


class SucInfoScreen(Screen):
    pass


class ErrInfoScreen(Screen):
    pass


class ToyChainApp(App):

    def build(self):
        # Create the screen manager
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(TransferScreen(name='transfer'))
        sm.add_widget(SucInfoScreen(name='suc'))
        sm.add_widget(ErrInfoScreen(name='err'))
        return sm


if __name__ == '__main__':
    # TODO
    # parser = ArgumentParser()
    # parser.add_argument('-c', '--config', default='config', type=str,
    #                     help='config file name')
    # args = parser.parse_args()
    # config_filename = args.config
    #
    # app.config.from_object(config_filename)
    # app.config['CONFIG_FILENAME'] = config_filename
    # server.init()
    #
    # app.run(
    #     host=app.config['HOST'],
    #     port=app.config['PORT'],
    #     use_reloader=app.config['USE_RELOADER']
    # )
    # ToyChainApp().run()
