# @Description: TODO
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/4/17 11:22
# @File : setup.py
import re
import wmi
import random
import base64
from pyDes import *
import os
import sys
import time
import json
import threading
import license
import datetime
import pandts
import seleninm
import openpyxl
import pandas as pd
import requests
from peewee import *

try:
    res = 0
    res = pandts.main()

    if (res == 0) or (res == -1):
        sys.exit()
    if res == 1:
        time.sleep(10000)
except:
    if res == 0:
        sys.exit()
    if not seleninm.db.is_closed():
        seleninm.db.close()

    print('***********************************')
    print('***********************************')
    print('出错')
    time.sleep(10000)
