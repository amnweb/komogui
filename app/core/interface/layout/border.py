# core/options/animation.py
from PyQt6.QtWidgets import QVBoxLayout, QWidget
from core.interface.components.button import ButtonLayout
from core.interface.components.checkbox import CheckboxLayout
from core.interface.components.dropdown import DropdownLayout
from core.interface.components.colorbox import ColorboxLayout

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

    def add_checkbox_layout(self, title, description, checked, config_id=None):
        checkbox_layout = CheckboxLayout(title, description, checked, config_id=config_id)
        self.main_layout.addWidget(checkbox_layout)
        
    def add_colorbox_layout(self, title, description, options, config_id=None):
        colorbox_layout = ColorboxLayout(title, description, options, config_id=config_id)
        self.main_layout.addWidget(colorbox_layout)
        
def border_widget():
    border_layout = DynamicLayout()
    
    # Main border settings
    border_layout.add_checkbox_layout(
        'Enable Border', 
        'Display an active window border', 
        True,
        config_id="border"
    )
    
    # Border implementation settings
    border_layout.add_dropdown_layout(
        'Border implementation', 
        'Active window border implementation', 
        ["Komorebi", "Windows"],
        config_id="border_implementation"
    )
    
    border_layout.add_dropdown_layout(
        'Border style', 
        'Active window border style', 
        ["System", "Rounded", "Square"],
        config_id="border_style"
    )
    
    border_layout.add_options_layout(
        'Border width', 
        'Width of the window border', 
        8, 0, 24,
        config_id="border_width"
    )
    
    border_layout.add_options_layout(
        'Border offset', 
        'Offset of the window border', 
        0, -10, 24,
        config_id="border_offset"
    )
    
    # Border colors section
    border_layout.add_colorbox_layout(
        'Single', 
        'Colour when the container contains a single window', 
        "#ffffff",
        config_id="border_colours.single"
    )
    
    border_layout.add_colorbox_layout(
        'Stack', 
        'Colour when the container contains multiple windows', 
        "#ffffff",
        config_id="border_colours.stack"
    )
    
    border_layout.add_colorbox_layout(
        'Monocle', 
        'Colour when the container is in monocle mode', 
        "#ffffff",
        config_id="border_colours.monocle"
    )
    
    border_layout.add_colorbox_layout(
        'Unfocused', 
        'Colour when the container is unfocused', 
        "#ffffff",
        config_id="border_colours.unfocused"
    )

    return border_layout