#-*-coding:utf-8-*-
#!/usr/bin/python
import tkinter as tk
#import queue,threading

checkrboard = [[0]*3 for point in range(3)]
offset = [(1, 0), (0, 1), (1, 1), (1, -1)]
print(checkrboard)
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

    ini_image1 = tk.PhotoImage(file='1.gif')
    ini_image2 = tk.PhotoImage(file='2.gif')
    player1 = ('O', 1, ini_image1)
    player2 = ('X', 2, ini_image2)
    current_player=player1[1]
    def main_walk(pos,button):
        global checkrboard, player1, player2, current_player
        x = pos[0]
        y = pos[1]
        if current_player == 1:
            if checkrboard[x][y] == 0:
                checkrboard[x][y] = player1[1]
                button.config(image=player1[2])
                current_player = 2
                is_Win(x, y, player1[1], player1[0])
        elif current_player == 2:
            if checkrboard[x][y] == 0:
                checkrboard[x][y] = player2[1]
                button.config(image=player2[2])
                current_player = 1
                is_Win(x, y, player2[1], player2[0])

    def is_Win(x, y, cur_value, cur_name):
        global checkrboard
        full = 0
        for line in checkrboard:
            if 0 not in line:
                full += 1
        if full < 3 and player_win(x, y, cur_value):
            info = cur_name+'is WIN!!'
            state_info(info)
        elif full == 3 and not player_win(x, y, cur_value):
            info = 'Draw!!'
            state_info(info)

    def player_win(x,y,cur_value):
        global offset
        for pos in offset:
            if one_direction(x, y, pos[0], pos[1], cur_value):
                return True
        return False

    def one_direction(x, y, offset1, offset2, cur_value):
        global checkrboard
        count = 1
        for direction in range(1, 3):
            x_pos = x + direction*offset1
            y_pos = y + direction*offset2
            if 0 <= x_pos <= 2 and 0 <= y_pos <= 2 and checkrboard[x_pos][y_pos] == cur_value:
                count += 1
            else:
                break
        for direction in range(1, 3):
            x_pos = x - direction*offset1
            y_pos = y - direction*offset2
            if 0 <= x_pos <= 2 and 0 <= y_pos <= 2 and checkrboard[x_pos][y_pos] == cur_value:
                count += 1
            else:
                break
        return count >= 3


    def close_all_window():
        windows.destroy()

    def state_info(name):
        info = tk.Toplevel(windows)
        info.geometry("300x100+580+250")
        state = tk.StringVar()
        state.set(name)
        btn = tk.Button(info, textvariable=state, width=10, height=2, command=close_all_window)
        btn.place(x=100, y=30)

    def ini_img(button):
        button.config(background=None)

    #按钮部件
    b1 = tk.Button(windows, width=100, height=100, image=player1[2], command=lambda: ini_img(b1))
    b1.place(x=0, y=0)
    b2 = tk.Button(windows, width=100, height=100, command=lambda: main_walk((0, 1), b2))
    b2.place(x=100, y=0)
    b3 = tk.Button(windows, width=100, height=100, command=lambda: main_walk((0, 2), b3))
    b3.place(x=200, y=0)
    b4 = tk.Button(windows, width=100, height=100, command=lambda: main_walk((1, 0), b4))
    b4.place(x=0, y=100)
    b5 = tk.Button(windows, width=100, height=100, command=lambda: main_walk((1, 1), b5))
    b5.place(x=100, y=100)
    b6 = tk.Button(windows, width=100, height=100, command=lambda: main_walk((1, 2), b6))
    b6.place(x=200, y=100)
    b7 = tk.Button(windows, width=100, height=100, command=lambda: main_walk((2, 0), b7))
    b7.place(x=0, y=200)
    b8 = tk.Button(windows, width=100, height=100, command=lambda: main_walk((2, 1), b8))
    b8.place(x=100, y=200)
    b9 = tk.Button(windows, width=100, height=100, command=lambda: main_walk((2, 2), b9))
    b9.place(x=200, y=200)
    windows.mainloop()