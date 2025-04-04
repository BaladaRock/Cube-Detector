import cv2

class GridHelper:
    def __init__(self, rows=3, cols=3):
        self.rows = rows
        self.cols = cols
        self.grid = []

    @staticmethod
    def form_grid(squares, tolerance=20):
        if len(squares) != 9:
            return None

        squares.sort(key=lambda s: s[1])
        rows = [[], [], []]

        current_row = 0
        rows[current_row].append(squares[0])
        for sq in squares[1:]:
            if abs(sq[1] - rows[current_row][0][1]) < tolerance:
                rows[current_row].append(sq)
            elif current_row < 2:
                current_row += 1
                rows[current_row].append(sq)

        if any(len(row) != 3 for row in rows):
            return None

        for row in rows:
            row.sort(key=lambda s: s[0])

        return rows

    @staticmethod
    def draw_grid(frame, grid):
        for row in grid:
            for (x, y, w, h) in row:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)  # Yellow box
