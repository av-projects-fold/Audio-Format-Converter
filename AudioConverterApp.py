import sys
import os
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, 
    QProgressBar, QFileDialog, QLineEdit, QMessageBox, 
    QHBoxLayout, QComboBox, QGroupBox, QSizePolicy
)
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDragEnterEvent, QDropEvent
from mutagen import File  # Only import the main File class


class AudioConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AV Audio Converter")
        self.setMinimumSize(250, 450)
        self.setMaximumSize(350, 600)
        self.setAcceptDrops(True)
        
        self.input_file = ""
        self.output_directory = "C:\\Users\\"
        
        # Create the layout
        self.layout = QVBoxLayout()
        
        input_group_box = QGroupBox("Input")
        input_group_layout = QVBoxLayout()

        # Input label and drag area
        self.drag_area = QLabel("Drag and drop files here")
        self.drag_area.setStyleSheet("border: 2px dashed #aaa; padding: 10px;")
        self.drag_area.setAlignment(Qt.AlignCenter)
        input_group_layout.addWidget(self.drag_area)
        
        # Select File button
        self.select_file_button = QPushButton("Select File")
        self.select_file_button.clicked.connect(self.select_file)
        input_group_layout.addWidget(self.select_file_button)
        
        # Input file information label
        self.file_info_label = QLabel("Input file information")
        self.file_info_label.setWordWrap(True)  # Enable word wrapping for the label
        input_group_layout.addWidget(self.file_info_label)

        input_group_box.setLayout(input_group_layout)
        input_group_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)  # Allow dynamic resizing
        self.layout.addWidget(input_group_box)





        self.layout.addSpacing(20)
        output_group_box = QGroupBox("Output Settings")
        output_group_layout = QVBoxLayout()
        # Output settings
        
        # Output directory
        self.directory_line_edit = QLineEdit(self.output_directory)
        output_group_layout.addWidget(self.directory_line_edit)
        
        # Change Output Directory button
        self.change_dir_button = QPushButton("Change Output Directory")
        self.change_dir_button.clicked.connect(self.change_output_directory)
        output_group_layout.addWidget(self.change_dir_button)
        
        # Output format dropdown
        self.output_format_combo = QComboBox()
        self.output_format_combo.addItems(["MP3", "WAV", "OGG", "AAC", "AIFF", "M4A"])
        output_group_layout.addWidget(self.output_format_combo)
        
        output_group_box.setLayout(output_group_layout)
        self.layout.addWidget(output_group_box)






        #Setting up Groubox
        self.layout.addSpacing(20)
        Process_group_box = QGroupBox("Process")
        Process_group_layout = QVBoxLayout()

        # Convert button    
        self.convert_button = QPushButton("Convert")
        self.convert_button.clicked.connect(self.convert_audio)
        Process_group_layout.addWidget(self.convert_button)
        
        # Clear button
        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_interface)
        Process_group_layout.addWidget(self.clear_button)
        
        # Progress label and bar
        self.progress_label = QLabel("Progress...")
        Process_group_layout.addWidget(self.progress_label)
        
        self.progress_bar = QProgressBar()
        Process_group_layout.addWidget(self.progress_bar)

        Process_group_box.setLayout(Process_group_layout)
        self.layout.addWidget(Process_group_box)
        
        # Set the main layout
        self.setLayout(self.layout)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            file_path = event.mimeData().urls()[0].toLocalFile()
            if self.validate_file(file_path):
                self.input_file = file_path
                self.update_file_info()
                self.adjustSize()

    def select_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Audio File", "", "Audio Files (*.mp3 *.wav *.ogg *.aac *.aiff *.m4a)", options=options)
        if file_path and self.validate_file(file_path):
            self.input_file = file_path
            self.update_file_info()
            self.adjustSize()

    def change_output_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Output Directory", self.output_directory)
        if directory:
            self.output_directory = directory
            self.directory_line_edit.setText(directory)

    def convert_audio(self):
        if not self.input_file:
            self.show_error("No input file selected.")
            return

        output_format = self.output_format_combo.currentText().lower()
        base_name = os.path.splitext(os.path.basename(self.input_file))[0]
        output_file = os.path.join(self.output_directory, f"{base_name}_AV_Converted.{output_format}")

        self.progress_bar.setValue(0)
        
        try:
            self.show_progress("Converting...")
            command = f'"{os.path.join(os.path.dirname(__file__), "ffmpeg", "ffmpeg.exe")}" -i "{self.input_file}" -y "{output_file}"'
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # Wait for the process to complete
            process.communicate()  # This will block until the conversion is done

            if process.returncode != 0:
                self.show_error(f"Conversion failed. Error: {process.stderr.read()}")
            else:
                self.progress_bar.setValue(100)  # Set progress to 100% when conversion is complete
                self.show_progress("Conversion completed successfully!")

        except Exception as e:
            self.show_error(f"Error during conversion: {str(e)}")





    def validate_file(self, file_path):
        if not os.path.isfile(file_path):
            self.show_error("File does not exist.")
            return False
        
        supported_formats = [".mp3", ".wav", ".ogg", ".aac", ".aiff", ".m4a"]
        if not any(file_path.lower().endswith(ext) for ext in supported_formats):
            self.show_error("Unsupported file type.")
            return False

        return True

    def update_file_info(self):
        if self.input_file:
            audio = File(self.input_file)
            if audio is not None:
                # Default values
                duration = audio.info.length  # Duration in seconds
                bitrate = audio.info.bitrate // 1000 if audio.info.bitrate else 0  # Convert to kbps
                sample_rate = audio.info.sample_rate if hasattr(audio.info, 'sample_rate') else 'N/A'
                channels = audio.info.channels if hasattr(audio.info, 'channels') else 'N/A'
                
                # Determine the format and bit depth
                file_format = os.path.splitext(self.input_file)[1][1:].upper()
                bit_depth = "N/A"

                # Format output string
                self.file_info_label.setText(
                    f"Duration: {duration:.2f} seconds, "
                    f"Format: {file_format}, "
                    f"Bitrate: {bitrate} kbps, "
                    f"Sample Rate: {sample_rate} Hz, "
                    f"Bit Depth: {bit_depth}, "
                    f"Channels: {channels}"
                )
                self.adjustSize()
            else:
                self.file_info_label.setText("Could not read audio properties.")


    def clear_interface(self):
        self.input_file = ""
        self.file_info_label.setText("Input file information")
        self.progress_bar.setValue(0)
        self.directory_line_edit.setText(self.output_directory)

    def show_progress(self, message):
        self.progress_label.setText(message)

    def show_error(self, message):
        QMessageBox.critical(self, "Error", message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    converter = AudioConverterApp()
    converter.show()
    sys.exit(app.exec_())
