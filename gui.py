import tkinter as tk
import tkinter.font as tkFont
import keyboard
import eowbot as bot


class App:
    def __init__(self, form_root):
        # setting title
        form_root.title("EoW Bot")
        # setting window size
        width = 230
        height = 195
        screenwidth = form_root.winfo_screenwidth()
        screenheight = form_root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        form_root.geometry(alignstr)
        form_root.resizable(width=False, height=False)

        btnRecStart = tk.Button(form_root)
        btnRecStart["bg"] = "#f0f0f0"
        btnRecStart["cursor"] = "arrow"
        ft = tkFont.Font(family='Times', size=10)
        btnRecStart["font"] = ft
        btnRecStart["fg"] = "#000000"
        btnRecStart["justify"] = "center"
        btnRecStart["text"] = "Start Recording"
        btnRecStart["relief"] = "groove"
        btnRecStart.place(x=10, y=10, width=100, height=50)
        btnRecStart["command"] = self.btn_rec_start

        btnRecPause = tk.Button(form_root)
        btnRecPause["bg"] = "#f0f0f0"
        btnRecPause["cursor"] = "arrow"
        ft = tkFont.Font(family='Times', size=10)
        btnRecPause["font"] = ft
        btnRecPause["fg"] = "#000000"
        btnRecPause["justify"] = "center"
        btnRecPause["text"] = "Pause Recording"
        btnRecPause["relief"] = "groove"
        btnRecPause.place(x=10, y=70, width=100, height=50)
        btnRecPause["command"] = self.btn_rec_pause

        btnRecStop = tk.Button(form_root)
        btnRecStop["bg"] = "#f0f0f0"
        btnRecStop["cursor"] = "arrow"
        ft = tkFont.Font(family='Times', size=10)
        btnRecStop["font"] = ft
        btnRecStop["fg"] = "#000000"
        btnRecStop["justify"] = "center"
        btnRecStop["text"] = "Stop Recording"
        btnRecStop["relief"] = "groove"
        btnRecStop.place(x=10, y=130, width=100, height=50)
        btnRecStop["command"] = self.btn_rec_stop

        btnTrackSelect = tk.Button(form_root)
        btnTrackSelect["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times', size=10)
        btnTrackSelect["font"] = ft
        btnTrackSelect["fg"] = "#000000"
        btnTrackSelect["justify"] = "center"
        btnTrackSelect["text"] = "Select Track"
        btnTrackSelect["relief"] = "groove"
        btnTrackSelect.place(x=120, y=10, width=100, height=50)
        btnTrackSelect["command"] = self.btn_track_select

        btnTrackPlay = tk.Button(form_root)
        btnTrackPlay["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times', size=10)
        btnTrackPlay["font"] = ft
        btnTrackPlay["fg"] = "#000000"
        btnTrackPlay["justify"] = "center"
        btnTrackPlay["text"] = "Start Track"
        btnTrackPlay["relief"] = "groove"
        btnTrackPlay.place(x=120, y=70, width=100, height=50)
        btnTrackPlay["command"] = self.btn_track_play

        btnTrackPause = tk.Button(form_root)
        btnTrackPause["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times', size=10)
        btnTrackPause["font"] = ft
        btnTrackPause["fg"] = "#000000"
        btnTrackPause["justify"] = "center"
        btnTrackPause["text"] = "Pause/Play Track"
        btnTrackPause["relief"] = "groove"
        btnTrackPause.place(x=120, y=130, width=100, height=50)
        btnTrackPause["command"] = self.btn_track_pause

    @staticmethod
    def btn_rec_start():
        print("Запись начата")
        bot.track_rec('Paladin Temple to Blade Room.json')

    @staticmethod
    def btn_rec_pause(i=None):
        i += 1
        print("Запись приостановлена")
        if i % 2 == 0:
            keyboard.send("alt+F10")
        else:
            keyboard.send("alt+F11")

    @staticmethod
    def btn_rec_stop():
        print("Запись остановлена")
        keyboard.send("alt+F12")

    @staticmethod
    def btn_track_select(self=None):
        print("Выбрать трек"+self)

    @staticmethod
    def btn_track_play():
        print("Воспроизведен трек")
        bot.track_go("XO.json")

    @staticmethod
    def btn_track_pause(i=None):
        print("Трек приостановлен")
        i += 1
        if i % 2 == 0:
            keyboard.send("alt+F10")
        else:
            keyboard.send("alt+F11")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
