from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QWidget, QSizePolicy, QLineEdit
from PyQt6.QtCore import Qt
from core.interface.styles.styles import Styles
from core.utils.signals import signal_manager

class InputLayout(QWidget):
    def __init__(self, title, description, default_value="", config_id=None, parent=None):
        super().__init__(parent)
        self.config_id = config_id
        self.initUI(title, description, default_value, config_id)
        
    def initUI(self, title, description, default_value, config_id=None):
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
        right_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        self.input_field = QLineEdit()
        self.input_field.setText(str(default_value))
        self.input_field.setStyleSheet(Styles.INPUT_FIELD + """
        QLineEdit QMenu {
            background-color: #2b2f35;
            border: 1px solid #3c4047;
            padding: 0;
            border-radius: 8px;
            margin:0; 
            outline: none;    
        }
        QLineEdit QMenu::item {
            padding: 6px 20px;
            color: #ffffff;
            border-radius: 2px;
            background-color: transparent;
        }

        QLineEdit QMenu::item:selected {
            background-color: #3c4047;
            color: #ffffff;
        }
        QLineEdit QMenu::separator {
            height: 1px;
            background-color: #3c4047;
            margin: 5px 0px;
        }
        QLineEdit QMenu::icon {
            padding-left: 14px; 
        }
        """)
        self.input_field.setFixedWidth(200)
        self.input_field.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        
        right_layout.addWidget(self.input_field)
        
        # Add left and right layouts to the container layout
        container_layout.addLayout(left_layout)
        container_layout.addLayout(right_layout)
        
        # Add the container to the main layout
        main_layout.addWidget(container)
        self.setLayout(main_layout)
        self.input_field.textChanged.connect(lambda _: signal_manager.value_changed.emit())
        
    def get_value(self):
        return self.input_field.text()

    def set_value(self, value):
        self.input_field.setText(str(value))