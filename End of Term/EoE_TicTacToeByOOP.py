#-*-coding:utf-8-*-
#!/usr/bin/python
import tkinter as tk
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
        self.menubars()
        self.Widgets(checkboard)
        self.player1 = ('O', 1, tk.PhotoImage(file='1.gif'))
        self.player2 = ('X', 2, tk.PhotoImage(file='2.gif'))
        self.current_player = self.player1

    def menubars(self):
        self.menubar = tk.Menu(self)
        self.fileMenu1 = tk.Menu(self.menubar, tearoff=False)
        self.fileMenu1.add_command(label='人机对战')
        self.fileMenu1.add_separator()
        self.fileMenu1.add_command(label='人人对战')
        self.menubar.add_cascade(label='模式', menu=self.fileMenu1)
        self.fileMenu2 = tk.Menu(self.menubar, tearoff=False)
        self.fileMenu2.add_command(label='新游戏')
        self.fileMenu2.add_separator()
        self.fileMenu2.add_command(label='悔棋')
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
                self.is_Win(x, y)
                self.current_player = self.player2
        elif self.current_player[1] == 2:
            if self._checkerboard[x][y] == 0:
                self._checkerboard[x][y] = self.player2[1]
                self.btns[str(x)+'_'+str(y)].config(image=self.player2[2])
                self.is_Win(x, y)
                self.current_player = self.player1



    def state_info(self, name):
        self.info = tk.Toplevel(self)
        self.info.geometry("300x100+580+250")
        state = tk.StringVar()
        state.set(name)
        btn = tk.Button(self.info, textvariable=state, width=10, height=2, command=self.destroy)
        btn.place(x=100, y=30)

    def is_Win(self, x, y):
        full = 0
        for line in self._checkerboard:
            if 0 not in line:
                full += 1
        if full < self._line and self.player_win(x, y):
            info = self.current_player[0]+' is Win!!'
            self.state_info(info)
        elif full == self._line and not self.player_win(x,y):
            info = 'Draw!!'
            self.state_info(info)

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
                self.btns[str(x)+'_'+str(y)] = tk.Button(self, width=100, height=100, command=lambda s=pos: self.main_walk(s))
                self.btns[str(x)+'_'+str(y)].place(x=y*width, y=x*width)

if __name__ == '__main__':
    new_Game = My_tk(5, 3)
    new_Game.mainloop()
