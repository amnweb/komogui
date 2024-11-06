# utils.py
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QLabel, QFileDialog, QApplication, QMessageBox
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
import json
from core.utils.signals import signal_manager
from core.interface.styles.styles import Styles
from collections import OrderedDict

def create_content_widget(title, widget):
    content = QWidget()
    layout = QVBoxLayout()
    layout.setSpacing(0)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setAlignment(Qt.AlignmentFlag.AlignTop)
    name_label = QLabel(title)
    name_label.setStyleSheet('color:rgba(255,255,255,1); font-size: 20px; font-family: Segoe UI; font-weight: 600; padding:20px 0 10px 10px')
    layout.addWidget(name_label)
    layout.addWidget(widget)
    content.setLayout(layout)
    return content

def display_content(stacked_widget, index, label, active_label):
    # Change to current widget
    stacked_widget.setCurrentIndex(index)
    # Only handle label styling if a label is provided
    if label is not None:
        # Reset previous active label style if it exists
        if active_label is not None:
            active_label.setStyleSheet(Styles.SIDEBAR_BUTTON)
        # Set new label style
        label.setStyleSheet(Styles.SIDEBAR_BUTTON_ACTIVE)
        return label
    
    return active_label


def get_all_config_ids(parent_widget):
    config_ids = {}
    all_widgets = parent_widget.findChildren(QWidget, options=Qt.FindChildOption.FindChildrenRecursively)
    
    for child in all_widgets:
        if hasattr(child, 'config_id') and child.config_id:
            config_id = child.config_id
            if config_id not in config_ids:
                config_ids[config_id] = []
            config_ids[config_id].append(child)
    return config_ids


def get_widget_value(widget):
    value = widget.get_value()
    return value       

 
'''
Fucntion related to generating configuration data for json file.
Probably this can be better implemented.
'''
def process_monitor_config(config_id, value):
    parts = config_id.split('.')
    monitor_num = int(parts[0].split('-')[1])
    workspace_num = int(parts[1].split('-')[1])
    property_name = parts[2]
    return monitor_num, workspace_num, property_name

def process_ignore_rule(config_id, value):
    parts = config_id.split('.')
    rule_num = int(parts[0].split('-')[1])
    property_name = parts[1]
    return rule_num, property_name

def convert_value(value):
    str_value = str(value).lower()
    if str_value == "true":
        return True
    if str_value == "false":
        return False
    try:
        return int(value)
    except (ValueError, TypeError):
        return value

def generate_config(parent_widget, widget_factories):
    monitors = {}
    ignore_rules_map = {}
    other_configs = {}
    
    # Process all widgets and collect configs
    for widget in QApplication.instance().allWidgets():
        if not (hasattr(widget, 'config_id') and widget.config_id and hasattr(widget, 'get_value')):
            continue
            
        config_id = widget.config_id
        value = widget.get_value()
        
        try:
            if config_id.startswith('monitors-'):
                monitor_num, workspace_num, property_name = process_monitor_config(config_id, value)
                monitors.setdefault(monitor_num, {"workspaces": {}})
                monitors[monitor_num]["workspaces"].setdefault(workspace_num, {})
                monitors[monitor_num]["workspaces"][workspace_num][property_name] = str(value)
                
            elif config_id.startswith('ignore_rules-'):
                rule_num, property_name = process_ignore_rule(config_id, value)
                ignore_rules_map.setdefault(rule_num, {})
                ignore_rules_map[rule_num][property_name] = value
                
            else:
                current = other_configs
                parts = config_id.split('.')
                for part in parts[:-1]:
                    current = current.setdefault(part, {})
                current[parts[-1]] = convert_value(value)
                
        except (IndexError, ValueError) as e:
            print(f"Error processing config_id {config_id}: {e}")
            continue

    # Build final config with ordered sections
    final_config = OrderedDict([
        ("$schema", "https://raw.githubusercontent.com/LGUG2Z/komorebi/master/schema.json"),
        ("app_specific_configuration_path", "$Env:USERPROFILE/.config/applications.json")
    ])
    
    # Sort and add other configs
    sorted_configs = OrderedDict(sorted(other_configs.items(), key=lambda x: x[0]))
    final_config.update(sorted_configs)
    
    # Add monitors with sorted workspaces
    if monitors:
        monitor_list = []
        for monitor_id in sorted(monitors.keys()):
            workspace_list = []
            for workspace_id in sorted(monitors[monitor_id]["workspaces"].keys()):
                workspace = monitors[monitor_id]["workspaces"][workspace_id]
                if "name" in workspace and "layout" in workspace:
                    workspace_list.append({
                        "name": workspace["name"],
                        "layout": workspace["layout"]
                    })
            if workspace_list:
                monitor_list.append({"workspaces": workspace_list})
        final_config["monitors"] = monitor_list
    
    # Add sorted ignore rules
    if ignore_rules_map:
        rules_list = []
        for rule_id in sorted(ignore_rules_map.keys()):
            rule = ignore_rules_map[rule_id]
            if all(key in rule for key in ['kind', 'matching_strategy', 'id']):
                rules_list.append({
                    'kind': rule['kind'],
                    'matching_strategy': rule['matching_strategy'],
                    'id': rule['id']
                })
        final_config["ignore_rules"] = rules_list
        
    return final_config


 
        
class Dialogs():
    def __init__(self):
        self.config_path = None  

    def open_file_dialog(self):
        """Opens file dialog for JSON files and returns selected file path"""
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("JSON files (*.json)")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                self.config_path = selected_files[0]
 
                try:
                    with open(self.config_path, 'r') as file:
                        self.config_data = json.load(file)
                    self.update_widgets()
                    signal_manager.ui_update.emit()
                    return selected_files[0]
                except Exception as e:
                    error_dialog = QMessageBox()
                    error_dialog.setIcon(QMessageBox.Icon.Critical)
                    error_dialog.setWindowIcon(QIcon('app/assets/komorebi.ico'))
                    error_dialog.setWindowTitle("Error")
                    error_dialog.setText("Error loading file")
                    error_dialog.setInformativeText(str(e))
                    error_dialog.exec()
        return None
    
    

    def save_file_dialog(self, parent_widget, widget_factories, show_dialog=False):
        try:
            # Generate config first
            config = generate_config(parent_widget, widget_factories)

            if show_dialog:
                # Create file dialog
                file_dialog = QFileDialog()
                file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
                file_dialog.setNameFilter("JSON files (*.json)")
                file_dialog.setDefaultSuffix("json")
                
                if file_dialog.exec():
                    file_path = file_dialog.selectedFiles()[0]
                else:
                    return None
            else:
                # Use existing path or default
                if hasattr(self, 'config_path') and self.config_path:
                    file_path = self.config_path
                else:
                    # No existing path - force dialog
                    return self.save_file_dialog(parent_widget, widget_factories, True)
            
            # Save config to path
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
                
            # Store path for future saves
            self.config_path = file_path
            return file_path
                
        except Exception as e:
            error_dialog = QMessageBox()
            error_dialog.setIcon(QMessageBox.Icon.Critical)
            error_dialog.setWindowIcon(QIcon('core/assets/komorebi.ico'))
            error_dialog.setWindowTitle("Error")
            error_dialog.setText("Error saving configuration")
            error_dialog.setInformativeText(str(e))
            error_dialog.exec()
            return None
    
 
                    
                    
    def get_config_value(self, config_id):
        """Get the value from the configuration data based on the config_id"""
        if not self.config_data:
            return None
        value = self.config_data
        keys = config_id.split('.')
        
        try:
            for key in keys:
                if isinstance(value, dict):
                    value = value.get(key)
                elif isinstance(value, list) and key.isdigit():
                    value = value[int(key)]
                else:
                    return None
                    
                if value is None:
                    return None
        except (KeyError, IndexError, ValueError):
            return None
            
        return value


    def set_widget_value(self, widget, value):
        """Set the value of the widget based on its type and the value format"""
        if hasattr(widget, 'dropdown'):
            widget.set_value(str(value))
        else:
            widget.set_value(value)

    def update_widgets(self):
        """Update widgets based on the loaded configuration"""
        if not self.config_data:
            print("No configuration data found")
            return

        # Handle ignore rules with indexed config IDs
        if 'ignore_rules' in self.config_data:
            ignore_rules = self.config_data['ignore_rules']
            if isinstance(ignore_rules, list):
                # Transform rules to include index
                indexed_rules = []
                for idx, rule in enumerate(ignore_rules, 1):
                    indexed_rule = {
                        'kind': rule.get('kind'),
                        'matching_strategy': rule.get('matching_strategy'),
                        'id': rule.get('id'),
                        'config_id_prefix': f'ignore_rules-{idx}'
                    }
                    indexed_rules.append(indexed_rule)
                signal_manager.ignore_rules_updated.emit(indexed_rules)

        # Handle workspaces
        if 'monitors' in self.config_data:
            monitors = self.config_data['monitors']
            if isinstance(monitors, list):
                signal_manager.workspace_monitors_updated.emit(monitors)

        # Update other widgets
        all_widgets = QApplication.instance().allWidgets()
        for widget in all_widgets:
            if hasattr(widget, 'config_id') and widget.config_id:
                # Skip special widgets with numbered rules
                if not (widget.config_id.split('.')[0].startswith('ignore_rules-') or 
                    widget.config_id.startswith('monitors')):
                    value = self.get_config_value(widget.config_id)
                    if value is not None:
                        self.set_widget_value(widget, value)