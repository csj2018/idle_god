import re, random, pickle, time, threading
from src.cls.NPC import *
from src.cls.World import *
from src.cls.Event import *

front = '\033[36m'
境界 = ['炼气期', '筑基期', '金丹期', '元婴期', '出窍期', '分神期', '合体期', '渡劫期', '大乘期',' 飞升']
小境界 = ['一重天', '二重天', '三重天', '四重天', '五重天','六重天','七重天','八重天','九重天','大圆满']

cfg = {}
event = Event()
world = World()
world.cfg = cfg
world.initial()

from src.cls.Danmu import *
danmu = Danmu()