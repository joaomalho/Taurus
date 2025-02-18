
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"X:\Taurus Python\market-analyzer\frontend\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("1440x900")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 900,
    width = 1440,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    0.0,
    0.0,
    90.0,
    900.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    90.0,
    0.0,
    1440.0,
    80.0,
    fill="#D9D9D9",
    outline="")

canvas.create_rectangle(
    100.0,
    125.0,
    708.0,
    891.0,
    fill="#D9D9D9",
    outline="")

canvas.create_rectangle(
    729.0,
    125.0,
    1189.0,
    891.0,
    fill="#D9D9D9",
    outline="")

canvas.create_rectangle(
    1209.0,
    125.0,
    1430.0,
    891.0,
    fill="#D9D9D9",
    outline="")

canvas.create_rectangle(
    90.0,
    80.0,
    1440.0,
    116.0,
    fill="#1D241E",
    outline="")

canvas.create_text(
    136.0,
    25.0,
    anchor="nw",
    text="Home Page",
    fill="#000000",
    font=("Poppins ExtraBold", 32 * -1)
)

canvas.create_rectangle(
    111.0,
    83.0,
    201.0,
    113.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    218.0,
    83.0,
    308.0,
    113.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    325.0,
    83.0,
    415.0,
    113.0,
    fill="#000000",
    outline="")

canvas.create_text(
    432.0,
    30.0,
    anchor="nw",
    text="Stocks",
    fill="#000000",
    font=("Poppins ExtraBold", 14 * -1)
)

canvas.create_text(
    507.0,
    30.0,
    anchor="nw",
    text="Currencies",
    fill="#000000",
    font=("Poppins ExtraBold", 14 * -1)
)

canvas.create_text(
    614.0,
    30.0,
    anchor="nw",
    text="ETFs",
    fill="#000000",
    font=("Poppins ExtraBold", 14 * -1)
)
window.resizable(False, False)
window.mainloop()
