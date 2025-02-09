# Function-Plotter
Develop a Python GUI application using PySide2 and Matplotlib that allows users to plot mathematical functions.
## Features

1. **Function Plotting**: Plot an arbitrary user-entered function.
2. **Input Handling**: Accepts mathematical functions of `x` (e.g., `5*x^3 + 2*x`).
3. **Range Specification**: Allows users to set the minimum and maximum values of `x`.
4. **Supported Operators**: Supports `+`, `-`, `/`, `*`, `^`, `log10()`, `sqrt()`.
5. **Input Validation**: Validates user input and displays error messages for invalid input.
6. **Embedded Matplotlib Plot**: The Matplotlib plot is embedded within the PySide2 application.
7. **Automated Testing**: Includes end-to-end tests using pytest and pytest-qt.

## Requirements

- Python 3.10
- PySide2
- Matplotlib
- pytest
- pytest-qt

## Example Screenshots

### Working Example
<img src="/screenshots/1.jpg" alt="Working Example" width="400"/>
<img src="/screenshots/4.jpg" alt="Working Example" width="400"/>

### Error Example
<img src="/screenshots/2.jpg" alt="Not Working Example" width="400"/>
<img src="/screenshots/3.jpg" alt="Not Working Example" width="400"/>
<img src="/screenshots/5.jpg" alt="Not Working Example" width="400"/>

### Tests
<img src="/screenshots/tests_passes.jpg" alt="Tests passed" width="400"/>