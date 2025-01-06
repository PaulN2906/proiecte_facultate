from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QProgressBar, QFileDialog, QWidget, QSlider, QStyleFactory, QInputDialog)
from PyQt5.QtCore import QTimer, Qt
from pydub import AudioSegment, effects
import pygame
import os
import tempfile
import sounddevice as sd
import wave

class SimpleAudioEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

        self.audio_file = None
        self.audio_segment = None
        self.is_playing = False
        self.is_paused = False
        self.current_time = 0
        self.total_time = 0

        self.temp_file = None

        pygame.mixer.init()

# Initializare interfata grafica
    def initUI(self):
        self.setWindowTitle("Simple Audio Editor")
        self.setGeometry(200, 200, 600, 400)
        self.setStyle(QStyleFactory.create('Fusion'))

        # Main layout
        main_layout = QVBoxLayout()

        # Status bar
        self.status_label = QLabel("No file loaded", self)
        self.status_label.setStyleSheet("font-size: 16px;")
        main_layout.addWidget(self.status_label)

        # Progress bar
        self.progress_label = QLabel("0:00 / 0:00", self)
        main_layout.addWidget(self.progress_label)

        self.progress = QProgressBar(self)
        self.progress.setValue(0)
        self.progress.setTextVisible(False)
        main_layout.addWidget(self.progress)

        # Controls layout
        controls_layout = QHBoxLayout()

        self.load_button = QPushButton("Load Audio", self)
        self.load_button.clicked.connect(self.load_audio)
        controls_layout.addWidget(self.load_button)

        self.record_button = QPushButton("Record", self)
        self.record_button.clicked.connect(self.record_audio)
        controls_layout.addWidget(self.record_button)

        self.play_button = QPushButton("Play", self)
        self.play_button.clicked.connect(self.play_audio)
        controls_layout.addWidget(self.play_button)

        self.pause_button = QPushButton("Pause", self)
        self.pause_button.clicked.connect(self.pause_audio)
        controls_layout.addWidget(self.pause_button)

        self.resume_button = QPushButton("Resume", self)
        self.resume_button.clicked.connect(self.resume_audio)
        controls_layout.addWidget(self.resume_button)

        self.stop_button = QPushButton("Stop", self)
        self.stop_button.clicked.connect(self.stop_audio)
        controls_layout.addWidget(self.stop_button)

        self.forward_button = QPushButton(">> 5s", self)
        self.forward_button.clicked.connect(self.go_forward)
        controls_layout.addWidget(self.forward_button)

        self.backward_button = QPushButton("<< 5s", self)
        self.backward_button.clicked.connect(self.go_backward)
        controls_layout.addWidget(self.backward_button)

        main_layout.addLayout(controls_layout)

        # Filters and export layout
        filters_layout = QHBoxLayout()

        self.filter_button = QPushButton("Deepen Voice", self)
        self.filter_button.clicked.connect(self.deepen_voice_filter)
        filters_layout.addWidget(self.filter_button)

        self.squeaky_button = QPushButton("Squeaky Voice", self)
        self.squeaky_button.clicked.connect(self.squeaky_voice_filter)
        filters_layout.addWidget(self.squeaky_button)

        self.trim_button = QPushButton("Trim Audio", self)
        self.trim_button.clicked.connect(self.trim_audio)
        filters_layout.addWidget(self.trim_button)

        self.export_button = QPushButton("Export Audio", self)
        self.export_button.clicked.connect(self.export_audio)
        filters_layout.addWidget(self.export_button)

        main_layout.addLayout(filters_layout)

        # Volume slider
        volume_layout = QHBoxLayout()
        volume_label = QLabel("Volume", self)
        self.volume_slider = QSlider(Qt.Horizontal, self)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(100)
        self.volume_slider.valueChanged.connect(self.set_volume)
        volume_layout.addWidget(volume_label)
        volume_layout.addWidget(self.volume_slider)
        main_layout.addLayout(volume_layout)

        # Set main layout
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Timer for updating progress
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)

# Functie pentru incarcarea unui fisier audio
    def load_audio(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Audio File", "", "Audio Files (*.mp3 *.wav)")
        if file_path:
            try:
                self.audio_file = file_path
                self.audio_segment = AudioSegment.from_file(file_path)
                self.total_time = len(self.audio_segment) / 1000  # Convert to seconds
                self.status_label.setText(f"Loaded: {file_path}")
                self.progress.setValue(0)
                self.update_progress_label()
            except Exception as e:
                self.status_label.setText(f"Error loading file: {e}")

# Functie pentru inregistrarea audio din aplicatie
    def record_audio(self):
        duration, ok = QInputDialog.getInt(self, "Record Audio", "Enter duration in seconds:", 5, 1, 300, 1)
        if ok:
            self.temp_file = self.perform_record_audio(duration)
            self.audio_file = self.temp_file
            self.audio_segment = AudioSegment.from_file(self.audio_file)
            self.total_time = len(self.audio_segment) / 1000
            self.status_label.setText("Recording complete and loaded into editor")

# Functie auxiliara pentru inregistrarea audio si salvarea intr-un fisier temporar
    def perform_record_audio(self, duration):
        temp_file = tempfile.mktemp(suffix=".wav")
        samplerate = 44100
        channels = 2
        recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=channels, dtype="int16")
        sd.wait()
        with wave.open(temp_file, "wb") as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(2)  # 16-bit audio
            wf.setframerate(samplerate)
            wf.writeframes(recording.tobytes())
        return temp_file

# Functie pentru redarea audio
    def play_audio(self):
        if self.audio_file:
            self.is_playing = True
            self.is_paused = False
            pygame.mixer.music.load(self.audio_file)
            pygame.mixer.music.play()
            self.timer.start(100)
            self.status_label.setText("Playing audio")
        else:
            self.status_label.setText("Please load an audio file first.")

# Functie pentru pauzarea redarii audio
    def pause_audio(self):
        if self.is_playing and not self.is_paused:
            self.is_paused = True
            pygame.mixer.music.pause()
            self.status_label.setText("Playback paused")

# Functie pentru reluarea redarii audio dupa pauza
    def resume_audio(self):
        if self.is_playing and self.is_paused:
            self.is_paused = False
            pygame.mixer.music.unpause()
            self.status_label.setText("Resuming playback")

# Functie pentru oprirea redarii audio
    def stop_audio(self):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = False
            pygame.mixer.music.stop()
            self.timer.stop()
            self.progress.setValue(0)
            self.current_time = 0
            self.update_progress_label()
            self.status_label.setText("Playback stopped")

# Functie pentru derularea audio inainte cu 5 secunde
    def go_forward(self):
        if self.is_playing:
            self.current_time = min(self.current_time + 5, self.total_time)
            pygame.mixer.music.set_pos(self.current_time)
            self.update_progress_label()

# Functie pentru derularea audio inapoi cu 5 secunde
    def go_backward(self):
        if self.is_playing:
            self.current_time = max(self.current_time - 5, 0)
            pygame.mixer.music.set_pos(self.current_time)
            self.update_progress_label()

# Functie pentru decuparea unui interval audio selectat
    def trim_audio(self):
        if self.audio_segment:
            start_time, ok1 = QInputDialog.getInt(self, "Trim Audio", "Enter start time in seconds:", 0, 0, int(self.total_time), 1)
            if not ok1:
                return

            end_time, ok2 = QInputDialog.getInt(self, "Trim Audio", "Enter end time in seconds:", int(self.total_time), 0, int(self.total_time), 1)
            if not ok2:
                return

            start_time_ms = start_time * 1000
            end_time_ms = end_time * 1000

            if start_time_ms < end_time_ms:
                self.audio_segment = self.audio_segment[start_time_ms:end_time_ms]
                self.total_time = len(self.audio_segment) / 1000
                self.current_time = 0

                # Save the trimmed audio to a temporary file
                if self.temp_file:
                    os.remove(self.temp_file)
                self.temp_file = tempfile.mktemp(suffix=".wav")
                self.audio_segment.export(self.temp_file, format="wav")
                self.audio_file = self.temp_file

                self.update_progress_label()
                self.status_label.setText("Audio trimmed and ready to play")
            else:
                self.status_label.setText("Invalid trim range")

# Functie pentru aplicarea filtrului de voce groasa
    def deepen_voice_filter(self):
        if self.audio_segment:
            try:
                self.audio_segment = self.audio_segment._spawn(self.audio_segment.raw_data, overrides={"frame_rate": int(self.audio_segment.frame_rate * 0.8)})
                self.audio_segment = self.audio_segment.set_frame_rate(44100)  # Reset to standard frame rate
                self.audio_segment.export("filtered_audio.wav", format="wav")
                self.audio_file = "filtered_audio.wav"
                self.status_label.setText("Voice deepened and filtered")
            except Exception as e:
                self.status_label.setText(f"Error applying filter: {e}")

# Functie pentru aplicarea filtrului de voce subtire
    def squeaky_voice_filter(self):
        if self.audio_segment:
            try:
                self.audio_segment = self.audio_segment._spawn(self.audio_segment.raw_data, overrides={"frame_rate": int(self.audio_segment.frame_rate * 1.5)})
                self.audio_segment = self.audio_segment.set_frame_rate(44100)  # Reset to standard frame rate
                self.audio_segment.export("filtered_audio_squeaky.wav", format="wav")
                self.audio_file = "filtered_audio_squeaky.wav"
                self.status_label.setText("Voice made squeaky")
            except Exception as e:
                self.status_label.setText(f"Error applying filter: {e}")

# Functie pentru exportarea fisierului audio editat
    def export_audio(self):
        if self.audio_segment:
            file_path, _ = QFileDialog.getSaveFileName(self, "Export Audio", "", "Audio Files (*.mp3 *.wav)")
            if file_path:
                try:
                    self.audio_segment.export(file_path, format=file_path.split('.')[-1])
                    self.status_label.setText(f"Audio exported to: {file_path}")
                except Exception as e:
                    self.status_label.setText(f"Error exporting audio: {e}")

# Functie pentru setarea volumului redarii audio
    def set_volume(self, value):
        pygame.mixer.music.set_volume(value / 100)

# Functie pentru actualizarea progresului redarii audio
    def update_progress(self):
        if self.is_playing and not self.is_paused:
            self.current_time += 0.1
            if self.current_time >= self.total_time:
                self.timer.stop()
                self.status_label.setText("Playback finished")
                self.progress.setValue(0)
                self.is_playing = False
            else:
                progress_value = int((self.current_time / self.total_time) * 100)
                self.progress.setValue(progress_value)
                self.update_progress_label()

# Functie pentru actualizarea progresului redarii audio
    def update_progress_label(self):
        current_minutes = int(self.current_time // 60)
        current_seconds = int(self.current_time % 60)
        total_minutes = int(self.total_time // 60)
        total_seconds = int(self.total_time % 60)
        self.progress_label.setText(f"{current_minutes}:{current_seconds:02d} / {total_minutes}:{total_seconds:02d}")

# Punctul de intrare in aplicatie
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    editor = SimpleAudioEditor()
    editor.show()
    sys.exit(app.exec_())
