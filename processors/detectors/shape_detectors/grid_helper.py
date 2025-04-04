import cv2

class GridHelper:
    def __init__(self, rows=3, cols=3):
        self.rows = rows
        self.cols = cols
        self.grid = []

    @staticmethod
    def form_grid(squares):
        if len(squares) != 9:
            return None

        squares = sorted(squares, key=lambda s: s[1])

        rows = [sorted(squares[i * 3:(i + 1) * 3], key=lambda s: s[0]) for i in range(3)]

        return rows

    @staticmethod
    def draw_grid(frame, grid):
        for row in grid:
            for (x, y, w, h) in row:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)  # Yellow box
