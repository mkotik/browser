from tkinter import font
from text import Text


class Layout:
    def __init__(self, tokens):
        self.line = []
        self.display_list = []
        self.HSTEP = 13
        self.VSTEP = 18
        self.cursor_x = self.HSTEP
        self.cursor_y = self.VSTEP
        self.width = 800
        self.height = 600
        self.scroll_width = 20
        self.weight = "normal"
        self.style = "roman"
        self.size = 12
        # self.flush()
        for tok in tokens:
            self.token(tok)
        self.flush()

    def token(self, tok):
        if isinstance(tok, Text):
            for word in tok.text.split():
                active_font = font.Font(
                    size=self.size,
                    weight=self.weight,
                    slant=self.style,
                )
                w = active_font.measure(word) + active_font.measure(" ")
                if self.cursor_x > (self.width - w - self.scroll_width):
                    self.cursor_x = self.HSTEP
                    self.cursor_y += active_font.metrics("linespace") * 1.25

                self.word(word)
                # self.display_list.append(
                #     (self.cursor_x, self.cursor_y, word, active_font)
                # )
                self.cursor_x += w
        elif tok.tag == "small":
            self.size -= 2
        elif tok.tag == "/small":
            self.size += 2
        elif tok.tag == "big":
            self.size += 4
        elif tok.tag == "/big":
            self.size -= 4
        elif tok.tag == "i":
            self.style = "italic"
        elif tok.tag == "/i":
            self.style = "roman"
        elif tok.tag == "b":
            self.weight = "bold"
        elif tok.tag == "/b":
            self.weight = "normal"

    # ...
    def word(self, word):
        active_font = font.Font(
            size=self.size,
            weight=self.weight,
            slant=self.style,
        )
        w = active_font.measure(word)
        self.line.append((self.cursor_x, word, active_font, self.cursor_y))
        if self.cursor_x + w > self.width - self.HSTEP:
            self.flush()
        # ...

    def flush(self):
        if not self.line:
            return

        baseline = max(font.metrics()["ascent"] for _, _, font, _ in self.line)
        max_descent = max([font.metrics()["descent"] for _, _, font, _ in self.line])

        for x, word, font, y in self.line:
            new_y = y + baseline - font.metrics("ascent")
            self.display_list.append((x, new_y, word, font))

        # self.cursor_y = baseline + 1.25 * max_descent
