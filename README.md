# Master's Thesis

[ES] Control de asistencia y distancia social automatizado mediante reconocimiento de imágenes.

[EN] Automated attendance and social distance control through image recognition.

## Packages installation

Use the package-management system [pip](https://pip.pypa.io/en/stable/) to install the required packages.

```bash
$ pip install requests
$ pip install Pillow
$ pip install numpy
$ pip install opencv-python
$ pip install opencv-contrib-python
$ pip install scipy
$ pip install pyqt5
$ pip install pyqt5-tools
$ pip install pyinstaller
```

To create the auto_training_gui.exe, just run the following command on the source folder:

```bash
$ pyinstaller --clean --onefile --windowed auto_training_gui.py
```
