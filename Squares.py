# -*- coding: cp1251 -*-
"""
���� "����������" � 2005 http://www.script-coding.info/
������� ����:
� ���������� ������ �� ������ ���������� "�������������" ��� ���������� ���� �����, �� �����������
������� ��������� ������� ���������. ������� �������� ����, ����� ��� ���������� �� ���� ����� ������
����� (����������� ������), � ���������� ����������� �����.
���������: ����� ������������� ���������� ���������, �� �������� ��� ���������, ������� "���������"
��� �����, �� ����������� ������� �� ���������. ������, ��� ������ �� ����� ������������ ������ ����
(�� ���������� �����). � ������ ���� ������ ������� ����� ����� �� ������� ������ "���������������"
������� ����. ������� ����� �������� ������� � ����������� ����������� ����� � ����� �����������
������������ �����. �����!
P.S. ���� ����� �������� �������, ������� ���� records.dat.
"""
# =================================================================================================================================================
def GetLimit():
    # ������� ���������� ����� ���������� ����� ��� ������������, ������ �� ��������� ���� � ������ ������
    global Num
    return MinCount() * (Num * 2 - 1)
# =================================================================================================================================================
def MinCount():
    # ������� ���������� ���������� ���������� ������ ������ ����� �� ���� � ������ ������
    # (���� ������� ����� - ���������� ���������� �����, ���� ������ ������ - ���������� ���������� ������)
    global Btns, Num
    iWhite = 0; iBlack = 0
    i = 0
    while i < Num :
        j = 0
        while j < Num :
            if Btns[i][j].cget("bg") == "black" :
                iBlack += 1
            else:
                iWhite += 1
            j += 1
        i += 1
    if iBlack < iWhite :
        return iBlack
    else:
        return iWhite
# =================================================================================================================================================
def RedrawField(N):
    # ������� �������������� ���� � ������������ � ����������, ��������� ������������� (���� 4�4 ��� 6�6)
    global Num, bGame, StatusBar
    bGame = 0
    ClearField()
    Num = N
    DrawField()
    StatusBar.config(text = "��� ����")
# =================================================================================================================================================
def ClearField():
    # ������� ������� ���� ������
    global Btns, Frms, Num
    i = 0
    while i < Num :
        j = 0
        while j < Num :
            Btns[i][j].destroy()
            j += 1
        Frms[i].destroy()
        i += 1
# =================================================================================================================================================
def DrawField():
    # ������� ������ ���� �� ������ (4�4 ��� 6�6)
    global MainWnd, Btns, Frms, Num
    Btns = []
    Frms = []
    i = 0
    while i < Num :
        Frm = Frame(MainWnd)
        Frm.pack(side = TOP, anchor = W)
        BtnsIn = []
        Btns += [BtnsIn]
        Frms += [Frm]
        j = 0
        while j < Num :
            Btn = Button(Frm, command = (lambda a=i, b=j : Move(a, b)), width = 10, height = 5, bg = "black")
            Btn.pack(side = LEFT)
            Btns[i] += [Btn]
            j += 1
        i += 1
# =================================================================================================================================================
def NewGame():
    # ������� �������� ����� ����.
    global bGame, StatusBar, iMoves, iLim
    Shuffle()
    bGame = 1
    iLim = GetLimit()
    StatusBar.config(text = "����� - 0 �� " + str(iLim) + ", ���� - " + str(iLim))
    iMoves = 0
# =================================================================================================================================================
def Shuffle():
    # ������� ������������� ���� ���� ������ ��������� �������.
    global Num
    i = 0
    while i < Num :
        j = 0
        while j < Num :
            if random.random() > 0.5 :
                Btns[i][j].config(bg = "black")
            else:
                Btns[i][j].config(bg = "white")
            j += 1
        i += 1
# =================================================================================================================================================
def InversionColor(Btn):
    # ������� �������� � �������� ��������� ������ � ������ (�����������) � ����.
    if Btn.cget("bg") == "black" :
        Btn.config(bg = "white")
    else:
        Btn.config(bg = "black")
# =================================================================================================================================================
def Move(a, b):
    # �������-���������� ������ �� ������.
    global bGame, Btns, Num, iMoves, StatusBar
    # ���� ���� �� ��������, ������ �� ������:
    if bGame == 0 :
        return
    # ����������, ���:
    InversionColor(Btns[a][b])
    i = 0
    while i < Num :
        InversionColor(Btns[i][b])
        InversionColor(Btns[a][i])
        i += 1
    # ������ ���������:
    iMoves += 1
    StatusBar.config(text = "����� - " + str(iMoves) + " �� " + str(iLim) + ", ���� - " + str(iLim-iMoves))
    # ��������, �� ���� �� ���������:
    if MinCount() == 0 :
        bGame = 0 # ���� ��� ������ ����� ������ �����, �������� ����
        messagebox.showinfo("  ���� ��������!", "���������� ����� - " + str(iLim-iMoves) +
        ". ������������ ����� - " + str(iMoves) + " �� " + str(iLim) + ".")
        StatusBar.config(text = "��� ����")
        RecordResult(iLim-iMoves)
    elif iMoves == iLim :
        bGame = 0 # ���� ����� ����� ��������, �������� ����
        messagebox.showinfo("  ���� ��������!", "�� ���������! ����� ����� ��������!")
        StatusBar.config(text = "��� ����")
# =================================================================================================================================================
def RecordResult(Res):
    # ������� ���������� ��������� ����, ���� ��� ����������
    global Num, PlayerName
    Records = RecRead()
    Records44 = Records[0]
    Records66 = Records[1]
    if Num == 4 : # ����������� ���� 4�4
        RecList = Records44
    else: # ����������� ���� 6�6 (Num == 6)
        RecList = Records66
    # ���������, ���� �� ���������� ������
    Yes = 0
    for el in RecList :
        if int(el[:3].strip()) < Res :
            Yes = 1
            break
    if len(RecList) < 5 :
        Yes = 1
    if Yes == 0 :
        ShowRecords()
        return
    PlayerName = ""
    AskName()
    if len(PlayerName) == 0 :
        return
    RecList.append(str(Res).rjust(3) + PlayerName)
    RecList.sort() # ��������� � ������� ��������
    RecList.reverse()
    if len(RecList) > 5 :
        RecList.pop() # �������� ��������� �������
    RecWrite(Records44, Records66) # ���������� �����
    ShowRecords() # ����������� �����������
# =================================================================================================================================================
def onKeyEntry_registered(val):
    # ���������� ������� "key" ���� �����.
    # ����������� ����� �������� ������ - �� ����� 20 ��������.
    if len(val) > 20 :
        return 0
    else:
        return 1
# =================================================================================================================================================
def AskName():
    # ������� ������������ ����������� � ������������� ��� ������
    global MainWnd
    AskWnd = Toplevel() # ���� �������
    AskWnd.transient(MainWnd) # ������ ���� ������� "��������� �����" (�������� ������ "��������")
    AskWnd.maxsize(200,70)
    AskWnd.minsize(200,70)
    Legend = Label(AskWnd, text = "���� ��� (�� ����� 20 ����.):") # �������
    Legend.pack(side = TOP, anchor = W)
    onKeyEntry = AskWnd.register(onKeyEntry_registered) # ����������� ����������� �������
    Ent = Entry(AskWnd, width = 30, validate = "key", validatecommand = onKeyEntry + " %P") # ���� �����
    Ent.pack(side = TOP)
    Ent.focus() # �������� ������ � ���� �����
    Ent.bind("<Return>", (lambda event, e=Ent : SetPlayerName(e))) # ������� Enter � ���� ����� �������� SetPlayerName()
    BtnOK = Button(AskWnd, text = "��", width = 12,
        command = (lambda e=Ent : SetPlayerName(e))) # ������ "��", �������� SetPlayerName()
    BtnOK.pack(side = LEFT, pady = (5,2), padx = 5)
    BtnCancel = Button(AskWnd, text = "������", width = 12,
        command = AskWnd.destroy) # ������ "������"
    BtnCancel.pack(side = RIGHT, pady = (5,2), padx = 5)
    AskWnd.iconbitmap(sys.path[0] + "\\Squares.ico") # ������ ����
    AskWnd.title("  ������ �����������") # ������ ��������� ����
    AskWnd.bind('<Escape>', lambda event : AskWnd.destroy()) # ����� �� ������� "Esc"
    MainWndGeom = MainWnd.geometry() # ����� ���������� ���� ��� ��������
    pos = MainWndGeom.find("+")
    AskWnd.geometry("200x70"+MainWndGeom[pos:])
    AskWnd.focus_set() # �������� ������ ����� (����������� �����������)
    AskWnd.grab_set() # ���������� ������ ���� (����������� �����������)
    AskWnd.wait_window() # �������� �������� ���� (����������� �����������)
# =================================================================================================================================================
def SetPlayerName(Ent):
    # ������� ������������� ��� ������ �� ���� ����� �� ����� � ���������� ����������  (��������� � ������ �� �����)
    global PlayerName
    PlayerName = Ent.get().strip().encode("CP1251") # ��� ������������
    if len(PlayerName) == 0 :
        PlayerName = "��� �����".encode("CP1251")
    Ent.master.destroy() # �������� ����-��������
# =================================================================================================================================================
def RecWrite(Records44, Records66):
    # ������� �������� � ���������� ���������� � �������� � ���� ���� ������� (��� ��� 4�4 � 6�6 ��������������) � �������������� ���� � ���������
    FilePath = sys.path[0] + "\\records.dat" #���� � ����� � ������������
    file = open(FilePath, "w")
    i = 0
    if len(Records44) > 0 :
        for el in Records44 :
            file.write(el + "\n")
            i += 1
    while i < 5 :
        file.write("\n")
        i += 1
    if len(Records66) > 0 :
        for el in Records66 :
            file.write(el + "\n")
            i += 1
    while i < 10 :
        file.write("\n")
        i += 1
    file.close()
# =================================================================================================================================================
def RecRead():
    # ������� ��������� ���������� � �������� �� ����� � ���������� ������ �� ���� ������� (��� ��� 4�4 � 6�6 ��������������)
    Records44 = [] # ������ �������� 4�4
    Records66 = [] # ������ �������� 6�6
    FilePath = sys.path[0] + "\\records.dat" #���� � ����� � ������������
    try:
        file = open(FilePath, "r") # �������� ����� �� ������
        i = 0 # ����� ������
        for line in file.readlines(): # ���������� ����������� ����� ���������
            i += 1
            line = line.rstrip()
            if len(line) == 0 :
                continue
            if i <= 5 :
                Records44.append(line)
            elif i <= 10 :
                Records66.append(line)
            else :
                break
        file.close() # �������� �����
    except:
        pass
    return Records44, Records66
# =================================================================================================================================================
def ShowRecords():
    # ������� ������������� ���������� � ��������
    Records = RecRead()
    Records44 = Records[0]
    Records66 = Records[1]
    strOutput = ""
    if len(Records44) > 0 :
        strOutput += "������� �� ���� 4�4:\n"
        for el in Records44 :
            strOutput += "    " + el[3:].strip() + " - " + el[:3].strip() + "\n"
    if len(Records66) > 0 :
        strOutput += "������� �� ���� 6�6:\n"
        for el in Records66 :
            strOutput += "    " + el[3:].strip() + " - " + el[:3].strip() + "\n"
    strOutput = strOutput.strip()
    if len(strOutput) > 0 :
        messagebox.showinfo("  �������", strOutput)
    else:
        messagebox.showinfo("  �������", "�������� ���� ���!")
# =================================================================================================================================================
def onKeyPressN(event):
    NewGame()
# =================================================================================================================================================
# �������� ���������
# =================================================================================================================================================
import sys
import random
from tkinter import *
#from tkMessageBox import *
from tkinter import messagebox

Btns = [] # ������ ������ �� �����
Frms = [] # ������ ������� �� �����

MainWnd = Tk() # �������� �������� ����
MainWnd.title("  ����������")

Num = 4 # ����������� ���� (�� ��������� ������ 4�4)
DrawField()

# �������� ����
MainMenu = Menu(MainWnd)
MainWnd.config(menu = MainMenu)
GeneralMenu = Menu(MainMenu, tearoff = 0)
GeneralMenu.add_command(label = "����� ���� (N)", command = NewGame)
GeneralMenu.add_command(label = "�������...", command = ShowRecords)
GeneralMenu.add_command(label = "����� (Alt+F4)", command = MainWnd.quit)
MainMenu.add_cascade(label = "�������", menu = GeneralMenu)
OptionsMenu = Menu(MainMenu, tearoff = 0)
OptionsMenu.add_command(label = "���� 4�4", command = (lambda a = 4 : RedrawField(a)))
OptionsMenu.add_command(label = "���� 6�6", command = (lambda a = 6 : RedrawField(a)))
MainMenu.add_cascade(label = "���������", menu = OptionsMenu)

bGame = 0 # ����: 1 - ���� ��������, 0 - ���.
iMoves = 0 # ������� ����� ������������.
iLim = 0 # ����� ����� ��� ������������.
PlayerName = "" # ��� ������

# ������ ���������
StatusBar = Label(MainWnd, relief = SUNKEN, text = "��� ����", anchor = W)
StatusBar.pack(side = BOTTOM, fill = X, pady = (2,0))

MainWnd.resizable(0, 0) # ������ ��������� �������� �������� ����
MainWnd.iconbitmap(sys.path[0] + "\\Squares.ico") # ������ �������� ����

MainWnd.bind('<n>', onKeyPressN) # �������� ������� onKeyPressN() � ������� "N"
#MainWnd.bind('<�>', onKeyPressN) # �������� ������� onKeyPressN() � ������� "�" ("N" � ������� ���������)

MainWnd.mainloop() # ������ �������� ����