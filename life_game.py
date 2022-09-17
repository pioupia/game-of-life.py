from math import floor
from tkinter import Tk, Canvas


class GameOfLife:
    def __init__(self):
        # Initialisation des variables dans la class.
        self.playing = False
        self.size = 10
        self.height = self.width = 600

        self.colors = {
            "cell": "#16d8ed",
            "bg": "#191919"
        }

        self.cells = []

        for i in range(0, self.height, self.size):
            line = []
            for j in range(0, self.width, self.size):
                line.append(0)
            self.cells.append(line)

        self.root = Tk()
        self.root.resizable(width=False, height=False)
        self.root.title("Game Of Life")

        self.canvas = Canvas(self.root,
                             width=self.width,
                             height=self.height,
                             bg=self.colors['bg'])

        # On focus le canvas pour avoir accès aux événements du clavier.
        self.canvas.focus_set()

        # On écoute des évènements du clavier et de la souris.
        self.canvas.bind("<Key>", self.key)
        self.canvas.bind("<Button-1>", self.click)
        self.canvas.bind("<B1-Motion>", self.drag_handler)
        self.canvas.pack()

        """
            On précise qu'on fait une loop dans le canvas pour éviter que
            l'image se close au bout de 2ms
        """
        self.root.mainloop()

    def run(self) -> bool:
        """
        Méthode principale du jeu.

        Fait tourner le jeu de la vie (à l'infini).
        Elle rafraichit l’affichage à chaque tour
        """

        if not self.playing:
            return False

        self.canvas.delete("all")

        for y in range(0, len(self.cells)):
            for x in range(0, len(self.cells[y])):
                status = self.cells[y][x]
                neighbors = self.getNeighborsCount(x, y)

                if status == 0 and neighbors == 3:
                    self.cells[y][x] = 1
                elif status == 1 and neighbors not in [2, 3]:
                    self.cells[y][x] = 0

                color = self.colors['bg'] if self.cells[y][x] == 0 \
                    else self.colors['cell']
                self.canvas.create_rectangle(
                    (x * self.size) - (self.size // 2),
                    (y * self.size) - (self.size // 2),
                    (x * self.size) + (self.size // 2),
                    (y * self.size) + (self.size // 2),
                    fill=color,
                    outline=color)

        self.root.update()
        return self.run()

    def key(self, event) -> None:
        if event.char == 'p':
            self.playing = not self.playing
            if self.playing:
                self.run()

    def click(self, event) -> bool:
        if self.playing:
            return False

        [case, x, y] = self.nearestCase(event.x, event.y)

        if case is None:
            return False

        self.cells[y][x] = 1

        self.canvas.create_rectangle((x * self.size) - (self.size // 2),
                                     (y * self.size) - (self.size // 2),
                                     (x * self.size) + (self.size // 2),
                                     (y * self.size) + (self.size // 2),
                                     fill=self.colors['cell'],
                                     outline=self.colors['bg'])

        return True

    def drag_handler(self, event) -> bool or click:
        if self.playing:
            return False

        return self.click(event)

    def getNeighborsCount(self, x=0, y=0) -> int:
        size = 0

        for new_y in range(y - 1, y + 2):
            for new_x in range(x - 1, x + 2):
                try:
                    cell = self.cells[new_y][new_x]
                except Exception:
                    continue

                if cell == 1 and (new_x != x or new_y != y):
                    size += 1

        return size

    def nearestCase(self, x=0, y=0) -> (int, int, int):
        x = floor(x / self.size)
        y = floor(y / self.size)

        return self.cells[y][x], x, y


gameOfLife = GameOfLife()
gameOfLife.run()
