from PyQt6.QtWidgets import QVBoxLayout, QWidget, QLabel, QPushButton, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt
from core.interface.styles.styles import Styles
from core.utils.utils import Dialogs
from core.utils.signals import signal_manager

class Sidebar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_config_path = None 
        self.sidebar_items_enabled = False 
        self.dialogs = Dialogs()
        self.initUI()
        self.load_btn.clicked.connect(self.dialogs.open_file_dialog)
        self.save_btn.clicked.connect(lambda: self.dialogs.save_file_dialog(self.parent().stacked_widget, self.parent().widget_factories))
        self.about_btn.clicked.connect(self.load_about_page)
        self.set_sidebar_items_enabled(False)
        
        signal_manager.value_changed.connect(self._value_changed)
        
    def _value_changed(self):
        self.save_btn.setStyleSheet(Styles.BUTTON_UNSAVED)
        
    def initUI(self):
        self.setFixedWidth(160)

        # Create the sidebar layout
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setSpacing(6)
        sidebar_layout.setContentsMargins(6, 6, 6, 6)
        sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

       # Options for the sidebar
        options = ['General','Animation', 'Borders', 'Stackbar', 'Transparency', 'Ignore Rules','Workspaces']
        self.labels = []
        for index, file_name in enumerate(options):
            label = QLabel(file_name)
            label.setStyleSheet(Styles.SIDEBAR_BUTTON)
            label.setCursor(Qt.CursorShape.PointingHandCursor)
            label.mousePressEvent = lambda event, idx=index+1, lbl=label: self.parent().on_sidebar_label_click(idx, lbl)
            sidebar_layout.addWidget(label)
            self.labels.append(label)

        # Add vertical spacer to push buttons to bottom
        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sidebar_layout.addItem(spacer)

        # Create and style the buttons
        self.load_btn = QPushButton("Load Config")
        self.save_btn = QPushButton("Save Config")
        self.about_btn = QPushButton("About")

        self.load_btn.setStyleSheet(Styles.BUTTON_ADD)
        self.save_btn.setStyleSheet(Styles.BUTTON_ADD)
        self.about_btn.setStyleSheet(Styles.BUTTON_ADD)
        
        self.load_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.about_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.save_btn.clicked.connect(self.on_button_click)
        
        # Add buttons at the bottom
        sidebar_layout.addWidget(self.load_btn)
        sidebar_layout.addWidget(self.save_btn)
        sidebar_layout.addWidget(self.about_btn)

        self.setLayout(sidebar_layout)
        
    def on_button_click(self):
        self.save_btn.setStyleSheet(Styles.BUTTON_ADD)
            
    def clear_active_background(self):
        if not self.sidebar_items_enabled:
            return
        for label in self.labels:
            label.setStyleSheet(Styles.SIDEBAR_BUTTON)
        
    def load_about_page(self):
        self.clear_active_background()
        index = 8  # Use a unique index for the "About" button
        self.parent().on_sidebar_label_click(index, None)

    def set_sidebar_items_enabled(self, enabled):
        self.sidebar_items_enabled = enabled
        for label in self.labels:
            label.setEnabled(enabled)
            label.setStyleSheet(Styles.SIDEBAR_BUTTON if enabled else Styles.SIDEBAR_BUTTON_DISABLED)
        self.save_btn.setEnabled(enabled)