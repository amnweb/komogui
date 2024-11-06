# core/options/transparency.py
from PyQt6.QtWidgets import QVBoxLayout, QWidget
from core.interface.components.button import ButtonLayout
from core.interface.components.checkbox import CheckboxLayout

class DynamicLayout(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)
        
    def add_options_layout(self, title, description, value, min_value, max_value, config_id=None):
        options_layout = ButtonLayout(title, description, value, min_value, max_value, config_id=config_id)
        self.main_layout.addWidget(options_layout)

    def add_checkbox_layout(self, title, description, checked, config_id=None):
        checkbox_layout = CheckboxLayout(title, description, checked, config_id=config_id)
        self.main_layout.addWidget(checkbox_layout)
 
        
def transparency_widget():
    transparency_layout = DynamicLayout()
    
    transparency_layout.add_checkbox_layout(
        'Transparency', 
        'Add transparency to unfocused windows', 
        False,
        config_id="transparency"
    )
    
    transparency_layout.add_options_layout(
        'Transparency alpha', 
        'Alpha value for unfocused window transparency', 
        225,
        0, 
        255,
        config_id="transparency_alpha"
    )
 
    return transparency_layout