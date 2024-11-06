from PyQt6.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QWidget, QStackedWidget, QScrollArea
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from core.interface.layout.animation import animation_widget
from core.interface.layout.border import border_widget
from core.interface.layout.transparency import transparency_widget
from core.interface.layout.general import general_widget
from core.interface.layout.stackbar import stackbar_widget
from core.interface.components.ignore_rules import ignore_rules_widget
from core.interface.components.workspace import workspace_widget
from core.interface.windows.about import about_widget
from core.interface.components.sidebar import Sidebar
from core.utils.utils import create_content_widget, display_content
from core.utils.window_effects import ApplyMica
from core.interface.styles.styles import Styles
from core.interface.windows.home import Home
from core.utils.signals import signal_manager
from core.utils.settings import APP_NAME

class ScrollWrapper(QWidget):
    def __init__(self, widget):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setWidget(widget)
        scroll.setStyleSheet(Styles.SCROLL_AREA)

        layout.addWidget(scroll)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        signal_manager.ui_update.connect(self.on_config_loaded)

        self.active_label = None

        self.initUI()

    def get_or_create_widget(self, title, factory):
        return create_content_widget(title, factory())

    def initUI(self):
        self.setWindowTitle(APP_NAME)
        self.setWindowIcon(QIcon('app/assets/komorebi.ico'))
        self.setMinimumSize(880, 720)

        main_layout = QHBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.sidebar = Sidebar(self)
        main_layout.addWidget(self.sidebar)

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setContentsMargins(0, 0, 0, 0)

        self.widget_factories = [
            ('', lambda: Home()),
            ('General Configuration', general_widget),
            ('Animations Configuration', animation_widget),
            ('Border Configuration', border_widget),
            ('Stackbar Configuration', stackbar_widget),
            ('Transparency Configuration', transparency_widget),
            ('Ignore Rules Configuration', ignore_rules_widget),
            ('Workspaces Configuration', workspace_widget),
            ('', about_widget)
        ]

        # Add wrapped widgets
        for title, factory in self.widget_factories:
            widget = self.get_or_create_widget(title, factory)
            wrapped = ScrollWrapper(widget)
            self.stacked_widget.addWidget(wrapped)

        main_layout.addWidget(self.stacked_widget)
        self.setLayout(main_layout)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        ApplyMica(self.winId())

    def on_config_loaded(self):
        index = 1
        label = self.sidebar.labels[index - 1]
        self.on_sidebar_label_click(index, label)
        self.sidebar.set_sidebar_items_enabled(True)

    def on_sidebar_label_click(self, index, label):
        self.stacked_widget.setCurrentIndex(index)
        self.active_label = display_content(
            self.stacked_widget, index, label, self.active_label)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())