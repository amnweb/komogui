from PyQt6.QtWidgets import (QVBoxLayout, QWidget, QPushButton,
                             QHBoxLayout, QFrame, QLabel)
from PyQt6.QtCore import Qt
from core.interface.components.dropdown import DropdownLayout
from core.interface.components.input import InputLayout
from core.interface.styles.styles import Styles
from core.utils.signals import signal_manager

 

class WorkspaceWidget(QWidget):
    def __init__(self, parent=None, number="1", monitor_id="1", count=1):
        super().__init__(parent)
        self.number = number
        self.count = count
        self.monitor_id = monitor_id
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        # Create container
        container = QWidget()
        # container.setObjectName('options_container')
        # container.setStyleSheet(Styles.CONTAINER)

        container_layout = QVBoxLayout()
        container_layout.setContentsMargins(0, 0, 0, 0)

        # Add workspace components with monitor ID
        self.name = InputLayout(
            'Name', 'Workspace name', self.number,
            config_id=f"monitors-{self.monitor_id}.workspace-{self.count}.name"
        )
        self.layout_type = DropdownLayout(
            'Layout', 'Workspace layout type',
            ["BSP", "Columns", "Rows", "VerticalStack",
             "HorizontalStack", "UltrawideVerticalStack",
             "Grid", "RightMainVerticalStack"],
            config_id=f"monitors-{self.monitor_id}.workspace-{self.count}.layout"
        )

        container_layout.addWidget(self.name)
        container_layout.addWidget(self.layout_type)

        # Add remove button with right alignment
        button_container = QWidget()
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)

        self.remove_button = QPushButton("Remove Workspace")
        self.remove_button.setStyleSheet(Styles.BUTTON_ADD)
        button_layout.addStretch()
        button_layout.addWidget(self.remove_button)
        button_container.setLayout(button_layout)

        container_layout.addWidget(button_container)
        container.setLayout(container_layout)
        self.layout.addWidget(container)
        self.setLayout(self.layout)


class MonitorWidget(QWidget):
    def __init__(self, parent=None, monitor_id="1"):
        super().__init__(parent)
        self.monitor_id = monitor_id
        self.workspace_count = 0
        self.initUI()
        self.update_frame_visibility()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Create frame container with background
        self.frame = QFrame()
        self.frame.setObjectName('options_container')
        self.frame.setStyleSheet(Styles.CONTAINER_ALT)
        
        frame_layout = QVBoxLayout(self.frame)

        # Create container for workspaces
        self.workspaces_widget = QWidget()
        self.workspaces_container = QVBoxLayout(self.workspaces_widget)
        self.workspaces_container.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.workspaces_container.setSpacing(5)

        # Add workspace widget to frame
        frame_layout.addWidget(self.workspaces_widget)

        # Add Workspace button
        self.add_button = QPushButton("Add New Workspace")
        self.add_button.setStyleSheet(Styles.BUTTON_ADD)
        self.add_button.clicked.connect(self.add_workspace)

        # Add remove monitor button
        self.remove_button = QPushButton("Remove Monitor")
        self.remove_button.setStyleSheet(Styles.BUTTON_REMOVE)

        # Add widgets to layout
        self.layout.addWidget(self.frame)
        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.remove_button)
        self.setLayout(self.layout)
 

    def add_workspace(self):
        self.workspace_count += 1
        workspace = WorkspaceWidget(self, str(self.workspace_count), self.monitor_id)
        workspace.remove_button.clicked.connect(
            lambda checked, w=workspace: self.remove_workspace(w)
        )
        self.workspaces_container.addWidget(workspace)
        self.update_frame_visibility()
        signal_manager.value_changed.emit()

    def remove_workspace(self, workspace):
        """Remove workspace widget and cleanup"""        
        i = 0
        while i < self.workspaces_container.count():
            widget = self.workspaces_container.itemAt(i).widget()
            if isinstance(widget, WorkspaceWidget):
                #print(f"Checking widget at index {i}: monitor {widget.monitor_id}, workspace {widget.number}")
                
                # Compare monitor_id and workspace number
                if (widget.monitor_id == workspace.monitor_id and 
                    widget.number == workspace.number):
                    #print(f"Found matching workspace at index {i}")
                    # Remove from layout
                    item = self.workspaces_container.takeAt(i)
                    if item:
                        widget = item.widget()
                        if widget:
                            widget.hide()
                            widget.setParent(None)
                            widget.deleteLater()
                            self.workspace_count -= 1
                            self.update_frame_visibility()
                            self.add_button.setFocus()
                            #print(f"Workspace removed. Count now: {self.workspace_count}")
                            return
            i += 1
            signal_manager.value_changed.emit()
            
    def update_frame_visibility(self):
        self.frame.setVisible(self.workspace_count > 0)
 
                
class MonitorLabel(QWidget):
    def __init__(self, number, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 5)
        self.layout.setSpacing(0)

        self.label = QLabel(f"Monitor {number}")
        self.label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 14px;
                font-weight: bold;
            }
        """)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)


class DynamicLayout(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.monitor_count = 0
        self.initUI()
        signal_manager.workspace_monitors_updated.connect(self.handle_monitors)
        
    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)

        self.monitors_widget = QWidget()
        self.monitors_container = QVBoxLayout(self.monitors_widget)
        self.monitors_container.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.monitors_container.setSpacing(10)

        self.add_button = QPushButton("Add New Monitor")
        self.add_button.setStyleSheet(Styles.BUTTON_ADD)
        self.add_button.clicked.connect(self.add_monitor)

        self.layout.addWidget(self.monitors_widget)
        self.layout.addWidget(self.add_button)
        self.setLayout(self.layout)
        
    def handle_monitors(self, monitors):
        """Handle received monitors data"""
        # Clear existing monitors
        while self.monitors_container.count():
            widget = self.monitors_container.takeAt(0).widget()
            if widget:
                widget.deleteLater()
                
        # Add new monitors
        for monitor_idx, monitor_data in enumerate(monitors, 1):
            #print(f"Creating monitor {monitor_idx}")
            monitor = MonitorWidget(monitor_id=str(monitor_idx))
            monitor_label = MonitorLabel(monitor_idx)
            
            # Add widgets to container
            self.monitors_container.addWidget(monitor_label)
            self.monitors_container.addWidget(monitor)
            
            # Store label reference and connect remove button - same as in add_monitor
            monitor.label = monitor_label
            monitor.remove_button.clicked.connect(
                lambda checked, m=monitor, l=monitor_label: self.remove_monitor(m, l)
            )
            
            # Add workspaces for this monitor
            if 'workspaces' in monitor_data:
                for workspace_idx, workspace_data in enumerate(monitor_data['workspaces'], 1):
                    #print(f"Creating workspace {workspace_idx} for monitor {monitor_idx}")
                    workspace = WorkspaceWidget(
                        parent=monitor,
                        number=workspace_data.get('name', str(workspace_idx)),
                        monitor_id=str(monitor_idx),
                        count=workspace_idx
                    )
                    
                    if 'name' in workspace_data:
                        workspace.name.set_value(workspace_data['name'])
                    if 'layout' in workspace_data:
                        workspace.layout_type.set_value(workspace_data['layout'])
                    
                    # Ensure workspace is added to correct monitor's container
                    monitor.workspaces_container.addWidget(workspace)
                    
                    # Connect remove button with explicit monitor reference
                    workspace.remove_button.clicked.connect(
                        lambda checked, w=workspace, m=monitor: m.remove_workspace(w)
                    )
                    
                    monitor.workspace_count += 1
                    #print(f"Added workspace to monitor {monitor_idx}, count: {monitor.workspace_count}")
                    
                monitor.update_frame_visibility()
 
            
        self.monitor_count = len(monitors)
        
    def add_monitor(self):
        self.monitor_count += 1
        monitor = MonitorWidget(monitor_id=str(self.monitor_count))
        monitor_label = MonitorLabel(self.monitor_count)

        self.monitors_container.addWidget(monitor_label)
        self.monitors_container.addWidget(monitor)

        monitor.label = monitor_label
        monitor.remove_button.clicked.connect(
            lambda checked, m=monitor, l=monitor_label: self.remove_monitor(m, l)
        )

    def remove_monitor(self, monitor, label):
        """Remove monitor and its label from container"""
        #print(f"Removing monitor {monitor.monitor_id}")
        
        # Find indices to remove
        indices_to_remove = []
        for i in range(self.monitors_container.count()):
            widget = self.monitors_container.itemAt(i).widget()
            if widget == monitor or widget == label:
                indices_to_remove.append(i)
                
        # Remove widgets in reverse order to maintain indices
        for i in reversed(indices_to_remove):
            item = self.monitors_container.takeAt(i)
            if item:
                widget = item.widget()
                if widget:
                    widget.hide()
                    widget.setParent(None)
                    widget.deleteLater()
        
        self.monitor_count -= 1
        #print(f"Monitor removed. Count now: {self.monitor_count}")


def workspace_widget():
    return DynamicLayout()