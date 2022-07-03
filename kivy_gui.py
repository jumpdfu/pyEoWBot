from kivy.app import App
from kivy.lang.builder import Builder
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from eowbot import scan_map


class EoWApp(App):
    def build(self):
        bl = BoxLayout()
        bl.orientation = 'vertical'
        btn_refresh = Button(text='Refresh')
        btn_refresh.size_hint = 1, 0.05
        bl.add_widget(btn_refresh)
        self.gl = GridLayout(size_hint=(1, 0.95))
        self.gl.rows = 21
        self.draw_map()
        bl.add_widget(self.gl)

        return bl

    def draw_map(self):
        scanned_map = scan_map()
        for i in range(21):
            for j in range(21):
                index = i + j * 21
                self.gl.add_widget(Button(text=str(scanned_map[index][1])))
        print('Refresh button pressed')


if __name__ == "__main__":
    EoWApp().run()
