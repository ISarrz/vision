from flet import *
from flet_multi_page import subPage
import json
DG = "#1C1F22"
BG = "#23272a"
G = "#2c2f33"
LG = "#99aab5"
with open('data/settings.json', 'r') as file:
    settings_data = json.load(file)

buttons_style = ButtonStyle(
    color={
        MaterialState.HOVERED: colors.WHITE,
        MaterialState.DEFAULT: LG,
    },
    overlay_color=colors.TRANSPARENT,
)
buttons_style_red = ButtonStyle(
    color={
        MaterialState.HOVERED: colors.RED,
        MaterialState.DEFAULT: LG,
    },
    overlay_color=colors.TRANSPARENT,
)
buttons_style_light_red = ButtonStyle(
    color={
        MaterialState.HOVERED: colors.RED,
        MaterialState.DEFAULT: DG,
    },
    overlay_color=colors.TRANSPARENT,
)
buttons_style_light_green = ButtonStyle(
    color={
        MaterialState.HOVERED: colors.GREEN,
        MaterialState.DEFAULT: DG,
    },
    overlay_color=colors.TRANSPARENT,
)

