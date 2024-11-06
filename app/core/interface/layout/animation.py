# core/options/animation.py
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
        
def animation_widget():
    animation_layout = DynamicLayout()
    animation_layout.add_checkbox_layout(
        'Enable Animation',
        'Enable or disable the animation',
        True,
        config_id="animation.enabled"
    )
    animation_layout.add_options_layout(
        'Animation Duration',
        'Duration of the animation in milliseconds',
        400,
        0,
        2000,
        config_id="animation.duration"
    )
    animation_layout.add_dropdown_layout(
        'Animation Style',
        'Style of the animation',
        ['Linear','EaseInSine','EaseOutSine','EaseInOutSine','EaseInQuad','EaseOutQuad','EaseInOutQuad','EaseInCubic','EaseInOutCubic','EaseInQuart','EaseOutQuart','EaseInOutQuart','EaseInQuint','EaseOutQuint','EaseInOutQuint','EaseInExpo','EaseOutExpo','EaseInOutExpo','EaseInCirc','EaseOutCirc','EaseInOutCirc','EaseInBack','EaseOutBack','EaseInOutBack','EaseInElastic','EaseOutElastic','EaseInOutElastic','EaseInBounce','EaseOutBounce','EaseInOutBounce'],
        config_id="animation.style"
    )
    animation_layout.add_options_layout(
        'Animation FPS',
        'Frames per second for the animation',
        60,
        60,
        240,
        config_id="animation.fps"
    )
    return animation_layout