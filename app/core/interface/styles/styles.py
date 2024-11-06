class Styles:
    CONTAINER = '''
        QWidget#options_container { 
            background-color: rgba(255, 255, 255, 0.04);
            border-radius: 6px; 
            padding: 0px; 
            border: 1px solid rgba(0,0,0,0.2);
        }
    '''
    CONTAINER_ALT = '''
        QWidget#options_container { 
            background-color: rgba(255, 255, 255, 0.02);
            border-radius: 6px; 
            padding: 0px; 
            border: 1px solid rgba(0,0,0,0.2);
        }
    '''
    LABEL_TITLE = '''
        color: rgba(255,255,255,0.9); 
        font-size: 14px; 
        font-family: Segoe UI;
        font-weight: 600; 
        padding-top: 14px;
        padding-left: 0;
    '''

    LABEL_DESCRIPTION = '''
        color: rgba(255,255,255,0.6);
        font-size: 12px; 
        padding-bottom:12px;
        font-family: Segoe UI;
        font-weight: 600;
        padding-left: 1px; 
        margin-left: 0;
    '''
    INPUT_FIELD = '''
        QLineEdit {
            background-color: rgba(255,255,255,0.04); 
            color: rgba(255,255,255,0.9);
            font-size: 14px;
            font-weight: 600;
            font-family: Segoe UI;
            padding: 4px;
            border: none;
            border-radius: 4px;
            border: 2px solid transparent;
        }
        QLineEdit:focus {
            background-color: #222;
            border-bottom: 2px solid #0078d7;
        }
    '''
    BUTTON_ROUNDED = '''
        QPushButton {
            border-radius: 15px;
            padding: 0px;
            margin: 0px;
            background-color: rgba(255, 255, 255, 0.04);
            color:rgba(255, 255, 255, 0.8);
            font-size: 18px;
            font-family: Consolas;
            font-weight: bold;
            margin-left: 4px;
        }
        QPushButton:hover {
            background-color: rgba(255, 255, 255, 0.08);
        }
        QPushButton:pressed {
            background-color: rgba(255, 255, 255, 0.06);
        }
    '''
    BUTTON_ADD = '''
        QPushButton {
            background-color: rgba(255, 255, 255, 0.04);
            color: white;
            padding: 6px 24px;
            border-radius: 6px;
            font-family: "Segoe UI";
            font-size: 13px;
            font-weight: 600;
        }
        QPushButton:hover {
            background-color: rgba(255, 255, 255, 0.08);
        }
        QPushButton:pressed {
            background-color: rgba(255, 255, 255, 0.06);
 
        }
    '''
    BUTTON_REMOVE = '''
        QPushButton {
            background-color: rgba(209, 64, 69, 0.2);
            color: rgb(209, 64, 69);
            padding: 4px 16px;
            border-radius: 6px;
            font-family: "Segoe UI";
            font-size: 13px;
            font-weight: 600;
        }
        QPushButton:hover {
            background-color: rgba(209, 64, 69, 0.15);
 
        }
        QPushButton:pressed {
            background-color: rgba(209, 64, 69, 0.08);
 
        }
    '''
    BUTTON_UNSAVED = '''
        QPushButton {
            background-color: rgba(245, 52, 55, 0.6);
            color: white;
            padding: 6px 24px;
            border-radius: 6px;
            font-family: "Segoe UI";
            font-size: 13px;
            font-weight: 600;
        }
        QPushButton:hover {
            background-color: rgba(245, 52, 55, 0.7);
        }
        QPushButton:pressed {
            background-color: rgba(245, 52, 55, 0.4);
        }
    '''
    DROPDOWN = '''
        QComboBox {
            combobox-popup: 0;
            background-color:rgba(255,255,255,0.06);
            color:rgba(255,255,255,0.9);
            font-size: 13px;
            font-family: Segoe UI;
            font-weight: 600;
            padding: 4px 8px;
            border: none;
            border-radius: 4px;
        }
        QComboBox:on {
            background-color: #353439; 
        }
        QComboBox::drop-down {
            border: none;
        }
        QComboBox::down-arrow {
            image: url(noimg);
        }
        QComboBox QAbstractItemView {
            background-color: #353439;
            color: white;
            font-size: 13px;
            font-family: Segoe UI;
            selection-background-color: #404653;
            border: none;
            padding:2px;
            margin: 0px;
            outline: none;
        }
        QComboBox QAbstractItemView::item {
            padding: 8px 0;
        }
        QComboBox QScrollBar:vertical {
            width: 4px;
            background: transparent;
        }
        QComboBox QScrollBar::handle:vertical {
            background: rgba(255,255,255,0.2);
            border-radius: 2px;
            min-height: 10px;
        }
        QComboBox QScrollBar::add-line:vertical,
        QComboBox QScrollBar::sub-line:vertical {
            height: 0px;
        }
        QComboBox QScrollBar::add-page:vertical,
        QComboBox QScrollBar::sub-page:vertical {
            background: transparent;
        }
    '''
    SCROLL_AREA = '''
        QScrollArea {
            background: transparent;
            border: none;
        }
        QScrollArea > QWidget {
            background:transparent
        }
        QScrollArea > QWidget > QWidget {
            border-left: 1px solid #333;
        }
        QScrollBar:vertical {
            background:rgba(255,255,255,0);
            width: 6px;
            margin: 0;
            border:none;
        }
        QScrollBar::handle:vertical {
            background: rgba(255,255,255,0.1);
            min-height: 20px;
            border-radius: 3px;
        }
        QScrollBar::add-line:vertical, 
        QScrollBar::sub-line:vertical {
            height: 0px;
            background: none;
        }
        QScrollBar::add-page:vertical,
        QScrollBar::sub-page:vertical {
            background: none;
        }
    '''
    SIDEBAR_BUTTON = '''
        QLabel { 
            color: rgba(255,255,255,0.95);
            font-size: 14px;
            font-family:Segoe UI;
            font-weight:600;
            padding:10px 6px 10px 16px;
            border-radius: 6px; 
            border: 1px solid rgba(0,0,0,0);
        }
    '''
    SIDEBAR_BUTTON_ACTIVE = '''
        QLabel { 
            background-color: rgba(255, 255, 255, 0.06);
            color: rgba(255,255,255,1);
            font-size: 14px;
            font-family:Segoe UI;
            font-weight:600;
            padding:10px 6px 10px 16px;
            border-radius: 6px; 
            border: 1px solid rgba(0,0,0,0.2);
        }
    '''
    SIDEBAR_BUTTON_DISABLED = '''
        QLabel { 
            color: rgba(255,255,255,0.4);
            font-size: 14px;
            font-family:Segoe UI;
            font-weight:600;
            padding:10px 6px 10px 16px;
            border-radius: 6px; 
            border: 1px solid rgba(0,0,0,0);
        }
    '''
    CHECKBOX = '''
        QCheckBox {
            spacing: 5px;
        }
        QCheckBox::indicator {
            width: 18px;
            height: 18px;
            border-radius: 3px;
            border: 1px solid #7D7D7D;
            background-color: transparent;
        }
        QCheckBox::indicator:hover {
            border: 1px solid #0078D4;
        }
        QCheckBox::indicator:checked {
            background-color: #0078D4;
            border: 1px solid #0078D4;
            image: url(./app/assets/checkmark.png);
        }
        QCheckBox::indicator:checked:hover {
            background-color: #429CE3;
            border: 1px solid #429CE3;
        }
        QCheckBox::indicator:disabled {
            border: 1px solid #C4C4C4;
            background-color: #F0F0F0;
        }
        QCheckBox::indicator:checked:disabled {
            background-color: #C4C4C4;
            border: 1px solid #C4C4C4;
        }
    '''
