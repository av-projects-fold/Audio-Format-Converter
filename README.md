# Python Audio Format Converter

This project is a Python-based audio format converter designed to handle various audio file formats that may not be easily importable into DAWs like Cubase. The tool provides a quick and intuitive drag-and-drop solution for converting audio files into compatible formats. 

## Features

- Drag-and-drop functionality for quick conversions.
- Supports a wide range of audio formats via `ffmpeg`.
- Supported formats: Audio Files (`*.mp3`, `*.wav`, `*.ogg`, `*.aac`, `*.aiff`, `*.m4a`).
- Standalone `.exe` generation for easy distribution.

---

## Table of Contents

- [Installation](#installation)
- [Folder Structure](#folder-structure)
- [Requirements](#requirements)
- [Building the .exe](#building-the-exe)
- [User Interface](#user-interface)

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/audio-converter.git
   cd audio-converter
   ```
2. Install the dependencies using `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

3. Download and place `ffmpeg` in the appropriate folder (see [Folder Structure](#folder-structure)).

---

## Building the .exe

Creating an executable for your Python application, along with including ffmpeg, can be accomplished using tools like PyInstaller. Below are the steps to package your AudioConverterApp into a standalone executable.

### Step 1: Create a Virtual Environment
In your project folder, create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### Step 2: Install Dependencies
Install the project dependencies listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Step 3: Install FFMPEG
Download `ffmpeg` and place the `ffmpeg.exe` binary in a folder named `ffmpeg` within your project directory. Ensure the folder structure matches the [Folder Structure](#folder-structure) section.

### Step 4: Modify Your Script
Ensure your script references the `ffmpeg` binary using a relative path. For example:

```python
...
    self.show_progress("Converting...")
    command = f'"{os.path.join(os.path.dirname(__file__), "ffmpeg", "ffmpeg.exe")}" -i "{self.input_file}" -y "{output_file}"'
    ...        

```

### Step 5: Install PyInstaller
Install PyInstaller in your virtual environment:

```bash
pip install pyinstaller
```

### Step 6: Create the Executable
Run the following command to generate the `.exe` file:

```bash
pyinstaller --onefile --add-data "ffmpeg;ffmpeg" AudioConverterApp.py
```

- `--onefile`: Packages everything into a single executable.
- `--add-data "ffmpeg;ffmpeg"`: Ensures the `ffmpeg` folder is included in the executable.

### Step 7: Locate Your Executable
After running the command, a new folder named `dist` will be created in your project directory. Inside the `dist` folder, you will find your executable named `AudioConverterApp.exe`.

---

## Folder Structure

For optimal performance and to ensure that `ffmpeg.exe` is properly included when generating the `.exe` file, organize the project folder as follows:

```
.
|-- AudioConverterApp.py
|-- ffmpeg/
|   |-- ffmpeg.exe
|   ...
|-- venv/
```

### Notes:
- Place the `ffmpeg` folder in the root directory of the project.
- The `ffmpeg.exe` binary must be present inside the `ffmpeg/` folder.

---

## User Interface

Below is an image of the application's UI:

![Application UI](img/User%20Interface.PNG)


---

Enjoy seamless audio format conversions! If you encounter any issues or have suggestions, feel free to submit a pull request or open an issue on GitHub.
