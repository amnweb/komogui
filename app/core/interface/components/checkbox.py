from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QWidget, QSizePolicy, QCheckBox
from PyQt6.QtCore import Qt
from core.interface.styles.styles import Styles
from core.utils.signals import signal_manager

class CheckboxLayout(QWidget):
    def __init__(self, title, description, checked, config_id=None, parent=None):
        super().__init__(parent)
        self.config_id = config_id
        self.initUI(title, description, checked)

    def initUI(self, title, description, checked):
        # Create the main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create the container widget to apply the background color and border radius
        container = QWidget()
        container.setObjectName('options_container')
        container.setStyleSheet(Styles.CONTAINER)
        
        container_layout = QHBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)
        container.setFixedHeight(70)
        
        # Create the left layout for the container
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(10, 0, 0, 0)
        self.name_label = QLabel(title)
        self.name_label.setStyleSheet(Styles.LABEL_TITLE)
        self.description_label = QLabel(description)
        self.description_label.setStyleSheet(Styles.LABEL_DESCRIPTION)
        
        left_layout.addWidget(self.name_label)
        left_layout.addWidget(self.description_label)
        
        # Create the right layout for the container
        right_layout = QHBoxLayout()
        right_layout.setContentsMargins(0, 0, 10, 0)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.checkbox = QCheckBox()
        # Add this to your checkbox styling, after creating the checkbox
        self.checkbox.setStyleSheet(Styles.CHECKBOX)
 
        self.checkbox.setChecked(checked)
        self.checkbox.stateChanged.connect(self.toggle_enabled)
        self.checkbox.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        
        right_layout.addWidget(self.checkbox)
        
        # Add left and right layouts to the container layout
        container_layout.addLayout(left_layout)
        container_layout.addLayout(right_layout)
        
        # Add the container to the main layout
        main_layout.addWidget(container)
        self.setLayout(main_layout)

    def toggle_enabled(self, state):
        self.is_enabled = (state == Qt.CheckState.Checked.value)
        self.name_label.setEnabled(self.is_enabled)
        self.description_label.setEnabled(self.is_enabled)
        signal_manager.value_changed.emit()

    def get_value(self):
        value = self.checkbox.isChecked()
        return value
    
    def set_value(self, value):
        self.checkbox.setChecked(value)
        self.toggle_enabled(value)