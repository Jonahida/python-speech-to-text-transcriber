import os
import wave
import contextlib
import math
import time
import speech_recognition as sr
from pydub import AudioSegment
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal



class Ui_MainWindow(object):
    """Main window GUI."""

    def __init__(self):
        """Initialization function."""
        self.audio_file = ""
        self.output_file = ""
        self.convert_thread = None
        self.transcription_thread = None

    def setupUi(self, MainWindow):
        """Define visual components and positions."""
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(653, 836)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Selected audio file label
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 20, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.selected_audio_label = QtWidgets.QLabel(self.centralwidget)
        self.selected_audio_label.setGeometry(QtCore.QRect(230, 20, 371, 41))
        font.setPointSize(8)
        self.selected_audio_label.setFont(font)
        self.selected_audio_label.setFrameShape(QtWidgets.QFrame.Box)
        self.selected_audio_label.setText("")
        self.selected_audio_label.setObjectName("selected_audio_label")

        # Output file name
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(50, 90, 161, 41))
        font.setPointSize(14)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")

        self.output_file_name = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.output_file_name.setGeometry(QtCore.QRect(230, 90, 371, 41))
        font.setPointSize(14)
        self.output_file_name.setFont(font)
        self.output_file_name.setObjectName("output_file_name")

        # Transcribed text box
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(230, 280, 161, 41))
        font.setPointSize(14)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")

        self.transcribed_text = QtWidgets.QTextBrowser(self.centralwidget)
        self.transcribed_text.setGeometry(QtCore.QRect(230, 320, 381, 431))
        self.transcribed_text.setObjectName("transcribed_text")

        # Transcribe button
        self.transcribe_button = QtWidgets.QPushButton(self.centralwidget)
        self.transcribe_button.setEnabled(False)
        self.transcribe_button.setGeometry(QtCore.QRect(230, 150, 221, 40))
        font.setPointSize(14)
        self.transcribe_button.setFont(font)
        self.transcribe_button.setObjectName("transcribe_button")
        self.transcribe_button.clicked.connect(self.process_and_transcribe_audio)

        # Stop button
        self.stop_button = QtWidgets.QPushButton(self.centralwidget)
        self.stop_button.setEnabled(False)
        self.stop_button.setGeometry(QtCore.QRect(230, 190, 221, 40))
        font.setPointSize(14)
        self.stop_button.setFont(font)
        self.stop_button.setObjectName("stop_button")
        self.stop_button.clicked.connect(self.stop_processing)

        # Progress bar
        self.progress_bar = QtWidgets.QProgressBar(self.centralwidget)
        self.progress_bar.setGeometry(QtCore.QRect(230, 250, 381, 23))
        self.progress_bar.setProperty("value", 0)
        self.progress_bar.setObjectName("progress_bar")

        # Message label (for errors and warnings)
        self.message_label = QtWidgets.QLabel(self.centralwidget)
        self.message_label.setGeometry(QtCore.QRect(0, 760, 651, 21))
        font.setPointSize(8)
        self.message_label.setFont(font)
        self.message_label.setFrameShape(QtWidgets.QFrame.Box)
        self.message_label.setText("")
        self.message_label.setObjectName("message_label")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 653, 21))
        self.menubar.setObjectName("menubar")

        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")

        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")

        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.actionOpen_audio_file = QtWidgets.QAction(MainWindow)
        self.actionOpen_audio_file.setObjectName("actionOpen_audio_file")
        self.actionOpen_audio_file.triggered.connect(self.open_audio_file)

        self.actionAbout_speech_to_text_transcriber = QtWidgets.QAction(MainWindow)
        self.actionAbout_speech_to_text_transcriber.setObjectName("actionAbout_speech_to_text_transcriber")
        self.actionAbout_speech_to_text_transcriber.triggered.connect(self.show_about)

        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionQuit.triggered.connect(self.quit_project)

        self.menuFile.addAction(self.actionOpen_audio_file)
        self.menuFile.addAction(self.actionQuit)
        self.menuAbout.addAction(self.actionAbout_speech_to_text_transcriber)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        """Translate UI method."""
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Speech to Text Transcriber"))
        self.label.setText(_translate("MainWindow", "Selected audio file:"))
        self.label_3.setText(_translate("MainWindow", "Output file name:"))
        self.label_5.setText(_translate("MainWindow", "Transcribed text:"))
        self.transcribe_button.setText(_translate("MainWindow", "Transcribe"))
        self.stop_button.setText(_translate("MainWindow", "Stop"))
        self.output_file_name.setPlaceholderText(_translate("MainWindow", "output_text.txt"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuAbout.setTitle(_translate("MainWindow", "About"))
        self.actionOpen_audio_file.setText(_translate("MainWindow", "Open audio file"))
        self.actionAbout_speech_to_text_transcriber.setText(_translate("MainWindow", "About Speech to Text Transcriber"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))

    def open_audio_file(self):
        """Open the audio file."""
        file_name, _ = QFileDialog.getOpenFileName(filter="Audio files (*.mp4 *.wav *.mp3 *.ogg *.flac *.aac *.m4a)")
        if file_name:
            self.transcribe_button.setEnabled(True)
            self.audio_file = file_name
            self.message_label.setText("")
            self.selected_audio_label.setText(file_name)
        else:
            self.message_label.setText("Please select an audio file")

    def convert_to_wav(self, input_file):
        """Convert any audio file to wav format."""
        self.message_label.setText("Converting audio file to WAV format...")
        audio = AudioSegment.from_file(input_file)
        wav_file = "converted_audio.wav"
        audio.export(wav_file, format="wav")
        return wav_file

    def get_audio_duration(self, audio_file):
        """Determine the length of the audio file."""
        with contextlib.closing(wave.open(audio_file, 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
            return duration

    def transcribe_audio(self, audio_file):
        """Transcribe the audio file."""
        total_duration = self.get_audio_duration(audio_file) / 10
        total_duration = math.ceil(total_duration)
        self.td = total_duration

        self.output_file = self.output_file_name.toPlainText() or "my_speech_file.txt"
        
        # Use thread to process in the background and avoid freezing the GUI
        self.transcription_thread = TranscriptionThread(total_duration, audio_file, self.output_file)
        self.transcription_thread.finished.connect(self.finished_transcribing)
        self.transcription_thread.change_value.connect(self.set_progress_value)
        self.transcription_thread.start()

    def finished_converting(self, wav_file):
        """Reset message text when conversion is finished."""
        self.message_label.setText("Transcribing file...")
        self.transcribe_audio(wav_file)

    def finished_transcribing(self):
        """This runs when transcription is finished to tidy up UI."""
        self.progress_bar.setValue(100)
        self.transcribe_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.message_label.setText("Transcription complete.")
        self.update_text_output()

    def set_progress_value(self, val):
        """Update progress bar value."""
        increment = int(math.floor(100 * (float(val) / self.td)))
        self.progress_bar.setValue(increment)

    def process_and_transcribe_audio(self):
        """Process the audio into a textual transcription."""
        self.transcribe_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        wav_file = self.convert_to_wav(self.audio_file)
        self.finished_converting(wav_file)

    def stop_processing(self):
        """Stop the ongoing transcription or conversion."""
        if self.convert_thread and self.convert_thread.isRunning():
            self.convert_thread.terminate()
            self.message_label.setText("Conversion stopped.")
        if self.transcription_thread and self.transcription_thread.isRunning():
            self.transcription_thread.terminate()
            self.message_label.setText("Transcription stopped.")
        self.transcribe_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def update_text_output(self):
        """Update the text box with the transcribed file."""
        with open(self.output_file, "r") as f:
            self.transcribed_text.setText(f.read())

    def quit_project(self):
        """Quit the application."""
        QtWidgets.qApp.quit()

    def show_about(self):
        """Show about message box."""
        msg = QMessageBox()
        msg.setWindowTitle("About Speech to Text Transcriber")
        msg.setText("Based on vid2speech created by Dr. Alan Davies,\nSenior Lecturer,\nHealth Data Science,\nManchester University, UK")
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

class TranscriptionThread(QThread):
    """Thread to transcribe file from audio to text."""

    change_value = pyqtSignal(int)

    def __init__(self, total_duration, audio_file, output_file):
        """Initialization function."""
        super().__init__()
        self.total_duration = total_duration
        self.audio_file = audio_file
        self.output_file = output_file

    def run(self):
        """Run transcription, audio to text."""
        recognizer = sr.Recognizer()
        for i in range(0, self.total_duration):
            try:
                with sr.AudioFile(self.audio_file) as source:
                    audio = recognizer.record(source, offset=i * 10, duration=10)
                    with open(self.output_file, "a") as f:
                        f.write(recognizer.recognize_google(audio))
                        f.write(" ")
                    self.change_value.emit(i)
            except sr.UnknownValueError:
                print("Unknown word detected...")
            except Exception as e:
                print(f"An error occurred: {e}")
                continue

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
