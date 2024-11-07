from PyQt6.QtCore import QObject, pyqtSignal
"""
This module defines the SignalManager class which is responsible for managing
various PyQt signals used throughout the application.
Classes:
    SignalManager(QObject): A class that defines several PyQt signals for 
    communication between different parts of the application.
Attributes:
    ignore_rules_updated (pyqtSignal): Signal to emit ignore rules data.
    workspace_monitors_updated (pyqtSignal): Signal to emit workspaces.
    ui_update (pyqtSignal): Signal to emit UI update.
    value_changed (pyqtSignal): Signal to emit value changed.
Instances:
    signal_manager (SignalManager): A global instance of the SignalManager class.
"""

class SignalManager(QObject):
    ignore_rules_updated = pyqtSignal(list)
    manage_rules_updated = pyqtSignal(list)
    floating_applications_updated = pyqtSignal(list)
    layered_applications_updated = pyqtSignal(list)
    workspace_monitors_updated = pyqtSignal(list)
    ui_update = pyqtSignal()
    value_changed = pyqtSignal()

signal_manager = SignalManager()