import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon
from functionality import MusicPlayer
from style import Style

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.player = MusicPlayer()
        self.style = Style(self.player)
        self.setCentralWidget(self.player)
        self.setWindowTitle("Music Player")
        self.setWindowIcon(QIcon("assets/music-player.png"))
        self.setMinimumSize(400, 650)
        self.style.apply_style()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())