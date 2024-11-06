# core/options/stackbar.py
from PyQt6.QtWidgets import QVBoxLayout, QWidget
from core.interface.components.button import ButtonLayout
from core.interface.components.dropdown import DropdownLayout
from core.interface.components.colorbox import ColorboxLayout
from core.interface.components.input import InputLayout

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
        
    def add_dropdown_layout(self, title, description, options, config_id=None):
        dropdown_layout = DropdownLayout(title, description, options, config_id=config_id)
        self.main_layout.addWidget(dropdown_layout)
 
    def add_colorbox_layout(self, title, description, options, config_id=None):
        colorbox_layout = ColorboxLayout(title, description, options, config_id=config_id)
        self.main_layout.addWidget(colorbox_layout)
        
    def add_input_layout(self, title, description, default_value="", config_id=None):
        input_layout = InputLayout(title, description, default_value, config_id=config_id)
        self.main_layout.addWidget(input_layout)
    
def stackbar_widget():
    stackbar_layout = DynamicLayout()
    
    # Main stackbar settings
    stackbar_layout.add_dropdown_layout(
        'Stackbar mode', 
        'Stackbar configuration options', 
        ["Always", "Never", "OnStack"],
        config_id="stackbar.mode"
    )
    
    stackbar_layout.add_options_layout(
        'Stackbar height', 
        'Stackbar height options', 
        0, 0, 200,
        config_id="stackbar.height"
    )
    
    stackbar_layout.add_dropdown_layout(
        'Stackbar label', 
        'Stackbar label options', 
        ["Process", "Title"],
        config_id="stackbar.label"
    )
    
    # Tabs section - note the updated config_ids
    stackbar_layout.add_colorbox_layout(
        'Tabs background', 
        'Stackbar tabs background color', 
        "#ffffff",
        config_id="stackbar.tabs.background"
    )
    
    stackbar_layout.add_colorbox_layout(
        'Focused text', 
        'Stackbar tabs focused text color', 
        "#ffffff",
        config_id="stackbar.tabs.focused_text"
    )
    
    stackbar_layout.add_colorbox_layout(
        'Unfocused text', 
        'Stackbar tabs unfocused text color', 
        "#ffffff",
        config_id="stackbar.tabs.unfocused_text"
    )
    
    stackbar_layout.add_input_layout(
        'Font family', 
        'Stackbar tabs font family', 
        "Segoe UI",
        config_id="stackbar.tabs.font_family"
    )
    
    stackbar_layout.add_options_layout(
        'Font size', 
        'Stackbar tabs font size', 
        0, 0, 36,
        config_id="stackbar.tabs.font_size"
    )
    
    stackbar_layout.add_options_layout(
        'Tabs width', 
        'Stackbar tabs width', 
        0, 0, 1000,
        config_id="stackbar.tabs.width"
    )
     
    return stackbar_layout