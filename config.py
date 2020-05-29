from enum import Enum

class DashThemeEnum(Enum):
    Dark = 1
    White = 2

# Choose Theme:
DASH_THEME = DashThemeEnum.Dark


if DASH_THEME == DashThemeEnum.Dark:
    BACKGROUND_COLOR = '#black'
    IS_DARK = True
    FONT_COLOR = 'white'
elif DASH_THEME == DashThemeEnum.White:
    BACKGROUND_COLOR = '#white'
    IS_DARK = False
    FONT_COLOR = 'black'
else:
    raise Exception(f"No a legit DashThemeEnum {DASH_THEME}")