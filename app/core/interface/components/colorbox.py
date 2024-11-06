from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget, QSizePolicy, QColorDialog
from PyQt6.QtCore import Qt
from core.interface.styles.styles import Styles
from core.utils.signals import signal_manager

class ColorboxLayout(QWidget):
    def __init__(self, title, description, color, config_id=None, parent=None):
        super().__init__(parent)
        self.config_id = config_id
        self.initUI(title, description, color, config_id)
         
    def initUI(self, title, description, color, config_id=None):
 
        # Create a container widget to apply the background color and border radius
        container = QWidget()
        container.setObjectName('options_container')
        container.setStyleSheet(Styles.CONTAINER)
        container_layout = QHBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)
        container.setFixedHeight(70)
        
        # Create the left layout
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(10, 0, 0, 0)
        self.name_label = QLabel(title)
        self.name_label.setStyleSheet(Styles.LABEL_TITLE)
        self.description_label = QLabel(description)
        self.description_label.setStyleSheet(Styles.LABEL_DESCRIPTION)
        
        left_layout.addWidget(self.name_label)
        left_layout.addWidget(self.description_label)
        
        # Create the right layout
        right_layout = QHBoxLayout()
        right_layout.setContentsMargins(0, 0, 10, 0)
        self.color_label = QLabel(color)
        self.color_label.setStyleSheet(f'color: {color}; font-size: 14px; font-family: Arial; padding-right:10px')
        self.color_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.color_button = QPushButton()
        self.color_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.color_button.setObjectName('color_button')
        self.color_button.setFixedSize(30, 30)
        self.color_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.color_button.clicked.connect(self.open_color_picker)
        
        # Style the button
        button_style = f"""
        QPushButton#color_button {{
            border-radius: 15px;
            padding: 0px;
            margin: 0px;
            background-color: {color};
            color: transparent;
        }}
        """
        self.color_button.setStyleSheet(button_style)
        # Set size policy to prevent stretching
        self.color_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.color_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        right_layout.addWidget(self.color_label)
        right_layout.addWidget(self.color_button)
        # Add left and right layouts to the container layout
        container_layout.addLayout(left_layout)
        container_layout.addLayout(right_layout)
        # Set the container layout as the main layout
        main_layout = QHBoxLayout(self)
        main_layout.addWidget(container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)

    def open_color_picker(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color_label.setText(color.name())
            self.color_label.setStyleSheet(f'color: {color.name()}; font-size: 14px; font-family: Segoe UI; padding-right:10px')
            self.color_button.setStyleSheet(f'background-color: {color.name()}; border-radius: 15px; padding: 0px; margin: 0px;')
            signal_manager.value_changed.emit()
            
    def get_value(self):
        return self.color_label.text()
    
    def set_value(self, value):
        self.color_label.setText(value)
        self.color_label.setStyleSheet(f'color: {value}; font-size: 14px; font-family: Segoe UI; padding-right:10px')
        self.color_button.setStyleSheet(f'background-color: {value}; border-radius: 15px; padding: 0px; margin: 0px;')