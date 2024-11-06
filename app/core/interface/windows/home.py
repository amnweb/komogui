from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGraphicsBlurEffect
from PyQt6.QtCore import Qt, QPropertyAnimation
from PyQt6.QtGui import QPixmap
import os

class AnimatedLabel(QWidget):
    def __init__(self, pixmap=None, text='', parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.label = QLabel(self)
        if pixmap:
            self.label.setPixmap(pixmap)
        else:
            self.label.setText(text)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label) 
        self.blur_effect = QGraphicsBlurEffect(self.label)
        self.initAnimations()

    def initAnimations(self):
        self.blur_animation = QPropertyAnimation(self.blur_effect, b"blurRadius")
        self.blur_animation.setDuration(400)
        self.blur_animation.setStartValue(20)
        self.blur_animation.setEndValue(0)

    def startAnimation(self):
        self.label.setGraphicsEffect(self.blur_effect)
        self.blur_animation.start()

class Home(QWidget):
    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout(self)

        # Logo Image, ensure the path exists correctly
        logo_path = os.path.join("app", "assets", "komorebi.png")
        pixmap = QPixmap(logo_path)
        scaled_pixmap = pixmap.scaled(128, 128, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

        # Animated logo
        self.logo_label = AnimatedLabel(pixmap=scaled_pixmap)
        self.main_layout.addWidget(self.logo_label)

        # Animated title
        self.title = AnimatedLabel(
            text='<span style="font-weight:400;">Komo</span><span style="font-weight:800;">GUI</span>')
        self.title.label.setStyleSheet("color: white; font-family: Segoe UI; font-size:48px;")
        self.title.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.title)

        # Animated description
        self.description = AnimatedLabel(
            text="Load a configuration file to begin configuring your tiling world.")
        self.description.label.setStyleSheet(
            "color: rgba(255,255,255,0.8); font-weight:normal; font-family: Segoe UI; font-size: 18px;")
        self.description.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.description)

        self.setLayout(self.main_layout)

    def showEvent(self, event):
        # Start animations when the window is shown
        self.logo_label.startAnimation()
        self.title.startAnimation()
        self.description.startAnimation()
        super().showEvent(event)