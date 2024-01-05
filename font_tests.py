
from escpos import config
c = config.Config()
p = c.printer()

phrase = "Sphinx of black quartz, judge my vow\n"
p.set(align="left")
p.text("DEFAULT\n")
p.text(phrase)
p.text("FONT B\n")
p.set(font="b")                                                                                                                                                             
p.text(phrase)
p.set(font="a")
p.text("BOLD\n")
p.set(text_type="b")
p.text(phrase)
p.set(text_type="normal")
p.text("DOUBLE HEIGHT\n")
p.set(height=2)
p.text(phrase)
p.set(height=1)
p.text("INVERT\n")
p.set(invert=True)
p.text(phrase)
p.set(invert=False)
p.text("FLIPPED\n")
p.set(flip=True)
p.text(phrase)
p.set(flip=False)
p.text("Double Width\n")
p.set(width=2)
p.text(phrase)
p.set(text_type="normal")
p.text("UNDERLINE v1\n")
p.set(text_type="u")
p.text(phrase)
p.set(text_type="normal")
p.text("UNDERLINE v2\n")
p.set(text_type="u2")
p.text(phrase)
p.set(text_type="normal")
p.text("SIZE 3-8 H&W\n")
p.set(height=3,width=3)
p.text(phrase)
p.set(height=4,width=4)
p.text(phrase)
p.set(height=5,width=5)
p.text(phrase)
p.set(height=6,width=6)
p.text(phrase)
p.set(height=7,width=7)
p.text(phrase)
p.set(height=8,width=8)
p.text(phrase)
p.set(text_type="normal")

p.cut()
