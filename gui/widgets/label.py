# label.py Extension to micro-gui providing the Label class

# Released under the MIT License (MIT). See LICENSE.
# Copyright (c) 2021-2024 Peter Hinch
from gui.core.tgui import Widget, display
from gui.core.writer import Writer
from gui.core.colors import *

# text: str display string int save width
class Label(Widget):
    LEFT = 0
    CENTRE = 1
    RIGHT = 2

    def __init__(
        self,
        writer,
        row,
        col,
        text,
        invert=False,
        fgcolor=None,
        bgcolor=None,
        bdcolor=False,
        justify=0,
    ):
        self.writer = writer
        self.justify = justify
        # Determine width of object
        if isinstance(text, int):
            width = text
            text = None
        else:
            width = writer.stringlen(text)
        height = writer.height
        self.invert = invert
        super().__init__(writer, row, col, height, width, fgcolor, bgcolor, bdcolor)
        self.tcol = col
        if text is not None:
            self.value(text, invert)

    def value(
        self, text=None, invert=False, fgcolor=None, bgcolor=None, bdcolor=None, justify=None
    ):
        if text is not None:
            sl = self.writer.stringlen(text)
            if justify is None:
                justify = self.justify
            self.tcol = self.col  # Default is left justify
            if sl > self.width:  # Clip
                font = self.writer.font
                pos = 0
                n = 0
                for ch in text:
                    pos += font.get_ch(ch)[2]  # width of current char
                    if pos > self.width:
                        break
                    n += 1
                text = text[:n]
            elif justify == 1:  # Centre
                self.tcol = self.col + (self.width - sl) // 2
            elif justify == 2:  # Right
                self.tcol = self.col + self.width - sl

        txt = super().value(text)
        self.draw = True  # Redraw unconditionally: colors may have changed.
        self.invert = invert
        self.fgcolor = self.def_fgcolor if fgcolor is None else fgcolor
        self.bgcolor = self.def_bgcolor if bgcolor is None else bgcolor
        if bdcolor is False:
            self.def_bdcolor = False
        self.bdcolor = self.def_bdcolor if bdcolor is None else bdcolor
        return txt

    def show(self):  # Passive: no need to test show return value.
        super().show(False)  # Honour background. Draw or erase border
        if isinstance(txt := super().value(), str):
            display.print_left(
                self.writer, self.tcol, self.row, txt, self.fgcolor, self.bgcolor, self.invert
            )
