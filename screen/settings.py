from collections import namedtuple

# Namedtuple untuk konfigurasi
Config = namedtuple("Config", ["box_size", "fps"])

# Konstanta
BOX_SIZE = 50
FPS = 60

# Konfigurasi dalam namedtuple
SETTINGS = Config(box_size=BOX_SIZE, fps=FPS)
