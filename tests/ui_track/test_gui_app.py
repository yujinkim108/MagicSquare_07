"""GUI app tests for input parsing and solve event handling."""

from __future__ import annotations

import pytest
from PyQt6.QtWidgets import QApplication

from magicsquare.boundary import BoundaryError, ErrorCode
from magicsquare.constants import CELL_EMPTY
from magicsquare.gui.app import MainWindow
import magicsquare.gui.app as app_module


@pytest.fixture(scope="session")
def qapp() -> QApplication:
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


@pytest.fixture
def window(qapp: QApplication) -> MainWindow:
    _ = qapp
    return MainWindow()


class TestGuiApp:
    def test_read_grid_parses_blank_as_empty_and_numbers_as_int(self, window: MainWindow) -> None:
        window._cells[0][0].setText("")
        window._cells[0][1].setText("12")

        grid = window._read_grid()

        assert grid[0][0] == CELL_EMPTY
        assert grid[0][1] == 12

    def test_read_grid_non_integer_raises_value_error(self, window: MainWindow) -> None:
        window._cells[0][0].setText("abc")

        with pytest.raises(ValueError, match="모든 칸에는 정수를 입력하세요."):
            window._read_grid()

    def test_on_solve_clicked_success_updates_result_label(self, window: MainWindow, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(app_module, "solve", lambda _grid: [1, 1, 16, 4, 4, 1])
        shown_errors: list[str] = []
        monkeypatch.setattr(window, "_show_error", lambda message: shown_errors.append(message))

        window._on_solve_clicked()

        assert window._result_label.text() == "결과: [1, 1, 16, 4, 4, 1]"
        assert shown_errors == []

    def test_on_solve_clicked_value_error_shows_message(self, window: MainWindow, monkeypatch: pytest.MonkeyPatch) -> None:
        def _raise_value_error(_grid: list[list[int]]) -> list[int]:
            raise ValueError("숫자 변환 오류")

        shown_errors: list[str] = []
        monkeypatch.setattr(app_module, "solve", _raise_value_error)
        monkeypatch.setattr(window, "_show_error", lambda message: shown_errors.append(message))

        window._on_solve_clicked()

        assert shown_errors == ["숫자 변환 오류"]

    def test_on_solve_clicked_boundary_error_shows_code_value(
        self, window: MainWindow, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        def _raise_boundary_error(_grid: list[list[int]]) -> list[int]:
            raise BoundaryError(ErrorCode.INVALID_SIZE)

        shown_errors: list[str] = []
        monkeypatch.setattr(app_module, "solve", _raise_boundary_error)
        monkeypatch.setattr(window, "_show_error", lambda message: shown_errors.append(message))

        window._on_solve_clicked()

        assert shown_errors == [ErrorCode.INVALID_SIZE.value]

    def test_show_error_calls_qmessagebox_critical(
        self, window: MainWindow, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        captured: list[tuple[object, str, str]] = []

        def _fake_critical(parent: object, title: str, message: str) -> None:
            captured.append((parent, title, message))

        monkeypatch.setattr(app_module.QMessageBox, "critical", _fake_critical)

        window._show_error("에러")

        assert captured == [(window, "입력/풀이 오류", "에러")]

    def test_run_creates_window_shows_and_executes(self, monkeypatch: pytest.MonkeyPatch) -> None:
        calls: list[str] = []

        class FakeWindow:
            def show(self) -> None:
                calls.append("show")

        class FakeApp:
            def __init__(self, _argv: list[str]) -> None:
                calls.append("app_init")

            def exec(self) -> int:
                calls.append("exec")
                return 7

        monkeypatch.setattr(app_module, "QApplication", FakeApp)
        monkeypatch.setattr(app_module, "MainWindow", FakeWindow)

        exit_code = app_module.run()

        assert exit_code == 7
        assert calls == ["app_init", "show", "exec"]
