#-*- coding:utf-8 -*-

__author__ = 'wangjf'

from nose.tools import eq_,ok_,raises
import wx
from pysearch import SearchFrame
from Login_Panel import LoginPanel
from Search_Panel import SearchPanel



class TestApp:

    def setUp(self):
        self.f = None
        self.app = wx.App()

    def tearDown(self):
        if self.f:
            self.f.Destroy()
        self.app.Destroy()

    def test_switching_panel(self):
        self.f = SearchFrame(None,id=-1)
        ok_(isinstance(self.f.login_panel,LoginPanel))
        ok_(isinstance(self.f.search_panel,SearchPanel))

        raises(RuntimeError,lambda :self.f.login_panel.Destroy())
        ok_(self.f.search_panel.Destroy())
    pass
