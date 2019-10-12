#-*-coding:utf-8-*-
#!/usr/bin/python
import tkinter as tk
from PIL import Image, ImageTk
import random

class My_tk(tk.Tk):
    def __init__(self, checkboard=3, count=3, width=100):
        super().__init__()
        _image = Image.open('0.gif')
        _p1_image = Image.open('1.gif')
        _p2_image = Image.open('2.gif')
        self._line = checkboard
        self.count = count                                                        #连子数，用来设置是三步棋还是五子棋
        self._checkerboard = [[0]*self._line for line in range(self._line)]       #二维列表棋盘，tk.button棋盘映射的实际棋盘
        self.offset = [(1, 0), (0, 1), (1, 1), (1, -1)]                           #二维向量，用来表示二维数组不同方向向量
        self.width = width
        self.geometry(str(self._line * width)+'x'+str(self._line * width))
        self.resizable(width=False, height=False)
        #棋子图片大小根据Button长宽自行更变
        self.image = ImageTk.PhotoImage(_image.resize((width, width), Image.ANTIALIAS))
        self.player1 = ('O', 1, ImageTk.PhotoImage(_p1_image.resize((width, width), Image.ANTIALIAS)))
        self.player2 = ('X', 2, ImageTk.PhotoImage(_p2_image.resize((width, width), Image.ANTIALIAS)))
        self.current_player = self.player1
        self.win = False
        self.now_pos = []                                                #判断现在走棋坐标状态，以用来悔棋
        self.menubars()                                                  #初始化菜单栏
        self.Widgets(checkboard)                                         #初始化棋盘

    #菜单功能
    def menubars(self):
        self.menubar = tk.Menu(self)
        self.fileMenu1 = tk.Menu(self.menubar, tearoff=False)
        self.fileMenu1.add_command(label='人机对战', command=lambda arg=True: self.action_com(arg))
        self.fileMenu1.add_separator()
        self.fileMenu1.add_command(label='人人对战', command=self.action_com)
        self.menubar.add_cascade(label='模式', menu=self.fileMenu1)
        self.fileMenu2 = tk.Menu(self.menubar, tearoff=False)
        self.fileMenu2.add_command(label='新游戏', command=self.new_game)
        self.fileMenu2.add_separator()
        self.fileMenu2.add_command(label='悔棋', command=self.step_up)
        self.menubar.add_cascade(label='游戏', menu=self.fileMenu2)
        self.fileMenu3 = tk.Menu(self.menubar, tearoff=False)
        self.fileMenu3.add_command(label='井字棋3X3', command=self.g_mode)
        self.fileMenu3.add_separator()
        self.fileMenu3.add_command(label='五子棋5x5', command=lambda x=5, y=5: self.g_mode(x, y))
        self.fileMenu3.add_command(label='五子棋15x15', command=lambda x=15, y=5, z=50: self.g_mode(x, y, z))
        self.menubar.add_cascade(label='游戏模式', menu=self.fileMenu3)
        self.config(menu=self.menubar)

    #走棋主函数，tk.Button command联动此函数
    def main_walk(self, pos):
        x = pos[0]
        y = pos[1]
        if self.current_player[1] == 1:
            if self._checkerboard[x][y] == 0:
                self._checkerboard[x][y] = self.player1[1]
                print(self._checkerboard)
                self.btns[str(x)+'_'+str(y)].config(image=self.player1[2])
                self.win = self.is_Win(x, y)
                self.now_pos = [pos[0], pos[1]]
                self.current_player = self.player2
        elif self.current_player[1] == 2:
            if self._checkerboard[x][y] == 0:
                self._checkerboard[x][y] = self.player2[1]
                print(self._checkerboard)
                self.btns[str(x)+'_'+str(y)].config(image=self.player2[2])
                self.win = self.is_Win(x, y)
                self.now_pos = [pos[0], pos[1]]
                self.current_player = self.player1


    def state_info(self, name):
        self.info = tk.Toplevel(self)
        self.info.geometry("300x100+580+250")
        state = tk.StringVar()
        state.set(name)
        lab_info = tk.Label(self.info, textvariable=state, width=10, height=2)
        lab_info.place(x=100, y=10)
        btn_new_game = tk.Button(self.info, text='新游戏', width=10, height=2, command=self.new_g_stat_info)
        btn_new_game.place(x=50, y=40)
        btn_quit = tk.Button(self.info, text='退出', width=10, height=2, command=self.destroy)
        btn_quit.place(x=150, y=40)

    def new_g_stat_info(self):
        self.new_game()
        self.info.destroy()

    def warning_info(self, value):
        self.w_info = tk.Toplevel(self)
        self.w_info.geometry("300x100")
        wraning = tk.StringVar()
        wraning.set(value)
        w_lable = tk.Label(self.w_info, textvariable=wraning, width=20, height=2)
        w_lable.place(x=100, y=30)

    #判断输赢函数
    def is_Win(self, x, y):
        full = 0
        for line in self._checkerboard:
            if 0 not in line:
                full += 1
        if full < self._line and self.player_win(x, y):
            info = self.current_player[0]+' is Win!!'
            self.state_info(info)
            return True
        elif full == self._line and not self.player_win(x, y):
            info = 'Draw!!'
            self.state_info(info)
            return True

    #以下棋点四个方向判断是否连子
    def player_win(self, x, y):
        for pos in self.offset:
            if self.one_direction(x, y, pos):
                return True
        return False

    #判断单方向是否连子
    def one_direction(self, x, y, offset):
        count = 1
        for direction in range(1, self._line):
            x_pos = x + direction*offset[0]
            y_pos = y + direction*offset[1]
            if 0 <= x_pos <= self._line-1 and 0 <= y_pos <= self._line-1 and self._checkerboard[x_pos][y_pos] == self.current_player[1]:
                count += 1
            else:
                break
        for direction in range(1, self._line):
            x_pos = x - direction*offset[0]
            y_pos = y - direction*offset[1]
            if 0 <= x_pos <= self._line-1 and 0 <= y_pos <= self._line-1 and self._checkerboard[x_pos][y_pos] == self.current_player[1]:
                count += 1
            else:
                break
        return count >= self.count

    #初始化TK棋盘
    def Widgets(self, chk):
        self.btns = {}
        for x in range(chk):
            for y in range(chk):
                pos = (x, y)
                self.btns[str(x)+'_'+str(y)] = tk.Button(self, width=self.width, height=self.width, image=self.image, command=lambda s=pos: self.main_walk(s))
                self.btns[str(x)+'_'+str(y)].place(x=y*self.width, y=x*self.width)

    #创建新游戏保留棋盘规格 绑定菜单栏新游戏
    def new_game(self):
        self._checkerboard = [[0] * self._line for line in range(self._line)]
        self.Widgets(self._line)
        self.current_player = self.player1
    #游戏模式功能，绑定菜单栏棋盘格数与连子数
    def g_mode(self, line=3, key1=3, key2=100):
        self.destroy()
        self.__init__(line, key1, key2)
    #悔棋
    def step_up(self):
        if self.now_pos and self._checkerboard[self.now_pos[0]][self.now_pos[1]] != 0:
            if self.current_player[1] == 1:
                self._checkerboard[self.now_pos[0]][self.now_pos[1]] = 0
                self.btns[str(self.now_pos[0]) + '_' + str(self.now_pos[1])].config(image=self.image)
                self.current_player = self.player2
            else:
                self._checkerboard[self.now_pos[0]][self.now_pos[1]] = 0
                self.btns[str(self.now_pos[0]) + '_' + str(self.now_pos[1])].config(image=self.image)
                self.current_player = self.player1
        elif self.now_pos and self._checkerboard[self.now_pos[0]][self.now_pos[1]] == 0:
            self.warning_info('你已经悔了棋')
        else:
            self.warning_info('你还没开始呢')
    #激活人机对战（开发未完成）
    def action_com(self,status=False):
        if status:
            for x in range(self._line):
                for y in range(self._line):
                    self.btns[str(x)+'_'+str(y)].config(command=lambda s=(x, y): self.com_start(s))
        else:
            for x in range(self._line):
                for y in range(self._line):
                    self.btns[str(x)+'_'+str(y)].config(command=lambda s=(x, y): self.main_walk(s))
    #人机对战走棋函数
    def com_start(self, pos):
        self.main_walk(pos)
        self.main_walk(self.stupid_com_method())
    '''
    def stupid_com_method(self):
        x = random.randint(0, self._line)
        y = random.randint(0, self._line)
        print(x, y)
        for s in range(len(self._checkerboard)):
            if self._checkerboard[x][y] == 0:
                return x, y
            else:
                continue
    '''
if __name__ == '__main__':
    gg = My_tk()
    gg.mainloop()