from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QPushButton
from PyQt6.QtCore import Qt
from core.interface.components.dropdown import DropdownLayout
from core.interface.components.input import InputLayout
from core.interface.styles.styles import Styles
from core.utils.signals import signal_manager
 

class RuleWidget(QWidget):
    def __init__(self, index, parent=None):
        super().__init__(parent)
        self.index = index
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        
        # Create container
        container = QWidget()
        container.setObjectName('options_container')
        container.setStyleSheet(Styles.CONTAINER_ALT)
        
        container_layout = QVBoxLayout()
        container_layout.setContentsMargins(10, 10, 10, 10)
        
        # Add rule components
        self.kind = DropdownLayout('Kind', 'Individual window force-manage rules', 
                                 ["Exe","Class","Title","Path"], 
                                 config_id=f"manage_rules-{self.index}.kind")
        self.strategy = DropdownLayout('Matching strategy', 'Individual window matching rules',
                                     ['Legacy','Equals','StartsWith','EndsWith','Contains','Regex','DoesNotEndWith','DoesNotStartWith','DoesNotEqual','DoesNotContain'], 
                                     config_id=f"manage_rules-{self.index}.matching_strategy")
        self.identifier = InputLayout('ID', 'Identifier as a string', "",
                                    config_id=f"manage_rules-{self.index}.id")
        
        container_layout.addWidget(self.kind)
        container_layout.addWidget(self.strategy)
        container_layout.addWidget(self.identifier)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.remove_button = QPushButton("Remove Rule")
        self.remove_button.setStyleSheet(Styles.BUTTON_ADD)
        button_layout.addWidget(self.remove_button)
        container_layout.addLayout(button_layout)
        container.setLayout(container_layout)
        self.layout.addWidget(container)
        self.setLayout(self.layout)

class DynamicLayout(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._initialized = False
        self.rule_count = 0
        
        # Initialize layout once
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)
        
        # Create container widget for rules
        self.rules_widget = QWidget()
        self.rules_container = QVBoxLayout(self.rules_widget)
        self.rules_container.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.rules_container.setSpacing(5)
        
        # Add Rule button
        self.add_button = QPushButton("Add New Rule")
        self.add_button.setStyleSheet(Styles.BUTTON_ADD)
        self.add_button.clicked.connect(self.add_rule)
        
        # Add widgets to main layout
        self.layout.addWidget(self.rules_widget)
        self.layout.addWidget(self.add_button)
        
        # Set layout once
        self.setLayout(self.layout)
        
        # Connect signal
        signal_manager.manage_rules_updated.connect(self.handle_manage_rules)
        self._initialized = True

    def showEvent(self, event):
        super().showEvent(event)
        
    def handle_manage_rules(self, rules):
        """Handle received ignore rules data"""
        # Clear existing rules
        while self.rules_container.count():
            widget = self.rules_container.takeAt(0).widget()
            if widget:
                widget.deleteLater()
        
        self.rule_count = 0  # Reset counter
        
        # Add new rules
        for rule_data in rules:
            self.rule_count += 1
            rule = RuleWidget(self.rule_count, self)
            if isinstance(rule_data, dict):
                if 'kind' in rule_data:
                    rule.kind.set_value(rule_data['kind'])
                if 'matching_strategy' in rule_data:
                    rule.strategy.set_value(rule_data['matching_strategy'])
                if 'id' in rule_data:
                    rule.identifier.set_value(rule_data['id'])
            
            def create_remove_callback(r):
                return lambda: self.remove_rule(r)
            
            rule.remove_button.clicked.connect(create_remove_callback(rule))
            self.rules_container.addWidget(rule)
                
    def add_rule(self):   
        self.rule_count += 1
        rule = RuleWidget(self.rule_count, self)
        rule.remove_button.clicked.connect(lambda: self.remove_rule(rule))
        self.rules_container.addWidget(rule)
        signal_manager.value_changed.emit()

    def remove_rule(self, rule):
        self.rules_container.removeWidget(rule)
        rule.deleteLater()
        signal_manager.value_changed.emit()
 
def manage_rules_widget():
    return DynamicLayout()