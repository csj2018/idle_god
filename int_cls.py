import re, random, pickle, time, threading
from src.cls.NPC import *
from src.cls.World import *
from src.cls.Event import *


境界 = ['\033[36m炼气期\033[0m', '\033[36m筑基期\033[0m', '\033[36m金丹期\033[0m', '\033[36m元婴期\033[0m',
        '\033[36m出窍期\033[0m', '\033[36m分神期\033[0m', '\033[36m合体期\033[0m', '\033[36m渡劫期\033[0m',
        '\033[36m大乘期\033[0m','\033[36m飞升\033[0m']
小境界 = ['一重天', '二重天', '三重天', '四重天', '五重天','六重天','七重天','八重天','九重天','大圆满']

cfg = {}
event = Event()
world = World()
world.cfg = cfg
world.initial()

from src.cls.Danmu import *
danmu = Danmu()