#-*-coding:utf-8-*-
#!/usr/bin/python
import tkinter as tk
import threading, random

class My_tk(tk.Tk):
    def __init__(self, checkboard=3, count=3):
        super().__init__()
        self._line = checkboard
        self.count = count
        self._checkerboard = [[0]*self._line for line in range(self._line)]
        self.offset = [(1, 0), (0, 1), (1, 1), (1, -1)]
        height = str(checkboard*100)
        self.geometry(height+'x'+height)
        self.resizable(width=False, height=False)
        self.image = tk.PhotoImage(file='0.gif')
        self.player1 = ('O', 1, tk.PhotoImage(file='1.gif'))
        self.player2 = ('X', 2, tk.PhotoImage(file='2.gif'))
        self.current_player = self.player1
        self.win = False
        self.now_pos = []
        self.menubars()
        self.Widgets(self._line)


    def menubars(self):
        self.menubar = tk.Menu(self)
        self.fileMenu1 = tk.Menu(self.menubar, tearoff=False)
        self.fileMenu1.add_command(label='人机对战', command=lambda an=True: self.stupid_com(an))
        self.fileMenu1.add_separator()
        self.fileMenu1.add_command(label='人人对战', command=lambda an=False: self.stupid_com(an))
        self.menubar.add_cascade(label='模式', menu=self.fileMenu1)
        self.fileMenu2 = tk.Menu(self.menubar, tearoff=False)
        self.fileMenu2.add_command(label='新游戏', command=self.new_game)
        self.fileMenu2.add_separator()
        self.fileMenu2.add_command(label='悔棋', command=self.step_up)
        self.menubar.add_cascade(label='游戏', menu=self.fileMenu2)
        self.config(menu=self.menubar)

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
        btn = tk.Button(self.info, textvariable=state, width=10, height=2, command=self.destroy)
        btn.place(x=100, y=30)

    def warning_info(self, value):
        self.w_info = tk.Toplevel(self)
        self.w_info.geometry("300x100")
        wraning = tk.StringVar()
        wraning.set(value)
        w_lable = tk.Label(self.w_info, textvariable=wraning, width=20, height=2)
        w_lable.place(x=100, y=30)

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

    def player_win(self, x, y):
        for pos in self.offset:
            if self.one_direction(x, y, pos):
                return True
        return False

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

    def Widgets(self, chk, width=100):
        self.btns = {}
        for x in range(chk):
            for y in range(chk):
                pos = (x, y)
                self.btns[str(x)+'_'+str(y)] = tk.Button(self, width=100, height=100, image=self.image, command=lambda s=pos: self.main_walk(s))
                self.btns[str(x)+'_'+str(y)].place(x=y*width, y=x*width)

    def new_game(self):
        self._checkerboard = [[0] * self._line for line in range(self._line)]
        self.Widgets(self._line)
        self.current_player = self.player1

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

    def stupid_com(self, status):
        if status == True:
            lock = threading.Lock()
            while True:
                if self.current_player == self.player1 and not self.win:
                    lock.acquire()
                elif self.current_player == self.player2 and not self.win:
                    lock.release()
                    self.main_walk(self.stupid_com_method())
                else:
                    break


    def stupid_com_method(self):
        x = random.randint(0, self._line)
        y = random.randint(0, self._line)
        for s in range(len(self._checkerboard)):
            if self._checkerboard[x][y] == 0:
                return x, y
            else:
                continue

if __name__ == '__main__':
    gg = My_tk()
    gg.mainloop()