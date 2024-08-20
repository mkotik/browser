import tkinter
from url import URL
from tkinter import font
from text import Text
from layout import Layout

# URL = "https://example.org"

WIDTH, HEIGHT = 800, 600


class Browser:
    def __init__(self):
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.window, width=WIDTH, height=HEIGHT)
        # self.canvas.create_rectangle(100, 100, 100, 100)
        self.canvas.pack()
        self.display_list = []
        self.scroll = 0
        self.debounce_timer = None
        self.text = ""
        self.width = 800
        self.height = 600
        self.scroll_width = 20
        self.total_scroll_height = 1
        self.window.bind("<Down>", self.scrolldown)
        self.window.bind("<Up>", self.scrollup)
        self.window.bind("<MouseWheel>", self.on_mousewheel)
        # self.window.bind("<Configure>", self.on_resize)

    def update_state(self):
        if len(self.display_list) > 0:
            self.total_scroll_height = self.display_list[-1][1] - self.height

    def on_mousewheel(self, e):
        self.scroll -= e.delta
        if self.scroll < 0:
            self.scroll = 0
            return
        self.draw()

    def on_resize(self, event):
        if self.text == "":
            return
        self.width = event.width
        self.height = event.height
        self.display_list = Layout(self.text).display_list
        self.draw()

    def scrolldown(self, e):
        if self.scroll >= self.total_scroll_height:
            return
        self.scroll += SCROLL_STEP
        self.draw()

    def scrollup(self, e):
        if self.scroll < 0:
            return
        self.scroll -= SCROLL_STEP
        self.draw()

    def create_scrollbar(self):
        print(self.total_scroll_height)
        if self.total_scroll_height <= self.height:
            return
        self.canvas.create_rectangle(
            self.width - self.scroll_width,
            0,
            self.width,
            self.height,
            fill="blue",
            outline="blue",
        )
        thumb_height = self.total_scroll_height / self.height
        thumb_top_position = (
            self.scroll / (self.total_scroll_height + VSTEP)
        ) * self.height
        self.canvas.create_rectangle(
            self.width - self.scroll_width,
            thumb_top_position,
            self.width,
            thumb_top_position + thumb_height,
            fill="red",
            outline="red",
        )

    def draw(self):
        self.canvas.delete("all")
        if self.scroll < 0:
            return
        self.create_scrollbar()
        for x, y, c, d in self.display_list:
            if y > self.scroll + HEIGHT:
                continue
            if y + VSTEP < self.scroll:
                continue
            self.canvas.create_text(
                x,
                y - self.scroll,
                text=c,
                font=d,
                anchor="nw",
            )

    def load(self, url):
        # ...
        # self.canvas.create_rectangle(10, 20, 400, 300)
        # self.canvas.create_oval(100, 100, 150, 150)
        # self.canvas.create_text(200, 150, text="Hi!")
        url_lib = URL(url)
        tokens = url_lib.load()

        self.tokens = tokens
        self.display_list = Layout(self.tokens).display_list
        self.total_scroll_height = self.display_list[-1][1] - self.height
        # self.update_state()
        self.draw()


if __name__ == "__main__":
    HSTEP = 13
    VSTEP = 18
    SCROLL_STEP = 18

    # Browser().load("https://browser.engineering/examples/example3-sizes.html")
    # Browser().load("http://example.com/")
    Browser().load("https://browser.engineering/text.html")
    tkinter.mainloop()
