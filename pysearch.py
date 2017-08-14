#-*- coding:utf-8 -*-

__author__ = 'wangjf'

import wx
import os,subprocess
from agithub import GitHub
from Login_Panel import LoginPanel
from Search_Panel import SearchPanel

class SearchFrame(wx.Frame):
    def __init__(self,*args,**kwargs):
        kwargs.setdefault('size',(600,500))
        wx.Frame.__init__(self,*args,**kwargs)

        self.credentials = {}
        self.orgs = {}

        self.create_controls()
        self.do_layout()
        self.SetTitle('Github Issue Search')

        # 尝试获取缓存
        self.credentials = git_credentials()
        if self.test_credentials():
            self.switch_to_search_panel()
        self.show()

    def login_accepted(self,username,password):
        self.credentials['username'] = username
        self.credentials['password'] = password
        if self.test_credentials():
            self.switch_to_search_panel()

    def test_credentials(self):
        if any(k not in self.credentials for k in ['username','password']):
            return False
        g = GitHub(self.credentials['username'],self.credentials['password'])
        status ,data = g.user.orgs.get()
        if status != 200:
            print('bad credentials in store')
            return False
        self.orgs = [o['login'] for o in data]
        return True

    def switch_to_search_panel(self):
        self.login_panel.Destroy()
        self.search_panel = SearchFrame(self,orgs=self.orgs,credential=self.credentials)
        self.sizer.Add(self.search_panel,1,flag=wx.EXPAND|wx.ALL,border=10)
        self.sizer.Layout()

    def create_controls(self):
        # 创建菜单用于OS X实现cmd+Q的快捷键
        filemenu = wx.Menu()
        filemenu.Append(wx.ID_EXIT,'&Exit')
        menubar = wx.MenuBar()
        menubar.Append(filemenu,'&File')
        self.SetMenuBar(menubar)

        # 实例化登录UI
        self.login_panel = LoginPanel(self,onlogin=self.login_accepted)

    def do_layout(self):
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.login_panel,1,flag=wx.EXPAND|wx.ALL,border=10)



# 获取缓存的登录信息
GITHUB_HOST = 'githun.com'
def git_credentials():
    os.environ['GIT_ASKPASS'] = 'true'
    p = subprocess.Popen(['git','credential','fill'],stdout=subprocess.PIPE,stdin=subprocess.PIPE)
    stdout,stderr = p.communicate('host={}\n\n'.format(GITHUB_HOST))

    creds = {}
    for line in stdout.split('\n')[:-1]:
        k,v = line.split('=')
        creds[k] = v
    return creds




if __name__ == '__main__':
    app = wx.App()
    SearchFrame(None)
    app.MainLoop()