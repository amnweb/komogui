from PyQt6.QtWidgets import QVBoxLayout, QWidget, QLabel, QPushButton, QSpacerItem, QSizePolicy, QHBoxLayout
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt6.QtGui import QTransform, QPainter, QPixmap
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
        self.setFixedWidth(180)

        # Create the sidebar layout
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setSpacing(6)
        sidebar_layout.setContentsMargins(6, 6, 6, 6)
        sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

       # Options for the sidebar
        options = ['General','Animation', 'Borders', 'Stackbar', 'Transparency', 'Workspaces']
        self.labels = []
        for index, file_name in enumerate(options):
            label = QLabel(file_name)
            label.setStyleSheet(Styles.SIDEBAR_BUTTON)
            label.setCursor(Qt.CursorShape.PointingHandCursor)
            label.mousePressEvent = lambda event, idx=index+1, lbl=label: self.parent().on_sidebar_label_click(idx, lbl)
            sidebar_layout.addWidget(label)
            self.labels.append(label)

        # In your Sidebar.__init__ method, after creating other labels:
        self.rules_dropdown = RulesDropdown(self)
        sidebar_layout.addWidget(self.rules_dropdown)

        # Add rules items to your labels list for consistent styling
        self.labels.extend(self.rules_dropdown.rules_items)

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
        index = 11  # Use a unique index for the "About" button
        self.parent().on_sidebar_label_click(index, None)

    def set_sidebar_items_enabled(self, enabled):
        self.sidebar_items_enabled = enabled
        for label in self.labels:
            label.setEnabled(enabled)
            label.setStyleSheet(Styles.SIDEBAR_BUTTON if enabled else Styles.SIDEBAR_BUTTON_DISABLED)
        self.rules_dropdown.header_text.setEnabled(enabled)
        self.rules_dropdown.header_text.setStyleSheet(Styles.SIDEBAR_BUTTON if enabled else Styles.SIDEBAR_BUTTON_DISABLED)
        self.rules_dropdown.header_arrow.setStyleSheet(Styles.SIDEBAR_BUTTON if enabled else Styles.SIDEBAR_BUTTON_DISABLED)
        self.save_btn.setEnabled(enabled)

class ArrowLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._rotation = 0
        self.opacity = 0.5
        self.pixmap = QPixmap("app/assets/chevron.png")
        # Scale the pixmap if needed
        self.pixmap = self.pixmap.scaled(8, 8, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        
    def _set_rotation(self, angle):
        self._rotation = angle
        self.update()
        
    def _get_rotation(self):
        return self._rotation
        
    rotation = pyqtProperty(float, _get_rotation, _set_rotation)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setOpacity(self.opacity)
        # Calculate center point
        center = self.rect().center()
        
        # Translate to center, rotate, translate back
        painter.translate(center)
        painter.rotate(self._rotation)
        painter.translate(-center)
        
        # Draw the pixmap centered
        x = (self.width() - self.pixmap.width()) // 2
        y = (self.height() - self.pixmap.height()) // 2
        painter.drawPixmap(x, y, self.pixmap)

class RulesDropdown(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        
        # Create header container
        header_container = QWidget()
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create text and arrow labels
        self.header_text = QLabel("Rules")
        self.header_arrow = ArrowLabel()
        
        # Style both labels
        self.header_text.setStyleSheet(Styles.SIDEBAR_BUTTON)
 
        
        # Add to horizontal layout
        header_layout.addWidget(self.header_text)
        header_layout.addStretch()  # This pushes the arrow to the right
        header_layout.addWidget(self.header_arrow)
        
        header_container.setLayout(header_layout)
        header_container.setCursor(Qt.CursorShape.PointingHandCursor)
        header_container.mousePressEvent = self.toggle_dropdown
        
        self.layout.addWidget(header_container)
        
        # Setup animation
        self.animation = QPropertyAnimation(self.header_arrow, b"rotation")
        self.animation.setDuration(200) 
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        
        self.is_expanded = False
        # Rest of your existing initialization code...

        # Create rule items with their corresponding indices and using tabs for indentation instead of complicated with css and classes
        rules_config = [
            ("  Ignore Rules", 7),
            ("  Force Manage Rules", 8),
            ("  Floating Apps", 9),
            ("  Layered Apps", 10)
        ]
        
        self.rules_items = []
        for text, index in rules_config:
            label = QLabel(text)
            label.setCursor(Qt.CursorShape.PointingHandCursor)
            # Store the index and connect click event
            label.index = index
            label.mousePressEvent = lambda e, lbl=label: self.on_rule_clicked(lbl)
            self.rules_items.append(label)
        
        # Hide items initially
        self.is_expanded = False
        for item in self.rules_items:
            self.layout.addWidget(item)
            item.hide()
            
        self.setLayout(self.layout)
    
    def toggle_dropdown(self, event):
        self.is_expanded = not self.is_expanded
        
        # Animate rotation
        self.animation.setStartValue(0 if self.is_expanded else 90)
        self.animation.setEndValue(90 if self.is_expanded else 0)
        self.animation.start()
        
        for item in self.rules_items:
            item.setVisible(self.is_expanded)
    
    def on_rule_clicked(self, label):
        # Call parent's sidebar label click handler with the rule's index
        self.parent().parent().on_sidebar_label_click(label.index, label)