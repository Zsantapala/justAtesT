#-*-coding:utf-8-*-
#!/usr/bin/python
import tkinter as tk
import queue,threading

def main_walk():
    pass

if __name__=='__main__':
    windows=tk.Tk()
    windows.title('井字棋游戏')
    windows.geometry('300x300')
    # 禁止拉伸
    windows.resizable(width=False, height=False)
    #菜单栏
    menubar = tk.Menu(windows)
    filemenu1 = tk.Menu(menubar, tearoff=False)
    filemenu1.add_command(label='人机对战')
    filemenu1.add_separator()
    filemenu1.add_command(label='人人对战')
    menubar.add_cascade(label='模式', menu=filemenu1)
    filemenu2 = tk.Menu(menubar, tearoff=False)
    filemenu2.add_command(label='新游戏')
    filemenu2.add_separator()
    filemenu2.add_command(label='悔棋')
    menubar.add_cascade(label='游戏', menu=filemenu2)
    windows.config(menu=menubar)

    ini_image = tk.PhotoImage(file='timg.gif')
    #按钮部件
    pos1 = tk.StringVar()
    pos1.set('1')
    b1 = tk.Button(windows, image=ini_image, width=100, height=100, text='1')
    b1.place(x=0, y=0)
    b2 = tk.Button(windows, image=ini_image, width=100, height=100)
    b2.place(x=100, y=0)
    b3 = tk.Button(windows, image=ini_image, width=100, height=100)
    b3.place(x=200, y=0)
    b4 = tk.Button(windows, image=ini_image, width=100, height=100)
    b4.place(x=0, y=100)
    b5 = tk.Button(windows, image=ini_image, width=100, height=100)
    b5.place(x=100, y=100)
    b6 = tk.Button(windows, image=ini_image, width=100, height=100)
    b6.place(x=200, y=100)
    b7 = tk.Button(windows, image=ini_image, width=100, height=100)
    b7.place(x=0, y=200)
    b8 = tk.Button(windows, image=ini_image, width=100, height=100)
    b8.place(x=100, y=200)
    b9 = tk.Button(windows, image=ini_image, width=100, height=100)
    b9.place(x=200, y=200)
    windows.mainloop()