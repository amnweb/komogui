from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget, QSizePolicy
from PyQt6.QtCore import Qt, QTimer
from core.interface.styles.styles import Styles
from core.utils.signals import signal_manager

class ButtonLayout(QWidget):
    def __init__(self, title, description, value, min_value, max_value, config_id=None, parent=None):
        super().__init__(parent)
 
        
        self.min_value = min_value
        self.max_value = max_value
        self.current_value = value
        self.config_id = config_id
        
        # Add timer setup
        self.timer = QTimer()
        self.timer.timeout.connect(self.on_timer)
        self.active_button = None

        self.INITIAL_DELAY = 500  # Initial delay in ms before fast mode
        self.FAST_INTERVAL = 10   # Fast increment interval in ms
        self.hold_timer = QTimer() 
        self.hold_timer.setSingleShot(True)
        self.hold_timer.timeout.connect(self.start_fast_mode)
        
        self.initUI(title, description, value, min_value, max_value, config_id)

    def initUI(self, title, description, value, min_value, max_value, config_id):
        # Create the main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create the container widget
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
        self.value_label = QLabel(str(value))
        self.value_label.setStyleSheet('color: rgba(255,255,255,0.8);font-size: 14px;font-family: "Segoe UI";font-weight:600;padding-right:10px;')
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.plus_button = QPushButton('+')
        self.minus_button = QPushButton('-')
        self.plus_button.setFixedSize(34, 30)
        self.minus_button.setFixedSize(34, 30)
        self.plus_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.minus_button.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.plus_button.clicked.connect(self.increase_value)
        self.minus_button.clicked.connect(self.decrease_value)
        
        # Modify button setup to include press/release events
        self.plus_button.pressed.connect(lambda: self.on_button_pressed(self.plus_button))
        self.plus_button.released.connect(self.on_button_released)
        self.minus_button.pressed.connect(lambda: self.on_button_pressed(self.minus_button))
        self.minus_button.released.connect(self.on_button_released)
 
        self.plus_button.setStyleSheet(Styles.BUTTON_ROUNDED)
        self.minus_button.setStyleSheet(Styles.BUTTON_ROUNDED)
        
        # Set size policies
        self.plus_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.minus_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.value_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        
        right_layout.addWidget(self.value_label)
        right_layout.addWidget(self.minus_button)
        right_layout.addWidget(self.plus_button)
        
        container_layout.addLayout(left_layout)
        container_layout.addLayout(right_layout)
        main_layout.addWidget(container)
        self.setLayout(main_layout)

    def increase_value(self):
        current_value = int(self.value_label.text())
        if current_value < self.max_value:
            self.value_label.setText(str(current_value + 1))
            signal_manager.value_changed.emit()

    def decrease_value(self):
        current_value = int(self.value_label.text())
        if current_value > self.min_value:
            self.value_label.setText(str(current_value - 1))
            signal_manager.value_changed.emit()
                   
    def on_button_pressed(self, button):
        self.active_button = button
        self.hold_timer.start(self.INITIAL_DELAY)
        
    def on_button_released(self):
        self.timer.stop()
        self.hold_timer.stop()
        self.active_button = None
        
        if self.active_button == self.plus_button:
            self.increase_value()
        elif self.active_button == self.minus_button:
            self.decrease_value()

    def on_timer(self):
        if self.active_button == self.plus_button:
            self.increase_value()
        elif self.active_button == self.minus_button:
            self.decrease_value()
            
    def start_fast_mode(self):
        if self.active_button:
            self.timer.start(self.FAST_INTERVAL)
            
    def get_value(self):
        return self.value_label.text()
    
    def set_value(self, value):
        self.value_label.setText(str(value))