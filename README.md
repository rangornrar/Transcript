# 🎙️ Whisper Pro Transcriber

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-stable-brightgreen)

**Whisper Pro Transcriber** is a modern, desktop graphical interface (GUI) for OpenAI's Whisper models. It allows you to transcribe audio and video files locally on your machine with high accuracy, completely offline.

It combines the standard **OpenAI Whisper** engine with the optimized **Faster-Whisper** implementation for blazing-fast performance.

---

## ✨ Key Features

* **🚀 Dual Engine Support:**
    * **Faster-Whisper:** Optimized for speed (up to 4x faster) and lower memory usage.
    * **OpenAI Whisper:** The standard reference implementation.
* **🎨 Modern UI:** Built with `CustomTkinter`, offering a clean look with native Dark/Light mode support.
* **📝 Multi-Format Export:**
    * **TXT:** Plain text transcription.
    * **SRT:** Subtitle files with precise timestamps (compatible with YouTube, VLC, etc.).
    * **JSON:** Full data export including metadata and confidence scores.
* **🌍 Auto-Language Detection:** Automatically identifies the language spoken in the audio.
* **💾 Smart Settings:** Automatically remembers your last used configuration (Model size, Language, Export format).
* **⚡ GPU Acceleration:** Automatically uses CUDA (NVIDIA GPU) if available, falling back to CPU if not.

---

## 🛠️ Installation

### 1. Prerequisites
* **Python 3.8+** must be installed on your system.
* **FFmpeg** is required by Whisper to process audio files.
    * *Windows:* `winget install ffmpeg` (or download from [ffmpeg.org](https://ffmpeg.org/))
    * *Mac:* `brew install ffmpeg`
    * *Linux:* `sudo apt install ffmpeg`

### 2. Install Python Dependencies
Open your terminal/command prompt and run:

```bash
pip install customtkinter openai-whisper faster-whisper torch
```
(Note: For GPU acceleration, ensure you have the correct PyTorch version with CUDA support installed).

## 📖 Usage Guide
### Launch the Application:

```Bash
python transcript_pro.py
```
### Configure Settings:

* **Engine:** Choose Faster-Whisper for speed, or OpenAI Whisper for maximum compatibility.

* **Quality (Model):**

  * tiny/base: Very fast, lower accuracy.

  * small/medium: Balanced.

  * large-v3: Maximum accuracy, requires more RAM/VRAM.

* **Language:** Select auto to let the AI guess, or specify a language.

* **Format:** Select .srt for subtitles or .txt for notes.

* **Add Files:** Click "+ Add Audio/Video" to select your media files (MP3, MP4, WAV, MKV, etc.).

* **Run:** Click "LANCER LA TRANSCRIPTION". The progress bar will indicate activity. The interface remains responsive thanks to multi-threading.

## 🧩 How it Works (Architecture)
The application is divided into two distinct layers to ensure stability:

### Extrait de code
```graph TD
    A[User Interface (CustomTkinter)] -->|Selects Files & Config| B(Configuration Manager)
    A -->|Clicks Run| C{Threading Manager}
    C -->|Spawns| D[Worker Thread]
    D -->|Loads| E[Transcription Engine]
    E -->|Selects| F[OpenAI Whisper]
    E -->|Selects| G[Faster-Whisper]
    F & G -->|Process Audio| H[Raw Segments]
    H -->|Formats| I[Export (SRT/TXT/JSON)]
    I -->|Saves| J[Disk]
    D -->|Updates| A
```
### ⚙️ Configuration File
The application creates a settings.json file in the root directory after the first run. You can manually edit this file if needed, though it is managed automatically by the UI.

```JSON
{
    "engine": "Faster-Whisper (Rapide & Léger)",
    "model_size": "base",
    "language": "fr",
    "export_format": "SRT (Sous-titres)",
    "device": "cuda"
}
```

## 🤝 Contributing
Feel free to fork this project and submit Pull Requests. Ideas for improvement:

[ ] Add "Diarization" (identifying who is speaking).

[ ] Add a visual audio player to preview files.

[ ] Drag-and-drop support.

## 📄 License
This project is open-source. Feel free to use and modify it.
