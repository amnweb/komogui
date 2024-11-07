from PyQt6.QtWidgets import QVBoxLayout, QWidget
from core.interface.components.button import ButtonLayout
from core.interface.components.checkbox import CheckboxLayout
from core.interface.components.dropdown import DropdownLayout

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
 
    
def general_widget():
    general_layout = DynamicLayout()
    # Add widgets with their config IDs
    general_layout.add_dropdown_layout(
        'Window hiding behaviour', 
        'Which Windows signal to use when hiding windows', 
        ["Hide","Minimize","Cloak"], 
        config_id="window_hiding_behaviour"
    )
    general_layout.add_dropdown_layout(
        'Cross monitor move behaviour', 
        'Determine what happens when a window is moved across a monitor boundary', 
        ["Swap","Insert","NoOp"],
        config_id="cross_monitor_move_behaviour"
    )
    general_layout.add_options_layout(
        'Workspace padding', 
        'Global default workspace padding', 
        8, 0, 120,
        config_id="default_workspace_padding"
    )
    general_layout.add_options_layout(
        'Container padding', 
        'Global default container padding', 
        8, 0, 120,
        config_id="default_container_padding"
    )
    general_layout.add_checkbox_layout(
        'Mouse follows focus', 
        'Enable or disable mouse follows focus', 
        True,
        config_id="mouse_follows_focus"
    )
     
    return general_layout