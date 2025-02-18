import tkinter
from url import URL
import tkinter.font

def lex(body):
    out = []
    buffer = ""
    in_tag = False
    for c in body:
        if c == "<":
            in_tag = True
            if buffer: out.append(Text(buffer))
            buffer = ""
        elif c == ">":
            in_tag = False
            out.append(Tag(buffer))
            buffer = ""
        else:
            buffer += c
    if not in_tag and buffer:
        out.append(Text(buffer))
    return out

WIDTH, HEIGHT = 800, 600
HSTEP, VSTEP = 13, 18

SCROLL_STEP = 100

def layout(tokens):
    display_list = []
    cursor_x, cursor_y = HSTEP, VSTEP
    for tok in tokens:
        w = font.measure(word)
        if isinstance(tok, Text):
            for word in tok.text.split():
                font = tkinter.font.Font(size=16, weight=weight, slant=style,)
                display_list.append((cursor_x, cursor_y, word, font))
                cursor_x += w + font.measure(" ")
                if cursor_x + w >= WIDTH - HSTEP:
                    cursor_y += font.metrics("linespace") * 1.25
                    cursor_x = HSTEP
        elif tok.tag == "i":
            style = "italic"
        elif tok.tag == "/i":
            style = "roman"
        elif tok.tag == "b":
            weight = "bold"
        elif tok.tag == "/b":
            weight = "normal"
    return display_list

class Browser:
    def __init__(self):
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(
            self.window,
            width=WIDTH,
            height=HEIGHT
        )

        self.canvas.pack()

        self.scroll = 0
        self.window.bind("<Down>", self.scrolldown)

    def load(self, url):
        body = url.request()
        text = lex(body)
        self.display_list = layout(text)
        self.draw()

    def draw(self):
        self.canvas.delete("all")
        for x, y, c, d in self.display_list:
            if y > self.scroll + HEIGHT: continue
            if y + VSTEP < self.scroll: continue
            self.canvas.create_text(x, y - self.scroll, text=c, anchor='nw', font=d)

    def scrolldown(self, e):
        self.scroll += SCROLL_STEP
        self.draw()

Class Text:
    def __init__(self, text):
        self.text = text

Class Tag:
    def __init__(self, tag):
        self.tag = tag

if __name__ == "__main__":
    import sys

    Browser().load(URL(sys.argv[1]))
    tkinter.mainloop()