# @Description: TODO
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/4/18 13:00
# @File : license.py


import re
import time

import requests
import wmi
import base64
from pyDes import *


class register:
    def __init__(self):
        self.Des_Key = "MRSUNDAY"
        self.Des_IV = "\x15\1\x2a\3\1\x23\2\0"

    global s
    s = wmi.WMI()

    def get_CPU_info(self):
        cpu = []
        cp = s.Win32_Processor()
        for u in cp:
            cpu.append(
                {
                    "Name": u.Name,
                    "Serial Number": u.ProcessorId,
                    "CoreNum": u.NumberOfCores
                }
            )
        return cpu

    def get_disk_info(self):
        disk = []
        for pd in s.Win32_DiskDrive():
            disk.append(
                {
                    "Serial": s.Win32_PhysicalMedia()[0].SerialNumber.lstrip().rstrip(),
                    "ID": pd.deviceid,
                    "Caption": pd.Caption,
                    "size": str(int(float(pd.Size) / 1024 / 1024 / 1024)) + "G"
                }
            )
        return disk

    def get_network_info(self):
        network = []
        for nw in s.Win32_NetworkAdapterConfiguration():  # IPEnabled=0
            if nw.MACAddress != None:
                network.append(
                    {
                        "MAC": nw.MACAddress,
                        "ip": nw.IPAddress
                    }
                )
        return network

    def get_mainboard_info(self):
        mainboard = []
        for board_id in s.Win32_BaseBoard():
            mainboard.append(board_id.SerialNumber.strip().strip('.'))
        return mainboard

    def getCombinNumber(self):
        a = self.get_network_info()
        b = self.get_CPU_info()
        c = self.get_disk_info()
        d = self.get_mainboard_info()
        machinecode_str = ""
        machinecode_str = machinecode_str + a[0]['MAC'] + b[0]['Serial Number'] + c[0]['Serial'] + d[0]
        selectindex = [15, 30, 32, 38, 43, 46]
        macode = ""

        mac_sub = re.sub(r'\D', '', a[0]['MAC'])

        if mac_sub:
            mac_last_num = int(mac_sub[-1])
        else:
            mac_last_num = 0
        if mac_last_num % 2 == 0:
            index1, index2, m, n = 30, 38, 'B', 'N'
        else:
            index1, index2, m, n = 32, 43, 'F', 'C'
        for i in selectindex:

            if i == index1:
                macode += m
            macode = macode + machinecode_str[i]
            if i == index2:
                macode += n
        return macode

    def Encrypted(self, tr):
        k = des(self.Des_Key, CBC, self.Des_IV, pad=None, padmode=PAD_PKCS5)
        EncryptStr = k.encrypt(tr)
        return base64.b64encode(EncryptStr)

    def checkAuthored(self):
        try:
            ontent = self.getCombinNumber()
            tent = bytes(ontent, encoding='utf-8')
            content = self.Encrypted(tent)
            print(content)
            key = requests.get('http://ss.zzuspc.top/10086_0.txt').text.strip()
            if key:
                key_decrypted = bytes(key, encoding='utf-8')
                if key_decrypted:
                    if key_decrypted == content:
                        return True, 1
                    else:
                        return False, 0
            else:
                return False, 0
        except:
            return False, -1


def start():
    reg = register()
    return reg.checkAuthored()
