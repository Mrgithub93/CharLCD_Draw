import tkinter as tk
from tkinter import filedialog

class LCDCharacterDesigner:
    def __init__(self, master):
        self.master = master
        master.title("8x2 LCD Character Designer")
        # change cell_size change overall window size
        self.cell_size = 10
        self.grid_width = 5
        self.grid_height = 8
        self.num_chars = 8

        self.frames = []
        self.canvases = []
        self.grids = [[[0 for _ in range(self.grid_width)] for _ in range(self.grid_height)] for _ in range(self.num_chars)]

        #(HD44780-based LCDs can only store 8 characters at a time this is mostly for reference when drawing)
        #this modifies the global variable, i have a 8x2 LCD so its set to that atm,
        #if you have a 16x2 LCD change = i in range(2), j in range(16)
        for i in range(2):
            for j in range(4):
                frame = tk.Frame(master, bd=2, relief=tk.RAISED, padx=5, pady=5)
                frame.grid(row=i, column=j, padx=10, pady=10)

                canvas = tk.Canvas(frame, width=self.cell_size * self.grid_width,
                                   height=self.cell_size * self.grid_height, bg="white")
                canvas.pack()

                char_index = i * 4 + j
                canvas.bind("<Button-1>", lambda e, idx=char_index: self.left_click(e, idx))
                canvas.bind("<B1-Motion>", lambda e, idx=char_index: self.left_drag(e, idx))
                canvas.bind("<Button-3>", lambda e, idx=char_index: self.right_click(e, idx))
                canvas.bind("<B3-Motion>", lambda e, idx=char_index: self.right_drag(e, idx))

                label = tk.Label(frame, text=f"Char {char_index}")
                label.pack()

                clear_button = tk.Button(frame, text="Clear", command=lambda idx=char_index: self.clear_character(idx))
                clear_button.pack()

                self.frames.append(frame)
                self.canvases.append(canvas)

                self.draw_grid(canvas)

        save_button = tk.Button(master, text="Save All", command=self.save_characters)
        save_button.grid(row=2, column=0, columnspan=4, sticky='ew', padx=10, pady=10)

        clear_all_button = tk.Button(master, text="Clear All", command=self.clear_all)
        clear_all_button.grid(row=2, column=4, columnspan=4, sticky='ew', padx=10, pady=10)

    def draw_grid(self, canvas):
        for i in range(self.grid_width + 1):
            canvas.create_line(i * self.cell_size, 0, i * self.cell_size, self.grid_height * self.cell_size, fill="gray")
        for i in range(self.grid_height + 1):
            canvas.create_line(0, i * self.cell_size, self.grid_width * self.cell_size, i * self.cell_size, fill="gray")

    def left_click(self, event, char_index):
        self.set_cell(event, char_index, 1)

    def right_click(self, event, char_index):
        self.set_cell(event, char_index, 0)

    def left_drag(self, event, char_index):
        self.set_cell(event, char_index, 1)

    def right_drag(self, event, char_index):
        self.set_cell(event, char_index, 0)

    def set_cell(self, event, char_index, value):
        x, y = event.x // self.cell_size, event.y // self.cell_size
        if 0 <= x < self.grid_width and 0 <= y < self.grid_height:
            self.grids[char_index][y][x] = value
            self.redraw_canvas(char_index)

    def redraw_canvas(self, char_index):
        canvas = self.canvases[char_index]
        canvas.delete("all")
        self.draw_grid(canvas)
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                if self.grids[char_index][y][x]:
                    canvas.create_rectangle(x * self.cell_size + 1, y * self.cell_size + 1,
                                            (x + 1) * self.cell_size - 1, (y + 1) * self.cell_size - 1,
                                            fill="black", outline="")

    def save_characters(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w') as f:
                for char_index, grid in enumerate(self.grids):
                    f.write(f"Character {char_index} = [\n")
                    for row in grid:
                        binary_str = ''.join(map(str, row))
                        f.write(f"0b{binary_str},\n")
                    f.write("]\n\n")

    def clear_character(self, char_index):
        self.grids[char_index] = [[0 for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        self.redraw_canvas(char_index)

    def clear_all(self):
        for char_index in range(self.num_chars):
            self.clear_character(char_index)

if __name__ == "__main__":
    root = tk.Tk()
    app = LCDCharacterDesigner(root)
    root.mainloop()
