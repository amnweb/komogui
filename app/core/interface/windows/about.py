from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QPixmap
import os
from datetime import datetime
import subprocess
import re
import requests
from core.utils.settings import BUILD_VERSION, GITHUB_URL, APP_NAME, APP_DESCRIPTION

class VersionChecker(QThread):
    version_checked = pyqtSignal(object, object)
    
    def __init__(self):
        super().__init__()
        self.installed_version = None
        
    def run(self):
        try:
            self.installed_version = self._get_installed_version()
            latest = self.get_latest_version()
            self.version_checked.emit(self.installed_version, latest)
        except Exception as e:
            print(f"Error checking versions: {e}")
    
    def _get_installed_version(self):
        try:        
            result = subprocess.run(['komorebic', '--version'], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            version_line = result.stdout.split('\n')[0]
            version_match = re.search(r'komorebic (\d+\.\d+\.\d+)', version_line)
            if version_match:
                return version_match.group(1)
            return None
        except Exception as e:
            print(f"Error getting version: {e}")
            return None

    def get_latest_version(self):
        try:
            response = requests.get('https://api.github.com/repos/LGUG2Z/komorebi/releases/latest')
            if response.status_code == 200:
                return response.json()['tag_name'].strip('v')
            return None
        except Exception as e:
            print(f"Error fetching latest version: {e}")
            return None

class About(QWidget):
    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout()  # Make layout a class member
        self.description_index = 2  # Store index where description is added
        self.version_checker = VersionChecker()
        self.version_checker.version_checked.connect(self.on_version_checked)
        self.link_label = None
        self.initUI()

    def showEvent(self, event):
        super().showEvent(event)
        if not self.version_checker.isRunning():
            self.version_checker.start()

    def on_version_checked(self, installed, latest):
        if installed:
            current_year = datetime.now().year
            copyright_text = (
                f"Komorebi v{installed}<br>"
                f'{APP_NAME} v{BUILD_VERSION}<br>'
                f"@{current_year} built with ❤️ by "
                f"<a href='https://github.com/amnweb' style='color: #007bff; "
                f"text-decoration: none;'>AmN</a>"
            )
            self.copyright.setTextFormat(Qt.TextFormat.RichText)
            self.copyright.setText(copyright_text)
        
        if installed and latest and installed < latest:
            version_text = f"New Komorebi version {latest} available! Click here to update"
            if self.link_label:
                self.main_layout.removeWidget(self.link_label)
                self.link_label.deleteLater()
            self.link_label = QLabel()
            self.link_label.setText(f"""<a href='https://github.com/LGUG2Z/komorebi/releases/latest' 
                style='color: #007bff; text-decoration: none; font-weight: bold;'>
                {version_text}</a>""")
            self.link_label.setOpenExternalLinks(True)
            self.link_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.link_label.setStyleSheet("""
                QLabel {
                    font-family: Segoe UI;
                    font-size: 14px;
                }
            """)
            self.main_layout.insertWidget(self.description_index + 1, self.link_label)

    def initUI(self):
        self.main_layout.setSpacing(20)
         
        # Setup Widgets (Logo, Title, Description)
        logo_label = QLabel()
        logo_path = os.path.join("app", "assets", "komorebi.png")
        pixmap = QPixmap(logo_path)
        scaled_pixmap = pixmap.scaled(128, 128, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        logo_label.setPixmap(scaled_pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title = QLabel('<span style="font-weight:400;">Komo</span><span style="font-weight:800;">GUI</span>')
        title.setStyleSheet("color: white; font-family: Segoe UI; font-size:48px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        description = QLabel(APP_DESCRIPTION)
        description.setWordWrap(True)
        description.setStyleSheet("color: rgba(255,255,255,0.6);font-weight:normal; font-family: Segoe UI; font-size: 14px;")
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        project_link = QLabel()
        project_link.setText(f"""GitHub Links<br><a href='https://github.com/LGUG2Z/komorebi'>Komorebi</a><br><a href='https://github.com/amnweb/yasb'>YASB Status Bar</a><br><a href='{GITHUB_URL}'>{APP_NAME}</a>""")
        project_link.setOpenExternalLinks(True)
        project_link.setAlignment(Qt.AlignmentFlag.AlignCenter)
        project_link.setStyleSheet("""
            QLabel {
                font-family: Segoe UI;
                font-size: 14px;
                font-weight: 600;
            }
        """)
        
        # Add spacer to push copyright to bottom
        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        
        # Create copyright notice with dynamic year and heart emoji
        current_year = datetime.now().year
        
        copyright_text = (
            f'{APP_NAME} v{BUILD_VERSION}<br>'
            f"@{current_year} built with ❤️ by "
            f"<a href='https://github.com/amnweb' style='color: #007bff; "
            f"text-decoration: none;'>AmN</a>"
        )
 
        self.copyright = QLabel(copyright_text)
        self.copyright.setTextFormat(Qt.TextFormat.RichText)
        self.copyright.setStyleSheet("color: rgba(255,255,255,0.5); font-family: Segoe UI; font-size: 12px;")
        self.copyright.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.copyright.setOpenExternalLinks(True)  # Allow clicking the link
        
        self.main_layout.addWidget(logo_label)
        self.main_layout.addWidget(title)
        self.main_layout.addWidget(description)
        self.main_layout.addWidget(project_link)
        
        self.main_layout.addSpacerItem(spacer)
        self.main_layout.addWidget(self.copyright)
        self.setLayout(self.main_layout)
        
def about_widget():
    about_widget = About()
    return about_widget