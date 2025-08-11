import sys
import math
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QLabel, QSlider, QApplication
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtGui import QPixmap, QImage
from PySide6 import QtCore
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.button_is_checked = True

        self.setWindowTitle("My App")

        layout = QVBoxLayout()

        #to do: add another button that pastes from clipboard or allow ctrl v somehow.
        button = QPushButton("Select Picture")
        button.setCheckable(True)
        button.clicked.connect(self.file_dialog_button_pressed)
        button.setChecked(self.button_is_checked)
        layout.addWidget(button)

        copyToClipboardButton = QPushButton("Copy To Clipboard")
        copyToClipboardButton.clicked.connect(self.copy_to_clipboard_button_pressed)
        layout.addWidget(copyToClipboardButton)

        pasteFromClipboardButton = QPushButton("Paste From Clipboard")
        pasteFromClipboardButton.clicked.connect(self.paste_from_clipboard_button_pressed)
        layout.addWidget(pasteFromClipboardButton)

        self.slider = QSlider(Qt.Horizontal);
        self.slider.valueChanged.connect(self.on_slider_value_changed)
        self.slider.setMinimum(1)
        self.slider.setMaximum(100)
        self.slider.setTickInterval(1)
        self.slider.setValue(100)

        layout.addWidget(self.slider)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.layout = layout

        self.pictureLabel = QLabel(self)
        self.layout.addWidget(self.pictureLabel)
        self.useImage("./testTiger.png")

    def useImage(self, imagepath):
        self.pix = QPixmap(imagepath)
        window_size = self.size()
        self.scalepix = self.pix.scaled(window_size.width(), window_size.height() * 0.8, QtCore.Qt.KeepAspectRatio) 
        
        self.pictureLabel.setPixmap(QPixmap(self.scalepix))
    

    def file_dialog_button_pressed(self, checked):
        fname = QFileDialog.getOpenFileName(self, 'Open file', 
             'c:\\',"Image files (*.jpg *.gif *.svg)")
        imagepath = fname[0]

        self.useImage(imagepath)

    def paste_from_clipboard_button_pressed(self):
        clipboard = QApplication.clipboard()
        image_from_clipboard = clipboard.image()
        if not image_from_clipboard.isNull():
            clipboardImage = QPixmap.fromImage(image_from_clipboard)
            self.useImage(clipboardImage)
        

    def copy_to_clipboard_button_pressed(self):
        clipboard = QApplication.clipboard()

        # Set the QPixmap to the clipboard
        clipboard.setPixmap(self.scalepix)

    def on_slider_value_changed(self, value):
            print(value)
            print((self.size()))
            self.pixelRatio = value / 100;
            width = max(1, self.pix.width() * self.pixelRatio)
            height = max(1, self.pix.height() * self.pixelRatio)
            pixelatedImage = self.pix.scaled(width, height, QtCore.Qt.KeepAspectRatio) 
            
            window_width = self.size().width()
            window_height = self.size().height() * 0.8

            self.scalepix = pixelatedImage.scaled(window_width, window_height, QtCore.Qt.KeepAspectRatio) 
            self.pictureLabel.setPixmap(QPixmap(self.scalepix))
            print((self.size()))


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()