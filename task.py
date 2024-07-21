from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QMessageBox
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
from PySide2.QtGui import QIcon
import sys
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import warnings
import sympy as sp

class MplWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.canvas = FigureCanvas(Figure())
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        vertical_layout.addWidget(NavigationToolbar(self.canvas, self))
        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.setLayout(vertical_layout)

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.init_ui()

    def init_ui(self):
        designer_file = QFile("task.ui")
        designer_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        loader.registerCustomWidget(MplWidget)
        self.ui = loader.load(designer_file, self)
        designer_file.close()

        self.setWindowTitle("Equation Drawing")
        self.setGeometry(100, 100, 800, 600)
        self.set_icon()
        self.setup_connections()

    def draw(self, min_value, max_value, formula):
        try:
            formula = self.string2func(str(formula))
            
            # Generate x values
            x = np.linspace(min_value, max_value, 1000)
            
            # Convert warnings to exceptions to make sure that the program will stops during any wrong input
            with warnings.catch_warnings():
                warnings.simplefilter("error", RuntimeWarning)
                
                # Evaluate the formula
                y = eval(formula, {"x": x, "np": np})
                
                # Check for NaN or infinite values
                if np.any(np.isnan(y)) or np.any(np.isinf(y)):
                    self.error("Invalid values encountered in the mathematical operation.")
                    return
            
            # Plot the function if no errors or warnings
            self.plot(x, y)
        
        except (SyntaxError, NameError) as e:
            self.error(f"Error in the formula: {str(e)}")
        except ValueError as e:
            self.error(str(e))
        except Exception as e:
            self.error(f"An unexpected error occurred: {str(e)}")



    def set_icon(self):
        appIcon = QIcon("screenshots/icon.png")
        self.setWindowIcon(appIcon)

    def setup_connections(self):
        self.ui.draw.clicked.connect(self.check_input) 
        self.ui.reset.clicked.connect(self.reset_graph)
    
    def reset_graph(self):
        self.ui.MplWidget.canvas.axes.clear()  
        self.ui.MplWidget.canvas.draw()      

    def string2func(self,string):

        replacements = {
                'sin' : 'np.sin',
                'cos' : 'np.cos',
                'exp': 'np.exp',
                'sqrt': 'np.sqrt',
                'log' : 'np.log',
                '^': '**',
            }

        for old, new in replacements.items():
            string = string.replace(old, new)
        return string

    def check_input(self):
        
        formula = self.ui.formula.text()
        min_value = self.ui.min_value.text()  #to check that all fields not empty
        max_value = self.ui.max_value.text()


        if formula and min_value and max_value:
            try:
                min_value = float(min_value)
                max_value = float(max_value)
                if min_value >= max_value:
                    self.error("The Min Value is Greater Than Max Value")
                else:
                    self.draw(min_value,max_value,formula)
            except ValueError:
                self.error("Please Enter Valid Numbers in Min and Max Values.")
        else:
            self.error("Please Fill All Fields.")

    def error(self, content):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Warning)
        msg.setText(content)
        msg.setWindowTitle("Input Error")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
    def plot(self, x, y):
        self.ui.MplWidget.canvas.axes.clear()
        self.ui.MplWidget.canvas.axes.plot(x, y)
        self.ui.MplWidget.canvas.axes.set_title('')
        self.ui.MplWidget.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
