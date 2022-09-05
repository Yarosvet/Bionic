# Bionic - desktop biological determinant
![Main window](https://github.com/Yarosvet/Bionic/raw/master/screenshots/main_window.png)
___
# Download binary
Available executables:
* **[Windows](https://github.com/Yarosvet/Bionic/releases/download/0.1/Bionic.exe)**
* **[Linux](https://github.com/Yarosvet/Bionic/releases/download/0.1/Bionic)**
# Run with python
```bash
pip3 install -r requirements.txt
python3 main.py
```
# Build
Install *pyinstaller*
```bash
pip3 install pyinstaller
```
And build binary
```bash
pyinstaller --noconsole --onefile main.py
```
The binary file will be exported to *dist* directory

# Screenshots
![Add book](https://github.com/Yarosvet/Bionic/raw/master/screenshots/add_dialog.png)
![Entry points](https://github.com/Yarosvet/Bionic/raw/master/screenshots/entry_window.png)
![Determinant](https://github.com/Yarosvet/Bionic/raw/master/screenshots/determinant_window.png)