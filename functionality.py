import os
import random
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QSlider, QListWidget, QPushButton, QFileDialog, 
                            QListWidgetItem)
from PyQt5.QtCore import Qt, QTimer, QUrl
from PyQt5.QtGui import QIcon, QFont
import pygame

class MusicPlayer(QWidget):
    def __init__(self):
        super().__init__()
        # Initialize pygame mixer
        pygame.mixer.init()
        self.current_song_index = -1
        self.is_playing = False
        self.playback_mode = "sequential"
        self.song_length = 0
        self.current_position = 0
        
        self.init_ui()
        self.setup_connections()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)

        # Top controls with icons
        top_controls = QHBoxLayout()
        self.add_button = QPushButton()
        self.add_button.setIcon(QIcon("assets/add.png"))
        
        self.repeat_button = QPushButton()
        self.repeat_button.setIcon(QIcon("assets/repeat.png"))
        self.repeat_button.setCheckable(True)
        
        self.shuffle_button = QPushButton()
        self.shuffle_button.setIcon(QIcon("assets/shuffle.png"))
        self.shuffle_button.setCheckable(True)
        
        top_controls.addWidget(self.add_button)
        top_controls.addStretch()
        top_controls.addWidget(self.repeat_button)
        top_controls.addWidget(self.shuffle_button)
        
        # Now Playing label
        self.now_playing_label = QLabel("Now Playing: ")
        self.now_playing_label.setAlignment(Qt.AlignCenter)
        self.now_playing_label.setFont(QFont('Arial', 10, QFont.Bold))
        
        # Player display
        self.time_label = QLabel("0:00 / 0:00")
        self.time_label.setAlignment(Qt.AlignCenter)
        self.progress_slider = QSlider(Qt.Horizontal)
        self.progress_slider.setRange(0, 100)
        
        # Playlist
        self.playlist = QListWidget()
        
        # Playback controls with icons
        controls = QHBoxLayout()
        self.previous_button = QPushButton()
        self.previous_button.setIcon(QIcon("assets/previous.png"))
        
        self.play_button = QPushButton()
        self.play_button.setIcon(QIcon("assets/play-buttton.png"))
        
        self.next_button = QPushButton()
        self.next_button.setIcon(QIcon("assets/next-button.png"))
        
        controls.addStretch()
        controls.addWidget(self.previous_button)
        controls.addWidget(self.play_button)
        controls.addWidget(self.next_button)
        controls.addStretch()
        
        # Assemble layout
        self.layout.addLayout(top_controls)
        self.layout.addWidget(self.now_playing_label)  # Add Now Playing label
        self.layout.addWidget(self.time_label)
        self.layout.addWidget(self.progress_slider)
        self.layout.addWidget(self.playlist)
        self.layout.addLayout(controls)
        
        self.setLayout(self.layout)

    def setup_connections(self):
        self.add_button.clicked.connect(self.add_songs)
        self.play_button.clicked.connect(self.toggle_play)
        self.previous_button.clicked.connect(self.previous_song)
        self.next_button.clicked.connect(self.next_song)
        self.playlist.itemDoubleClicked.connect(self.play_selected)
        self.repeat_button.clicked.connect(self.toggle_repeat_mode)
        self.shuffle_button.clicked.connect(self.toggle_shuffle_mode)
        self.progress_slider.sliderMoved.connect(self.seek_position)

    def add_songs(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Select Music Files", "", "Audio Files (*.mp3 *.wav *.ogg *.flac)")
        
        for file in files:
            abs_path = os.path.abspath(file)
            if os.path.exists(abs_path):
                item = QListWidgetItem(os.path.basename(abs_path))
                item.setData(Qt.UserRole, abs_path)
                self.playlist.addItem(item)

    def play_song(self):
        if 0 <= self.current_song_index < self.playlist.count():
            song_path = self.playlist.item(self.current_song_index).data(Qt.UserRole)
            
            try:
                pygame.mixer.music.stop()
                pygame.mixer.music.load(song_path)
                pygame.mixer.music.play()
                self.play_button.setIcon(QIcon("assets/pause (1).png"))
                self.is_playing = True
                
                # Update Now Playing label
                song_name = os.path.basename(song_path)
                self.now_playing_label.setText(f"Now Playing: {os.path.splitext(song_name)[0]}")
                
                # Get song length
                sound = pygame.mixer.Sound(song_path)
                self.song_length = sound.get_length()
                self.current_position = 0
                
                self.timer.start(1000)
                
            except Exception as e:
                print(f"Error playing song: {e}")

    def toggle_play(self):
        if self.playlist.count() == 0:
            return
            
        if self.is_playing:
            pygame.mixer.music.pause()
            self.play_button.setIcon(QIcon("assets/play-buttton.png"))
            self.is_playing = False
            self.timer.stop()
        else:
            if self.current_song_index == -1 and self.playlist.count() > 0:
                self.current_song_index = 0
                self.playlist.setCurrentRow(0)
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.unpause()
            else:
                self.play_song()
            self.play_button.setIcon(QIcon("assets/pause (1).png"))
            self.is_playing = True
            self.timer.start(1000)

    def next_song(self):
        if self.playlist.count() == 0:
            return
            
        if self.playback_mode == "shuffle":
            self.current_song_index = random.randint(0, self.playlist.count() - 1)
        else:
            self.current_song_index = (self.current_song_index + 1) % self.playlist.count()
            
        self.playlist.setCurrentRow(self.current_song_index)
        self.play_song()

    def previous_song(self):
        if self.playlist.count() == 0:
            return
            
        if self.current_position > 3:
            self.current_position = 0
            pygame.mixer.music.rewind()
            self.play_song()
        else:
            if self.playback_mode == "shuffle":
                self.current_song_index = random.randint(0, self.playlist.count() - 1)
            else:
                self.current_song_index = (self.current_song_index - 1) % self.playlist.count()
            self.playlist.setCurrentRow(self.current_song_index)
            self.play_song()

    def play_selected(self, item):
        self.current_song_index = self.playlist.row(item)
        self.play_song()

    def toggle_repeat_mode(self):
        modes = ["sequential", "repeat_one", "repeat_all"]
        current_index = modes.index(self.playback_mode) if self.playback_mode in modes else 0
        self.playback_mode = modes[(current_index + 1) % len(modes)]
        
        if self.playback_mode == "repeat_one":
            self.repeat_button.setIcon(QIcon("assets/repeat (1).png"))
        else:
            self.repeat_button.setIcon(QIcon("assets/repeat.png"))

    def toggle_shuffle_mode(self):
        self.playback_mode = "shuffle" if self.shuffle_button.isChecked() else "sequential"

    def update_progress(self):
        if self.is_playing and self.song_length > 0:
            self.current_position += 1
            if self.current_position >= self.song_length:
                self.handle_song_end()
            
            progress = (self.current_position / self.song_length) * 100
            self.progress_slider.setValue(int(progress))
            self.time_label.setText(
                f"{self.format_time(self.current_position)} / {self.format_time(self.song_length)}"
            )

    def handle_song_end(self):
        if self.playback_mode == "repeat_one":
            self.current_position = 0
            self.play_song()
        else:
            self.next_song()

    def seek_position(self, position):
        if self.song_length > 0:
            seek_pos = (position / 100) * self.song_length
            self.current_position = seek_pos
            pygame.mixer.music.set_pos(seek_pos)
            self.time_label.setText(
                f"{self.format_time(seek_pos)} / {self.format_time(self.song_length)}"
            )

    def format_time(self, seconds):
        return f"{int(seconds // 60)}:{int(seconds % 60):02d}"

    def closeEvent(self, event):
        pygame.mixer.quit()
        event.accept()