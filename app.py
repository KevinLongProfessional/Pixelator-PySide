import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QFileDialog, QLabel, QSlider, QApplication, QSpinBox
from PySide6.QtGui import QPixmap
from PySide6 import QtCore
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.button_is_checked = True

        self.setWindowTitle("Pixelator")

         #set constant for image to take up 90% of width to prevent resizing bug.
        self.imageWidthRatio = 0.9

        #set default pixelization ratio to 1.0.
        self.pixelRatio = 1

        layout = QVBoxLayout()

        self.inputWidget = QWidget()
        self.inputWidget.setMaximumHeight(200)
        inputLayout = QVBoxLayout(self.inputWidget)
        layout.addWidget(self.inputWidget)

        button = QPushButton("Select Picture")
        button.setCheckable(True)
        button.clicked.connect(self.file_dialog_button_pressed)
        button.setChecked(self.button_is_checked)
        inputLayout.addWidget(button)

        copyToClipboardButton = QPushButton("Copy To Clipboard")
        copyToClipboardButton.clicked.connect(self.copy_to_clipboard_button_pressed)
        inputLayout.addWidget(copyToClipboardButton)

        pasteFromClipboardButton = QPushButton("Paste From Clipboard")
        pasteFromClipboardButton.clicked.connect(self.paste_from_clipboard_button_pressed)
        inputLayout.addWidget(pasteFromClipboardButton)

        sliderContainerLayout  = QHBoxLayout()
        inputLayout.addLayout(sliderContainerLayout)

        percentInputLabel = QLabel(self)
        percentInputLabel.setText("Pixelation")
        sliderContainerLayout.addWidget(percentInputLabel)

        self.slider = QSlider(Qt.Horizontal);
        self.slider.valueChanged.connect(self.on_slider_value_changed)
        self.slider.setMinimum(1)
        self.slider.setMaximum(100)
        self.slider.setTickInterval(1)
        self.slider.setValue(100)
        sliderContainerLayout.addWidget(self.slider)

        self.percentInput = QSpinBox()
        self.percentInput.setRange(0, 100) # Sets the range for the spin box
        self.percentInput.setValue(100)
        sliderContainerLayout.addWidget(self.percentInput)
        self.percentInput.textChanged.connect(self.percent_input_changed)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.layout = layout

        self.pictureLabel = QLabel(self)
        self.layout.addWidget(self.pictureLabel)
        
    def showEvent(self, event):
        #setup initial test image.

        self.useImage("./testTiger.png")
        self.setScalePix()

    def resizeEvent(self, event):
        if hasattr(self, "pix"):
            self.setScalePix()

        #base resize.
        super().resizeEvent(event)

    def useImage(self, imagepath):
        self.pix = QPixmap(imagepath)
        window_size = self.size()
        self.scalepix = self.pix.scaled(window_size.width() * self.imageWidthRatio, window_size.height() - self.inputWidget.size().height(), QtCore.Qt.KeepAspectRatio) 

        self.pictureLabel.setPixmap(QPixmap(self.scalepix))
    
    def percent_input_changed(self, value):
        self.on_slider_value_changed(int(value))

    def update_percent_value(self, value):
        self.percentInput.setValue(value)
        self.slider.setValue(value)

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
        if hasattr(self, "pix"):
            self.pixelRatio = value / 100;
            self.setScalePix()

            self.update_percent_value(value)

    def setScalePix(self):
        width = max(1, self.pix.width() * self.pixelRatio)
        height = max(1, self.pix.height() * self.pixelRatio)
        self.pixelatedImage = self.pix.scaled(width, height, QtCore.Qt.KeepAspectRatio) 
        pixelatedimage_width = max(500, self.size().width() * self.imageWidthRatio)
        pixelatedimage_height = max(500, self.size().height() - self.inputWidget.size().height())

        self.scalepix = self.pixelatedImage.scaled(pixelatedimage_width, pixelatedimage_height, QtCore.Qt.KeepAspectRatio) 
        self.pictureLabel.setPixmap(QPixmap(self.scalepix))

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()