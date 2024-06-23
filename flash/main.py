import time
import M5
from M5 import *
from hardware import *
import requests
import config


# ----------------- Dataclasses to represent Tonies & Sources -------------------
class Tonie:
    def __init__(self, img, tag_id):
        self.img = img
        self.tag_id = tag_id

    def update_url(self, url):
        req = requests.post(
            config.TEDDYCLOUD_URL + "/content/json/set/" + self.tag_id,
            data="source=" + url,
        )
        req.close()


class SelectOption:
    def __init__(self, title, url):
        self.title = title
        self.url = url


# --------------------- Screens --------------------
class Screen:
    def __init__(self):
        self.elements = []

    def add(self, element):
        self.elements.append(element)
        return element

    def set_visible(self, value):
        for e in self.elements:
            e.setVisible(value)

    def on_select(self):
        print("Select")

    def on_confirm(self):
        print("Confirm")

    def on_back(self):
        print("Back")

    def update(self):
        pass


class ToniesScreen(Screen):
    def __init__(self, app, tonies):
        Screen.__init__(self)
        self._tonies = tonies
        self._selected_idx = 0
        self._lbl_main = self.add(
            Widgets.Label(
                "Click: Select", 4, 209, 1.0, 0x000000, 0xFFFFFF, Widgets.FONTS.DejaVu12
            )
        )
        self._lbl_main_2 = self.add(
            Widgets.Label(
                "Hold: Confirm", 4, 223, 1.0, 0x000000, 0xFFFFFF, Widgets.FONTS.DejaVu12
            )
        )
        # self._lbl_main_3 = self.add(
        #     Widgets.Label(
        #         "RightBtn: Back", 4, 195, 1.0, 0x000000, 0xFFFFFF, Widgets.FONTS.DejaVu12
        #     )
        # )
        self._img_main = self.add(Widgets.Image(self.current_tonie.img, 0, 0))
        self._app = app

    @property
    def current_tonie(self):
        return self._tonies[self._selected_idx]

    def on_select(self):
        self._selected_idx += 1
        if self._selected_idx >= len(self._tonies):
            self._selected_idx = 0
        self._img_main.setImage(self.current_tonie.img)

    def on_confirm(self):
        self._app.show_screen(self._app.select_screen)

    def on_back(self):
        Power.powerOff()


class SelectScreen(Screen):
    def __init__(self, app, options):
        Screen.__init__(self)
        self._labels = []
        self._margin_top = 5
        self._margin_left = 2
        self._row_height = 15
        self._voffset = 0
        self._selected_color = 0xFF0000
        self._normal_color = 0x000000
        self._ticks = 0
        self.selected_idx = 0
        self._options = options
        self._app = app
        for o in options:
            lbl = self.add(
                Widgets.Label(
                    o.title,
                    0,
                    0,
                    1.0,
                    self._normal_color,
                    0xFFFFFF,
                    Widgets.FONTS.DejaVu12,
                )
            )
            self._labels.append(lbl)
        self._labels[self.selected_idx].setColor(self._selected_color, 0xFFFFFF)
        self._layout()
        self.set_visible(False)

    def _y_for_idx(self, idx):
        return self._voffset + self._margin_top + self._row_height * idx

    def _layout(self):
        y = self._voffset + self._margin_top
        for l in self._labels:
            l.setCursor(self._margin_left, y)
            y += self._row_height

    def on_select(self):
        self._labels[self.selected_idx].setColor(self._normal_color, 0xFFFFFF)
        self._labels[self.selected_idx].setCursor(
            self._margin_left, self._y_for_idx(self.selected_idx)
        )
        self.selected_idx += 1
        if self.selected_idx >= len(self._labels):
            self.selected_idx = 0
            self._voffset = 0
            self._layout()
            self.set_visible(True)  # Necessary to redraw the screen
        selected_y = self._y_for_idx(self.selected_idx)
        if selected_y + self._row_height > config.SCREEN_HEIGHT:
            self._voffset += config.SCREEN_HEIGHT - selected_y - self._row_height
            self._layout()
        self._labels[self.selected_idx].setColor(self._selected_color, 0xFFFFFF)

    def update(self):
        # Animation of the selected thing
        t = time.ticks_ms()
        dx = t % 1000
        if dx > 500:
            dx = 999 - dx
        self._labels[self.selected_idx].setCursor(
            self._margin_left + dx // 200, self._y_for_idx(self.selected_idx)
        )

    def on_confirm(self):
        o = self._options[self.selected_idx]
        self._app.tonies_screen.current_tonie.update_url(o.url)
        Speaker.tone(2000, 50)
        self._app.show_screen(self._app.tonies_screen)

    def on_back(self):
        self._app.show_screen(self._app.tonies_screen)


# ----------------- App -------------------
class App:
    def __init__(self, config):
        M5.begin()
        Speaker.setVolumePercentage(0.5)
        Widgets.fillScreen(0xFFFFFF)
        self.select_screen = SelectScreen(
            self, [SelectOption(**source) for source in config.SOURCES]
        )
        self.tonies_screen = ToniesScreen(
            self, [Tonie(**tonie) for tonie in config.TONIES]
        )
        self.current_screen = self.tonies_screen
        BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=self.btnA_click)
        BtnA.setCallback(type=BtnA.CB_TYPE.WAS_HOLD, cb=self.btnA_hold)
        BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=self.btnB_click)

    def show_screen(self, screen):
        self.current_screen.set_visible(False)
        screen.set_visible(True)
        self.current_screen = screen

    def update(self):
        M5.update()
        self.current_screen.update()

    def btnA_click(self, state):
        self.current_screen.on_select()

    def btnB_click(self, state):
        self.current_screen.on_back()

    def btnA_hold(self, state):
        self.current_screen.on_confirm()


# ----------------- Main -------------------
def main():
    try:
        app = App(config)
        while True:
            app.update()
    except (Exception, KeyboardInterrupt) as e:
        try:
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("Please update to latest firmware")


if __name__ == "__main__":
    main()
