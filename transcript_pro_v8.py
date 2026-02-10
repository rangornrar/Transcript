import os
import time
import json
import threading
import datetime
import tkinter as tk
from tkinter import filedialog, messagebox
from typing import List, Dict, Any

# --- IMPORT UI MODERNE ---
try:
    import customtkinter as ctk
except ImportError:
    print("❌ Erreur: 'customtkinter' manquant. Installez-le avec 'pip install customtkinter'")
    # Fallback sur tkinter standard si nécessaire, mais ici on vise le moderne
    import tkinter as ctk 

# --- IMPORTS MOTEURS ---
try:
    import torch
except ImportError:
    torch = None

HAS_WHISPER = False
try:
    import whisper
    HAS_WHISPER = True
except ImportError:
    pass

HAS_FASTER_WHISPER = False
try:
    from faster_whisper import WhisperModel
    HAS_FASTER_WHISPER = True
except ImportError:
    pass

# --- CONFIGURATION & UTILITAIRES ---

class ConfigManager:
    """Gère la sauvegarde et le chargement des préférences utilisateur."""
    FILE_NAME = "settings.json"
    
    DEFAULT_CONFIG = {
        "engine": "Faster-Whisper (Rapide & Léger)" if HAS_FASTER_WHISPER else "OpenAI Whisper (Standard)",
        "model_size": "base",
        "language": "fr",
        "export_format": "SRT (Sous-titres)",
        "device": "cuda" if (torch and torch.cuda.is_available()) else "cpu"
    }

    @staticmethod
    def load():
        if os.path.exists(ConfigManager.FILE_NAME):
            try:
                with open(ConfigManager.FILE_NAME, "r") as f:
                    return {**ConfigManager.DEFAULT_CONFIG, **json.load(f)}
            except:
                pass
        return ConfigManager.DEFAULT_CONFIG

    @staticmethod
    def save(config: dict):
        with open(ConfigManager.FILE_NAME, "w") as f:
            json.dump(config, f, indent=4)

def format_timestamp(seconds: float, separator=",") -> str:
    """Convertit des secondes (float) en format HH:MM:SS,mmm"""
    td = datetime.timedelta(seconds=seconds)
    # On hack un peu pour avoir les millisecondes proprement
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    millis = int((seconds - total_seconds) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}{separator}{millis:03d}"

# --- BACKEND TRANSCRIPTION ---

class TranscriptionEngine:
    ENGINE_OPENAI = "OpenAI Whisper (Standard)"
    ENGINE_FASTER = "Faster-Whisper (Rapide & Léger)"

    def __init__(self):
        self.current_engine_type = None
        self.current_model_name = None
        self.model_instance = None
        self.device = "cuda" if (torch and torch.cuda.is_available()) else "cpu"

    def load_model(self, engine_type: str, model_name: str, callback_log):
        if (self.model_instance and 
            self.current_engine_type == engine_type and 
            self.current_model_name == model_name):
            return

        callback_log(f"🔄 Chargement modèle : {model_name} ({engine_type})...")
        
        # Libération mémoire
        self.model_instance = None
        if self.device == "cuda":
            torch.cuda.empty_cache()

        if engine_type == self.ENGINE_FASTER:
            compute_type = "float16" if self.device == "cuda" else "int8"
            self.model_instance = WhisperModel(model_name, device=self.device, compute_type=compute_type)
        
        elif engine_type == self.ENGINE_OPENAI:
            self.model_instance = whisper.load_model(model_name, device=self.device)
        
        self.current_engine_type = engine_type
        self.current_model_name = model_name
        callback_log(f"✅ Modèle prêt sur {self.device.upper()}.")

    def transcribe(self, filepath: str, language: str, callback_log) -> List[Dict]:
        """Retourne une liste standardisée de segments : [{'start': 0.0, 'end': 1.0, 'text': '...'}]"""
        
        callback_log(f"🎤 Analyse de : {os.path.basename(filepath)}...")
        segments_data = []
        lang_arg = None if language == "auto" else language

        if self.current_engine_type == self.ENGINE_FASTER:
            segments, info = self.model_instance.transcribe(filepath, language=lang_arg, beam_size=5)
            # Faster-Whisper renvoie un générateur, on boucle pour exécuter
            if info.language_probability > 0.5:
                callback_log(f"🌍 Langue détectée : {info.language.upper()} ({info.language_probability:.0%})")
            
            for seg in segments:
                segments_data.append({
                    "start": seg.start,
                    "end": seg.end,
                    "text": seg.text.strip()
                })

        elif self.current_engine_type == self.ENGINE_OPENAI:
            result = self.model_instance.transcribe(filepath, language=lang_arg, fp16=(self.device=="cuda"))
            for seg in result.get("segments", []):
                segments_data.append({
                    "start": seg["start"],
                    "end": seg["end"],
                    "text": seg["text"].strip()
                })
        
        return segments_data

    def export_file(self, segments: List[Dict], filepath: str, format_type: str):
        base_path = os.path.splitext(filepath)[0]
        
        if "TXT" in format_type:
            with open(f"{base_path}.txt", "w", encoding="utf-8") as f:
                for seg in segments:
                    f.write(f"{seg['text']}\n")

        elif "SRT" in format_type:
            with open(f"{base_path}.srt", "w", encoding="utf-8") as f:
                for i, seg in enumerate(segments):
                    start = format_timestamp(seg['start'], separator=",")
                    end = format_timestamp(seg['end'], separator=",")
                    f.write(f"{i+1}\n{start} --> {end}\n{seg['text']}\n\n")

        elif "JSON" in format_type:
            with open(f"{base_path}.json", "w", encoding="utf-8") as f:
                json.dump(segments, f, indent=4, ensure_ascii=False)

# --- INTERFACE GRAPHIQUE (CustomTkinter) ---

class ModernApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configuration de base
        ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
        ctk.set_default_color_theme("blue")
        
        self.title("🎙️ Whisper Pro Transcriber")
        self.geometry("900x700")
        
        self.backend = TranscriptionEngine()
        self.config = ConfigManager.load()
        self.files_to_process = []

        self.setup_ui()

    def setup_ui(self):
        # --- 1. Header & Configuration ---
        self.frame_config = ctk.CTkFrame(self)
        self.frame_config.pack(fill="x", padx=15, pady=15)

        # Moteur
        lbl_eng = ctk.CTkLabel(self.frame_config, text="Moteur IA:", font=("Roboto", 12, "bold"))
        lbl_eng.grid(row=0, column=0, padx=10, pady=10)
        self.cb_engine = ctk.CTkComboBox(self.frame_config, width=200, 
                                         values=[self.backend.ENGINE_FASTER, self.backend.ENGINE_OPENAI])
        self.cb_engine.set(self.config["engine"])
        self.cb_engine.grid(row=0, column=1, padx=10, pady=10)

        # Modèle
        lbl_mod = ctk.CTkLabel(self.frame_config, text="Qualité:", font=("Roboto", 12, "bold"))
        lbl_mod.grid(row=0, column=2, padx=10)
        self.cb_model = ctk.CTkComboBox(self.frame_config, width=120, 
                                        values=["tiny", "base", "small", "medium", "large-v3", "distil-large-v3"])
        self.cb_model.set(self.config["model_size"])
        self.cb_model.grid(row=0, column=3, padx=10)

        # Langue
        lbl_lang = ctk.CTkLabel(self.frame_config, text="Langue:", font=("Roboto", 12, "bold"))
        lbl_lang.grid(row=0, column=4, padx=10)
        self.cb_lang = ctk.CTkComboBox(self.frame_config, width=80, values=["auto", "fr", "en", "es", "de", "it", "ja"])
        self.cb_lang.set(self.config["language"])
        self.cb_lang.grid(row=0, column=5, padx=10)

        # Format Export
        lbl_fmt = ctk.CTkLabel(self.frame_config, text="Format:", font=("Roboto", 12, "bold"))
        lbl_fmt.grid(row=0, column=6, padx=10)
        self.cb_format = ctk.CTkComboBox(self.frame_config, width=150, values=["TXT (Texte brut)", "SRT (Sous-titres)", "JSON (Complet)"])
        self.cb_format.set(self.config["export_format"])
        self.cb_format.grid(row=0, column=7, padx=10)

        # --- 2. Zone Fichiers ---
        self.frame_files = ctk.CTkFrame(self)
        self.frame_files.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        self.lbl_files = ctk.CTkLabel(self.frame_files, text="Fichiers en attente (0)", font=("Roboto", 14))
        self.lbl_files.pack(pady=5)

        # Zone de texte en lecture seule pour lister les fichiers
        self.txt_files = ctk.CTkTextbox(self.frame_files, state="disabled", height=150)
        self.txt_files.pack(fill="both", expand=True, padx=10, pady=5)

        btn_box = ctk.CTkFrame(self.frame_files, fg_color="transparent")
        btn_box.pack(fill="x", pady=5)
        
        self.btn_add = ctk.CTkButton(btn_box, text="+ Ajouter Audio/Vidéo", command=self.add_files, fg_color="#2CC985", hover_color="#25A971")
        self.btn_add.pack(side="left", padx=10)
        
        self.btn_clear = ctk.CTkButton(btn_box, text="Vider la liste", command=self.clear_files, fg_color="#E74C3C", hover_color="#C0392B")
        self.btn_clear.pack(side="right", padx=10)

        # --- 3. Logs et Progression ---
        self.frame_log = ctk.CTkFrame(self, height=150)
        self.frame_log.pack(fill="x", padx=15, pady=(0, 15))

        self.txt_log = ctk.CTkTextbox(self.frame_log, state="disabled", height=100, font=("Consolas", 11))
        self.txt_log.pack(fill="both", padx=5, pady=5)

        self.progress_bar = ctk.CTkProgressBar(self.frame_log, mode="indeterminate")
        self.progress_bar.pack(fill="x", padx=5, pady=(0, 5))
        self.progress_bar.set(0)

        # --- 4. Bouton Action ---
        self.btn_run = ctk.CTkButton(self, text="LANCER LA TRANSCRIPTION", command=self.start_thread, height=50, font=("Roboto", 16, "bold"))
        self.btn_run.pack(fill="x", padx=30, pady=(0, 20))

    # --- LOGIQUE UI ---

    def log(self, message):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.txt_log.configure(state="normal")
        self.txt_log.insert("end", f"[{timestamp}] {message}\n")
        self.txt_log.see("end")
        self.txt_log.configure(state="disabled")

    def add_files(self):
        files = filedialog.askopenfilenames(filetypes=[("Media", "*.mp3 *.wav *.m4a *.mp4 *.mkv *.flac"), ("Tous", "*.*")])
        if files:
            for f in files:
                if f not in self.files_to_process:
                    self.files_to_process.append(f)
            self.refresh_file_list()

    def clear_files(self):
        self.files_to_process = []
        self.refresh_file_list()

    def refresh_file_list(self):
        self.txt_files.configure(state="normal")
        self.txt_files.delete("1.0", "end")
        for f in self.files_to_process:
            self.txt_files.insert("end", f"📄 {os.path.basename(f)}\n")
        self.txt_files.configure(state="disabled")
        self.lbl_files.configure(text=f"Fichiers en attente ({len(self.files_to_process)})")

    def save_settings(self):
        # Sauvegarde la config actuelle pour la prochaine fois
        new_conf = {
            "engine": self.cb_engine.get(),
            "model_size": self.cb_model.get(),
            "language": self.cb_lang.get(),
            "export_format": self.cb_format.get()
        }
        ConfigManager.save(new_conf)

    def start_thread(self):
        if not self.files_to_process:
            messagebox.showwarning("Attention", "Aucun fichier sélectionné.")
            return
        
        self.save_settings()
        
        # Bloquer UI
        self.btn_run.configure(state="disabled", text="Traitement en cours...")
        self.btn_add.configure(state="disabled")
        self.progress_bar.start()

        threading.Thread(target=self.process_files, daemon=True).start()

    def process_files(self):
        engine_choice = self.cb_engine.get()
        model_choice = self.cb_model.get()
        lang_choice = self.cb_lang.get()
        format_choice = self.cb_format.get()

        try:
            # 1. Charger le modèle
            self.backend.load_model(engine_choice, model_choice, self.log)

            # 2. Traiter chaque fichier
            for i, filepath in enumerate(self.files_to_process):
                self.log(f"--- Fichier {i+1}/{len(self.files_to_process)} ---")
                try:
                    start_t = time.time()
                    
                    # Transcription
                    segments = self.backend.transcribe(filepath, lang_choice, self.log)
                    
                    # Export
                    self.backend.export_file(segments, filepath, format_choice)
                    
                    duration = time.time() - start_t
                    self.log(f"✅ Terminé en {duration:.2f}s.")
                
                except Exception as e:
                    self.log(f"❌ Erreur sur {os.path.basename(filepath)}: {e}")

            self.log("🎉 Tout est terminé !")
            messagebox.showinfo("Succès", "Transcriptions terminées avec succès.")

        except Exception as e:
            self.log(f"🔥 Erreur Critique : {e}")
            messagebox.showerror("Erreur", str(e))

        finally:
            # Rétablir UI
            self.progress_bar.stop()
            self.btn_run.configure(state="normal", text="LANCER LA TRANSCRIPTION")
            self.btn_add.configure(state="normal")


if __name__ == "__main__":
    app = ModernApp()
    app.mainloop()