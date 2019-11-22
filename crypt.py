#!/usr/bin/env python
# coding:utf-8
"""
  Author:  u"dashmosh" --<1115486651@qq.com>
  Purpose: u"aes crypt"
  Created: 2019/11/21
"""
import os.path
import wx
import aesCrypt
import re

class MainWindow(wx.Frame):
    flg = 'encrypt'

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(800, 600), style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panel = wx.Panel(self, style=wx.TE_MULTILINE)
        self.panel.SetBackgroundColour(wx.LIGHT_GREY)
        self.fin = wx.Button(self.panel, -1, label='选择输入文件', pos=(5, 5))
        self.Bind(wx.EVT_BUTTON, self.OnFin, self.fin)
        self.finText = wx.TextCtrl(self.panel, -1, pos=(110, 5), size=(150, 30), style=wx.TE_READONLY)
        self.fOut = wx.Button(self.panel, -1, label='选择输出文件夹', pos=(280, 5))
        self.Bind(wx.EVT_BUTTON, self.OnFOut, self.fOut)
        self.fOutText = wx.TextCtrl(self.panel, -1, pos=(400, 5), size=(150, 30), style=wx.TE_READONLY)
        self.cText = wx.StaticText(self.panel, -1, label='选择加密(en)或解密(de)：', pos=(558, 9))
        list1 = ['encrypt', 'decrypt']
        self.ch1 = wx.ComboBox(self.panel, -1, value='encrypt', choices=list1, style=wx.CB_SORT | wx.TE_READONLY, pos=(700, 5))
        self.Bind(wx.EVT_COMBOBOX, self.OnCh1, self.ch1)
        self.kText = wx.StaticText(self.panel, -1, label='输入密钥：', pos=(24, 60))
        self.enOrDeKey = wx.TextCtrl(self.panel, -1, pos=(110, 52), size=(150, 30), style=wx.TE_PASSWORD | wx.TE_CENTRE)
        self.enOrDeKey.SetMaxLength(16)
        self.rekText = wx.StaticText(self.panel, -1, label='请再次输入密钥：', pos=(288, 60))
        self.reEnOrDeKey = wx.TextCtrl(self.panel, -1, pos=(400, 52), size=(150, 30), style=wx.TE_PASSWORD | wx.TE_CENTRE)
        self.c2Text = wx.StaticText(self.panel, -1, label='选择模式：', pos=(600, 60))
        list2 = ['CFB', 'ECB', 'CBC', 'CTR', 'OFB']
        self.ch2 = wx.ComboBox(self.panel, -1, value='CFB', choices=list2, style=wx.CB_SORT | wx.TE_READONLY, pos=(700, 52))
        self.do = wx.Button(self.panel, -1, label='执行加密/解密', pos=(300, 110))
        self.Bind(wx.EVT_BUTTON, self.OnDo, self.do)
        self.more = wx.Button(self.panel, -1, label='高级功能', pos=(650, 110))
        self.Bind(wx.EVT_BUTTON, self.OnMore, self.more)
        self.outPut = wx.TextCtrl(self.panel, -1, pos=(5, 170), size=(775, 340), style=wx.TE_READONLY | wx.TE_MULTILINE | wx.TE_LEFT)

        self.CreateStatusBar()  # A StatusBar in the bottom of the window
        # Setting up the menu.
        filemenu = wx.Menu()
        infomenu = wx.Menu()
        # wx.ID_ABOUT and wx.ID_EXIT are standard ids provided by wxWidgets.
        menuAbout = filemenu.Append(wx.ID_ABOUT, "About", " Information about this program")
        menuExit = filemenu.Append(wx.ID_EXIT, "Exit", " Terminate the program")
        modeInfo = infomenu.Append(-1, "modes", " Information about different modes")
        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, 'File')  # Adding the "filemenu" to the MenuBar
        menuBar.Append(infomenu, 'Info')
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.
        # Set events.
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnModeInfo, modeInfo)
        self.Show(True)

    def OnCh1(self, event):
        self.finText.Clear()
        MainWindow.flg = self.ch1.GetValue()

    def OnAbout(self, event):
        dlg = wx.MessageDialog(self, "A cryptor created by dashmosh, using aes to crypt", "About aesCryptor", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()  # finally destroy it when finished.

    def OnExit(self, event):
        self.Close(True)  # Close the frame.

    def OnFin(self, event):
        if MainWindow.flg == 'encrypt':
            dlg = wx.FileDialog(self, u"选择文件", wildcard='all files(*.*)|*.*', style=wx.DD_DEFAULT_STYLE)
        else:
            dlg = wx.FileDialog(self, u"选择文件", wildcard='jy files(*.jy)|*.jy', style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            inpath = dlg.GetPath()  # 文件路径
            self.finText.SetValue(inpath)
        dlg.Destroy()

    def OnFOut(self, event):
        dlg = wx.DirDialog(self, u"选择文件夹", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            outpath = dlg.GetPath()  # 文件夹路径
            self.fOutText.SetValue(outpath)
        dlg.Destroy()

    def OnModeInfo(self, event):
        dlg = wx.MessageDialog(self, "懒得写", "modes information", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()  # finally destroy it when finished.

    def OnMore(self, event):
        dlg = wx.MessageDialog(self, "FUCK U FLOWER !!!", "more information", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()  # finally destroy it when finished.

    def OnDo(self, event):
        textlist = {"in": "./test.jy", "out": "./test1.txt", "str": 'null', "en_or_de": "decrypt", "key": "12345678",
                "IV": "1234567890123456", "mode": "ECB", "way": "file"}
        tempin = self.finText.GetValue()
        self.outPut.Clear()
        if not tempin:
            dlg = wx.MessageDialog(self, "未选择输入文件", "warning", wx.OK)
            dlg.ShowModal()
            dlg.Destroy()  # finally destroy it when finished.
            return
        tempout = self.fOutText.GetValue()
        if not tempout:
            dlg = wx.MessageDialog(self, "未选择输出文件夹", "warning", wx.OK)
            dlg.ShowModal()
            dlg.Destroy()  # finally destroy it when finished.
            return
        temp1 = self.enOrDeKey.GetValue()
        if not temp1:
            dlg = wx.MessageDialog(self, "至少输入一位密钥", "warning", wx.OK)
            dlg.ShowModal()
            dlg.Destroy()  # finally destroy it when finished.
            return
        temp2 = self.reEnOrDeKey.GetValue()
        if temp1 != temp2:
            dlg = wx.MessageDialog(self, "两次输入的密钥不一致", "warning", wx.OK)
            dlg.ShowModal()
            dlg.Destroy()  # finally destroy it when finished.
            return
        self.outPut.AppendText('初始化参数中...请勿关闭程序:' + '\n')
        textlist['en_or_de'] = self.ch1.GetValue()
        textlist['in'] = tempin
        addname = os.path.basename(tempin)
        addname1 = os.path.splitext(addname)[0]
        suffix = '.' + addname.split(".")[-1]
        print(suffix)
        if textlist['en_or_de'] == 'encrypt':
            textlist['out'] = tempout + '\\' + addname1 + '.jy'
        else:
            with open(textlist['in'], 'r') as f:
                con = f.read()
                print(con)
                suffix = ''.join(re.findall('\.[^\.]*$', con))
                print(suffix)
                con = con.rstrip(suffix)
                print(con)
            with open(textlist['in'], 'w') as f:
                f.write(con)
                # 获取后删除存储的文件后缀
            textlist['out'] = tempout + '\\' + addname1 + suffix
        textlist['key'] = temp1
        textlist['mode'] = self.ch2.GetValue()
        print(textlist)
        if textlist['en_or_de'] == 'encrypt':
            self.outPut.AppendText('初始化参数成功，执行加密中...请勿关闭程序:' + '\n')
        else:
            self.outPut.AppendText('初始化参数成功，执行解密中...请勿关闭程序:' + '\n')
        res, time = aesCrypt.startcrypt(textlist)
        if textlist['en_or_de'] == 'encrypt':
            self.outPut.AppendText('加密成功...:' + '\n')
            self.outPut.AppendText('加密用时:' + time + 's\n')
            with open(textlist['out'], 'a') as nf:
                nf.write(suffix)
        else:
            self.outPut.AppendText('解密成功...:' + '\n')
            self.outPut.AppendText('解密用时:' + time + 's\n')

            with open(textlist['in'], 'a') as nf:
                nf.write(suffix)


if __name__ == '__main__':
    app = wx.App(False)
    frame = MainWindow(None, "aesCryptor by aggie188")
    app.MainLoop()

