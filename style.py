from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt, QSize

class Style:
    def __init__(self, widget):
        self.widget = widget
    
    def apply_style(self):
        # Light grey-white palette
        palette = self.widget.palette()
        palette.setColor(QPalette.Window, QColor(255,255,255))
        palette.setColor(QPalette.WindowText, QColor(60, 60, 60))
        palette.setColor(QPalette.Base, QColor(255, 255, 255))
        palette.setColor(QPalette.AlternateBase, QColor(240, 240, 240))
        palette.setColor(QPalette.Button, QColor(245, 245, 245))
        palette.setColor(QPalette.ButtonText, QColor(80, 80, 80))
        palette.setColor(QPalette.Highlight, QColor(100, 149, 237))  # Soft blue
        palette.setColor(QPalette.HighlightedText, Qt.white)
        self.widget.setPalette(palette)

        # Cover Art style
        # self.widget.cover_art.setStyleSheet("""
        #     QLabel {
        #         background-color: rgb(230, 230, 230);
        #         border: 2px solid white;
        #         border-radius: 8px;
        #     }
        # """)

        # Playlist style
        self.widget.playlist.setStyleSheet("""
            QListWidget {
                background-color: white;
                color: #505050;
                border: 1px solid #e0e0e0;
                font-size: 14px;
                border-radius: 8px;
            }
            QListWidget::item {
                padding: 10px 15px;
                border-bottom: 1px solid #f0f0f0;
            }
            QListWidget::item:hover {
                background-color: #f8f8f8;
            }
            QListWidget::item:selected {
                background-color: rgb(100, 149, 237);
                color: white;
                border-radius: 4px;
            }
        """)

        # Action buttons (Add)
        self.widget.add_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 0.05);
            }
            QPushButton:pressed {
                background-color: rgba(0, 0, 0, 0.1);
            }
        """)
        self.widget.add_button.setIconSize(QSize(22, 22))  # Using QSize object

        # Playback mode buttons (Repeat/Shuffle)
        mode_style = """
            QPushButton {
                background-color: transparent;
                border: none;
                padding: 8px;
                border-radius: 16px;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 0.05);
            }
            QPushButton:pressed {
                background-color: rgba(0, 0, 0, 0.1);
            }
            QPushButton:checked {
                background-color: rgba(100, 149, 237, 0.2);
            }
        """
        self.widget.repeat_button.setStyleSheet(mode_style)
        self.widget.shuffle_button.setStyleSheet(mode_style)
        self.widget.repeat_button.setIconSize(QSize(20, 20))  # Using QSize object
        self.widget.shuffle_button.setIconSize(QSize(20, 20))  # Using QSize object

        # Control buttons (Play/Next/Prev)
        nav_style = """
            QPushButton {
                background-color: white;
                border: 1px solid #e0e0e0;
                padding: 10px;
                border-radius: 20px;
                min-width: 40px;
                min-height: 40px;
            }
            QPushButton:hover {
                background-color: #f5f5f5;
                border-color: #d0d0d0;
            }
            QPushButton:pressed {
                background-color: #eeeeee;
            }
        """
        play_style = """
            QPushButton {
                background-color: rgb(100, 149, 237);
                border: none;
                padding: 12px;
                border-radius: 24px;
                min-width: 48px;
                min-height: 48px;
            }
            QPushButton:hover {
                background-color: rgb(120, 169, 255);
            }
            QPushButton:pressed {
                background-color: rgb(80, 129, 217);
            }
        """
        self.widget.previous_button.setStyleSheet(nav_style)
        self.widget.next_button.setStyleSheet(nav_style)
        self.widget.play_button.setStyleSheet(play_style)
        self.widget.previous_button.setIconSize(QSize(22, 22))  # Using QSize object
        self.widget.next_button.setIconSize(QSize(22, 22))  # Using QSize object
        self.widget.play_button.setIconSize(QSize(24, 24))  # Using QSize object

        # Progress slider
        self.widget.progress_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 4px;
                background: #e0e0e0;
                border-radius: 2px;
            }
            QSlider::handle:horizontal {
                width: 12px;
                height: 12px;
                background: white;
                border: 1px solid #d0d0d0;
                border-radius: 6px;
                margin: -4px 0;
            }
            QSlider::sub-page:horizontal {
                background: rgb(100, 149, 237);
                border-radius: 2px;
            }
        """)

        # Time label
        self.widget.time_label.setStyleSheet("""
            QLabel {
                color: #707070;
                font-size: 12px;
                font-weight: 500;
            }
        """)

        # Set modern font
        font = QFont("Segoe UI", 9)
        font.setWeight(QFont.Normal)
        self.widget.setFont(font)