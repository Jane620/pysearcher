#-*- coding:utf-8 -*-

__author__ = 'wangjf'

import wx
import os,subprocess
from agithub import GitHub

class SearchFrame(wx.Frame):
    pass

if __name__ == '__main__':
    app = wx.App()
    SearchFrame(None)
    app.MainLoop()