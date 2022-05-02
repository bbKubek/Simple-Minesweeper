from tkinter import Button, Label
import random, ctypes, sys
import settings

class Cell:
    all = []
    cell_count = settings.CELL_COUNT
    cell_count_label_obj = None
    def __init__(self, x, y, is_mine=False):
        self.is_mine = is_mine
        self.is_clicked = False
        self.is_flagged = False
        self.cell_btn_object = None
        self.x = x
        self.y = y

        # Append to Cell.all list
        Cell.all.append(self)
        
    def create_btn_object(self, location):
        btn = Button(
            location,
            width = 14,
            height = 4
        )
        btn.bind('<Button-1>', self.left_click_actions)
        btn.bind('<Button-3>', self.right_click_actions)
        self.cell_btn_object = btn

    @staticmethod
    def create_cell_count_label(location):
        label = Label(
            location,
            bg="black",
            fg="white",
            text=f"Cells left: {Cell.cell_count}",
            font=("", 30)
        )
        Cell.cell_count_label_obj = label

    def get_cell_by_axis(self, x, y):
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell

    @property
    def neighbour_cells(self):
        cells = [
            self.get_cell_by_axis(self.x-1, self.y-1),
            self.get_cell_by_axis(self.x-1, self.y),
            self.get_cell_by_axis(self.x-1, self.y+1),
            self.get_cell_by_axis(self.x, self.y-1),
            self.get_cell_by_axis(self.x+1, self.y-1),
            self.get_cell_by_axis(self.x+1, self.y),
            self.get_cell_by_axis(self.x+1, self.y+1),
            self.get_cell_by_axis(self.x, self.y+1),
        ]
        cells = [cell for cell in cells if cell is not None]
        return cells

    @property
    def neighbour_cells_mine_counter(self):
        counter = 0
        for cell in self.neighbour_cells:
            if cell.is_mine:
                counter += 1
        return counter

    def show_cell(self):
        if not self.is_clicked:
            Cell.cell_count -= 1
            self.cell_btn_object.configure(text=self.neighbour_cells_mine_counter)
            if Cell.cell_count_label_obj:
                Cell.cell_count_label_obj.configure(text=f"Cells left: {Cell.cell_count}")


        self.is_clicked = True

    def show_mine(self):
        self.cell_btn_object.configure(bg='Red')
        ctypes.windll.user32.MessageBoxW(0, "You lost", "Game Over", 0)
        sys.exit()

    def left_click_actions(self, event):
        if self.is_mine:
            self.show_mine()
        else:
            if self.neighbour_cells_mine_counter == 0:
                for cell_obj in self.neighbour_cells:
                    cell_obj.show_cell()
            self.show_cell()
            if Cell.cell_count == settings.MINES_COUNT:
                ctypes.windll.user32.MessageBoxW(0, "You won", "Congratulations", 0)

        self.cell_btn_object.unbind('<Button-1>')
        self.cell_btn_object.unbind('<Button-3>')

    def right_click_actions(self, event):
        if not self.is_flagged:
            self.cell_btn_object.configure(text='🚩')
            self.is_flagged = True
        else:
            self.cell_btn_object.configure(text='')
            self.is_flagged = False


    @staticmethod
    def randomize_mines():
        mines = random.sample(Cell.all, settings.MINES_COUNT)
        for mine in mines:
            mine.is_mine = True

    def __repr__(self):
        return f"Cell({self.x}, {self.y})"