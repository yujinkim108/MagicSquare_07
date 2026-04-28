"""PyQt6 screen layer.

Keeps UI concerns in this module and delegates business rules to boundary.
"""

from __future__ import annotations

from typing import List

from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from magicsquare.boundary import BoundaryError, solve
from magicsquare.constants import CELL_EMPTY, MATRIX_SIZE


class MainWindow(QMainWindow):
    """Simple MVP screen for entering a 4x4 grid and solving."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Magic Square 4x4")
        self._cells: list[list[QLineEdit]] = []
        self._result_label = QLabel("결과: [r1,c1,n1,r2,c2,n2]")
        self._result_label.setWordWrap(True)
        self._build_ui()

    def _build_ui(self) -> None:
        root = QWidget()
        main_layout = QVBoxLayout()
        grid_layout = QGridLayout()

        for row in range(MATRIX_SIZE):
            row_cells: list[QLineEdit] = []
            for col in range(MATRIX_SIZE):
                cell = QLineEdit("0")
                cell.setMaxLength(2)
                cell.setPlaceholderText("0")
                cell.setFixedWidth(56)
                grid_layout.addWidget(cell, row, col)
                row_cells.append(cell)
            self._cells.append(row_cells)

        button_row = QHBoxLayout()
        solve_button = QPushButton("풀기")
        solve_button.clicked.connect(self._on_solve_clicked)
        button_row.addWidget(solve_button)

        main_layout.addLayout(grid_layout)
        main_layout.addLayout(button_row)
        main_layout.addWidget(self._result_label)
        root.setLayout(main_layout)
        self.setCentralWidget(root)

    def _on_solve_clicked(self) -> None:
        try:
            grid = self._read_grid()
            result = solve(grid)
            self._result_label.setText(f"결과: {result}")
        except ValueError as exc:
            self._show_error(str(exc))
        except BoundaryError as exc:
            self._show_error(exc.code.value)

    def _read_grid(self) -> List[List[int]]:
        grid: list[list[int]] = []
        for row in self._cells:
            values: list[int] = []
            for cell in row:
                text = cell.text().strip()
                if text == "":
                    values.append(CELL_EMPTY)
                    continue
                try:
                    values.append(int(text))
                except ValueError as exc:
                    raise ValueError("모든 칸에는 정수를 입력하세요.") from exc
            grid.append(values)
        return grid

    def _show_error(self, message: str) -> None:
        QMessageBox.critical(self, "입력/풀이 오류", message)


def run() -> int:
    app = QApplication([])
    window = MainWindow()
    window.show()
    return app.exec()

