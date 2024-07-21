import pytest
from PySide2.QtWidgets import QMessageBox
from PySide2.QtCore import Qt
from task import MainWindow  

@pytest.fixture
def app(qtbot):
    main_window = MainWindow()
    qtbot.addWidget(main_window)
    main_window.show()
    yield main_window

def test_initial_ui_state(app):
    assert app.windowTitle() == "Equation Drawing"
    assert app.ui.formula.text() == ""
    assert app.ui.min_value.text() == ""
    assert app.ui.max_value.text() == ""

def test_draw_function_valid_input(qtbot, app):
    # Test 1: sin(x) from 0 to 10
    app.ui.formula.setText("sin(x)")
    app.ui.min_value.setText("0")
    app.ui.max_value.setText("10")
    qtbot.mouseClick(app.ui.draw, Qt.LeftButton)
    assert app.ui.MplWidget.canvas.axes.has_data()  

    # Test 2: 5*x^3 + 2*x from 0 to 5
    app.ui.formula.setText("5*x**3 + 2*x")
    app.ui.min_value.setText("0")
    app.ui.max_value.setText("5")
    qtbot.mouseClick(app.ui.draw, Qt.LeftButton)
    assert app.ui.MplWidget.canvas.axes.has_data() 

    # Test 3: log(10*x) from 2 to 4
    app.ui.formula.setText("log(10*x)")
    app.ui.min_value.setText("2")
    app.ui.max_value.setText("4")
    qtbot.mouseClick(app.ui.draw, Qt.LeftButton)
    assert app.ui.MplWidget.canvas.axes.has_data()  

def test_draw_function_invalid_minMax(qtbot, app):

    app.ui.formula.setText("sin(x)")
    app.ui.min_value.setText("10")
    app.ui.max_value.setText("0")
    qtbot.mouseClick(app.ui.draw, Qt.LeftButton)
    error_message = app.findChild(QMessageBox)
    assert error_message is not None
    assert error_message.text() == "The Min Value is Greater Than Max Value"
    qtbot.mouseClick(error_message.button(QMessageBox.Ok), Qt.LeftButton)


def test_draw_function_invalid_input(qtbot, app):
    # Test 1: invalid formula
    app.ui.formula.setText("5*x^^2")
    app.ui.min_value.setText("0")
    app.ui.max_value.setText("5")
    qtbot.mouseClick(app.ui.draw, Qt.LeftButton)
    error_message = app.findChild(QMessageBox)
    assert error_message is not None
    qtbot.mouseClick(error_message.button(QMessageBox.Ok), Qt.LeftButton)

    # Test 2: log of negative value
    app.ui.formula.setText("log(x)")
    app.ui.min_value.setText("-1")
    app.ui.max_value.setText("1")
    qtbot.mouseClick(app.ui.draw, Qt.LeftButton)
    error_message = app.findChild(QMessageBox)
    assert error_message is not None
    qtbot.mouseClick(error_message.button(QMessageBox.Ok), Qt.LeftButton)

    # Test 3: division by zero
    app.ui.formula.setText("1/x")
    app.ui.min_value.setText("0")
    app.ui.max_value.setText("1")
    qtbot.mouseClick(app.ui.draw, Qt.LeftButton)
    error_message = app.findChild(QMessageBox)
    assert error_message is not None
    qtbot.mouseClick(error_message.button(QMessageBox.Ok), Qt.LeftButton)
    

def test_reset_function(qtbot, app):
    app.ui.formula.setText("sin(x)")
    app.ui.min_value.setText("0")
    app.ui.max_value.setText("10")
    qtbot.mouseClick(app.ui.draw, Qt.LeftButton)
    assert app.ui.MplWidget.canvas.axes.has_data()  
    
    qtbot.mouseClick(app.ui.reset, Qt.LeftButton)
    assert not app.ui.MplWidget.canvas.axes.has_data()  # check if the plot has been cleared
