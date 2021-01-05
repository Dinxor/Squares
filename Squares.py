# -*- coding: cp1251 -*-
"""
Игра "Квадратики" © 2005 http://www.script-coding.info/
Правила игры:
В результате щелчка по любому квадратику "инвертируются" все квадратики двух линий, на пересечении
которых находится текущий квадратик. Следует добиться того, чтобы все квадратики на поле стали одного
цвета (безразлично какого), с наименьшим количеством ходов.
Подсказка: чтобы инвертировать конкретный квадратик, не затронув все остальные, следует "общёлкать"
две линии, на пересечении которых он находится. Однако, это далеко не самый рациональный способ игры
(по количеству ходов). В начале игры игроку выдаётся лимит ходов из расчёта такого "нерационального"
способа игры. Разница между выданным лимитом и фактическим количеством ходов и будет количеством
заработанных очков. Удачи!
P.S. Если нужно обнулить рекорды, удалите файл records.dat.
"""
# =================================================================================================================================================
def GetLimit():
    # Функция возвращает лимит количества ходов для пользователя, исходя из состояния поля в данный момент
    global Num
    return MinCount() * (Num * 2 - 1)
# =================================================================================================================================================
def MinCount():
    # Функция возвращает наименьшее количество кнопок одного цвета на поле в данный момент
    # (если менььше белых - возвращает количество белых, если меньше чёрных - возвращает количество чёрных)
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
    # Функция перерисовывает поле в соответствии с параметром, выбранным пользователем (поле 4х4 или 6х6)
    global Num, bGame, StatusBar
    bGame = 0
    ClearField()
    Num = N
    DrawField()
    StatusBar.config(text = "Нет игры")
# =================================================================================================================================================
def ClearField():
    # Функция очищает поле кнопок
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
    # Функция создаёт поле из кнопок (4х4 или 6х6)
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
    # Функция начинает новую игру.
    global bGame, StatusBar, iMoves, iLim
    Shuffle()
    bGame = 1
    iLim = GetLimit()
    StatusBar.config(text = "Ходов - 0 из " + str(iLim) + ", очки - " + str(iLim))
    iMoves = 0
# =================================================================================================================================================
def Shuffle():
    # Функция устанавливает цвет всех кнопок случайным образом.
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
    # Функция получает в качестве параметра кнопку и меняет (инвертирует) её цвет.
    if Btn.cget("bg") == "black" :
        Btn.config(bg = "white")
    else:
        Btn.config(bg = "black")
# =================================================================================================================================================
def Move(a, b):
    # Функция-обработчик щелчка по кнопке.
    global bGame, Btns, Num, iMoves, StatusBar
    # Если игра не запущена, ничего не делаем:
    if bGame == 0 :
        return
    # Собственно, ход:
    InversionColor(Btns[a][b])
    i = 0
    while i < Num :
        InversionColor(Btns[i][b])
        InversionColor(Btns[a][i])
        i += 1
    # Строка состояния:
    iMoves += 1
    StatusBar.config(text = "Ходов - " + str(iMoves) + " из " + str(iLim) + ", очки - " + str(iLim-iMoves))
    # Проверка, не пора ли закончить:
    if MinCount() == 0 :
        bGame = 0 # Если все кнопки стали одного цвета, завершим игру
        messagebox.showinfo("  Игра окончена!", "Количество очков - " + str(iLim-iMoves) +
        ". Использовано ходов - " + str(iMoves) + " из " + str(iLim) + ".")
        StatusBar.config(text = "Нет игры")
        RecordResult(iLim-iMoves)
    elif iMoves == iLim :
        bGame = 0 # Если лимит ходов исчерпан, завершим игру
        messagebox.showinfo("  Игра окончена!", "Вы проиграли! Лимит ходов исчерпан!")
        StatusBar.config(text = "Нет игры")
# =================================================================================================================================================
def RecordResult(Res):
    # Функция записывает результат игры, если это необходимо
    global Num, PlayerName
    Records = RecRead()
    Records44 = Records[0]
    Records66 = Records[1]
    if Num == 4 : # размерность поля 4х4
        RecList = Records44
    else: # размерность поля 6х6 (Num == 6)
        RecList = Records66
    # определим, надо ли записывать рекорд
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
    RecList.sort() # сортируем в порядке убывания
    RecList.reverse()
    if len(RecList) > 5 :
        RecList.pop() # обрезаем последний элемент
    RecWrite(Records44, Records66) # перезапись файла
    ShowRecords() # отображение результатов
# =================================================================================================================================================
def onKeyEntry_registered(val):
    # Обработчик события "key" поля ввода.
    # Ограничение длины вводимой строки - не более 20 символов.
    if len(val) > 20 :
        return 0
    else:
        return 1
# =================================================================================================================================================
def AskName():
    # Функция интерактивно запрашивает и устанавливает имя игрока
    global MainWnd
    AskWnd = Toplevel() # окно запроса
    AskWnd.transient(MainWnd) # делаем окно запроса "временным окном" (удаление кнопки "свернуть")
    AskWnd.maxsize(200,70)
    AskWnd.minsize(200,70)
    Legend = Label(AskWnd, text = "Ваше имя (не более 20 симв.):") # надпись
    Legend.pack(side = TOP, anchor = W)
    onKeyEntry = AskWnd.register(onKeyEntry_registered) # регистрация обработчика события
    Ent = Entry(AskWnd, width = 30, validate = "key", validatecommand = onKeyEntry + " %P") # поле ввода
    Ent.pack(side = TOP)
    Ent.focus() # передача фокуса в поле ввода
    Ent.bind("<Return>", (lambda event, e=Ent : SetPlayerName(e))) # нажатие Enter в поле ввода вызывает SetPlayerName()
    BtnOK = Button(AskWnd, text = "ОК", width = 12,
        command = (lambda e=Ent : SetPlayerName(e))) # кнопка "ОК", вызывает SetPlayerName()
    BtnOK.pack(side = LEFT, pady = (5,2), padx = 5)
    BtnCancel = Button(AskWnd, text = "Отмена", width = 12,
        command = AskWnd.destroy) # кнопка "Отмена"
    BtnCancel.pack(side = RIGHT, pady = (5,2), padx = 5)
    AskWnd.iconbitmap(sys.path[0] + "\\Squares.ico") # иконка окна
    AskWnd.title("  Запись результатов") # строка заголовка окна
    AskWnd.bind('<Escape>', lambda event : AskWnd.destroy()) # выход по нажатию "Esc"
    MainWndGeom = MainWnd.geometry() # вывод модального окна над основным
    pos = MainWndGeom.find("+")
    AskWnd.geometry("200x70"+MainWndGeom[pos:])
    AskWnd.focus_set() # перехват фокуса ввода (обеспечение модальности)
    AskWnd.grab_set() # отключение других окон (обеспечение модальности)
    AskWnd.wait_window() # ожидание удаления окна (обеспечение модальности)
# =================================================================================================================================================
def SetPlayerName(Ent):
    # Функция устанавливает имя игрока из поля ввода на форме в глобальную переменную  (привязана к кнопке на форме)
    global PlayerName
    PlayerName = Ent.get().strip().encode("CP1251") # Имя пользователя
    if len(PlayerName) == 0 :
        PlayerName = "Без имени".encode("CP1251")
    Ent.master.destroy() # закрытие окна-родителя
# =================================================================================================================================================
def RecWrite(Records44, Records66):
    # Функция получает в параметрах информацию о рекордах в виде двух списков (для игр 4х4 и 6х6 соответственно) и перезаписывает файл с рекордами
    FilePath = sys.path[0] + "\\records.dat" #путь к файлу с результатами
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
    # Функция считывает информацию о рекордах из файла и возвращает кортеж из двух списков (для игр 4х4 и 6х6 соответственно)
    Records44 = [] # список рекордов 4х4
    Records66 = [] # список рекордов 6х6
    FilePath = sys.path[0] + "\\records.dat" #путь к файлу с результатами
    try:
        file = open(FilePath, "r") # открытие файла на чтение
        i = 0 # номер строки
        for line in file.readlines(): # считывание содержимого файла построчно
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
        file.close() # закрытие файла
    except:
        pass
    return Records44, Records66
# =================================================================================================================================================
def ShowRecords():
    # Функция демонстрирует информацию о рекордах
    Records = RecRead()
    Records44 = Records[0]
    Records66 = Records[1]
    strOutput = ""
    if len(Records44) > 0 :
        strOutput += "Рекорды на поле 4х4:\n"
        for el in Records44 :
            strOutput += "    " + el[3:].strip() + " - " + el[:3].strip() + "\n"
    if len(Records66) > 0 :
        strOutput += "Рекорды на поле 6х6:\n"
        for el in Records66 :
            strOutput += "    " + el[3:].strip() + " - " + el[:3].strip() + "\n"
    strOutput = strOutput.strip()
    if len(strOutput) > 0 :
        messagebox.showinfo("  Рекорды", strOutput)
    else:
        messagebox.showinfo("  Рекорды", "Рекордов пока нет!")
# =================================================================================================================================================
def onKeyPressN(event):
    NewGame()
# =================================================================================================================================================
# Основная программа
# =================================================================================================================================================
import sys
import random
from tkinter import *
#from tkMessageBox import *
from tkinter import messagebox

Btns = [] # список кнопок на форме
Frms = [] # список фреймов на форме

MainWnd = Tk() # создание главного окна
MainWnd.title("  Квадратики")

Num = 4 # размерность поля (по умолчанию ставим 4х4)
DrawField()

# создание меню
MainMenu = Menu(MainWnd)
MainWnd.config(menu = MainMenu)
GeneralMenu = Menu(MainMenu, tearoff = 0)
GeneralMenu.add_command(label = "Новая игра (N)", command = NewGame)
GeneralMenu.add_command(label = "Рекорды...", command = ShowRecords)
GeneralMenu.add_command(label = "Выход (Alt+F4)", command = MainWnd.quit)
MainMenu.add_cascade(label = "Главная", menu = GeneralMenu)
OptionsMenu = Menu(MainMenu, tearoff = 0)
OptionsMenu.add_command(label = "Поле 4х4", command = (lambda a = 4 : RedrawField(a)))
OptionsMenu.add_command(label = "Поле 6х6", command = (lambda a = 6 : RedrawField(a)))
MainMenu.add_cascade(label = "Параметры", menu = OptionsMenu)

bGame = 0 # Флаг: 1 - игра запущена, 0 - нет.
iMoves = 0 # Счётчик ходов пользователя.
iLim = 0 # Лимит ходов для пользователя.
PlayerName = "" # Имя игрока

# строка состояния
StatusBar = Label(MainWnd, relief = SUNKEN, text = "Нет игры", anchor = W)
StatusBar.pack(side = BOTTOM, fill = X, pady = (2,0))

MainWnd.resizable(0, 0) # запрет изменения размеров главного окна
MainWnd.iconbitmap(sys.path[0] + "\\Squares.ico") # иконка главного окна

MainWnd.bind('<n>', onKeyPressN) # привязка функции onKeyPressN() к нажатию "N"
#MainWnd.bind('<т>', onKeyPressN) # привязка функции onKeyPressN() к нажатию "Т" ("N" в русской раскладке)

MainWnd.mainloop() # запуск главного окна