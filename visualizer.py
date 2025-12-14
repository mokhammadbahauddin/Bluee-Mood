"""
Optimized Audio Visualizer Engine (Beat Detection Focus)
"""

import numpy as np
import threading
import time
import pygame
import librosa

class VisualizerEngine:
    def __init__(self, sample_rate: int = 22050, chunk_size: int = 1024): # Chunk size lebih kecil = lebih responsif
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.num_bars = 40  # Kurangi bar agar lebih tebal dan jelas
        self.running = False
        self.thread = None

        # Audio Data
        self.audio_series = None
        self.track_duration = 0

        # Data Containers
        self.spectrum_data = np.zeros(self.num_bars)
        self.data_lock = threading.Lock()

        # --- BEAT LOGIC SETTINGS ---
        self.smoothing_factor = 0.4  # 0.0 = Instan, 1.0 = Beku. 0.4 pas untuk beat.
        self.previous_spectrum = np.zeros(self.num_bars)

        # Kita fokuskan bin frekuensi ke area Bass dan Mid (0 - 4000Hz)
        # karena disitulah "beat" berada. Treble tinggi seringkali cuma noise visual.
        self.freq_max_limit = 4000

    def load_track(self, file_path):
        def _load():
            try:
                # Load audio (Mono)
                y, sr = librosa.load(file_path, sr=self.sample_rate, mono=True)
                self.audio_series = y
                self.track_duration = librosa.get_duration(y=y, sr=sr)
                print(f"🎵 Visualizer: Track Loaded for Beat Detection")
            except Exception as e:
                print(f"❌ Load Error: {e}")
                self.audio_series = None

        threading.Thread(target=_load, daemon=True).start()

    def start(self):
        if self.running: return
        self.running = True
        self.thread = threading.Thread(target=self._processing_loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)

    def _processing_loop(self):
        while self.running:
            try:
                if self.audio_series is None or not pygame.mixer.music.get_busy():
                    # Efek turun perlahan saat lagu mati
                    with self.data_lock:
                        self.spectrum_data *= 0.8
                    time.sleep(0.03)
                    continue

                # 1. Ambil posisi waktu
                current_ms = pygame.mixer.music.get_pos()
                current_sec = current_ms / 1000.0

                # 2. Ambil sampel audio
                sample_idx = int(current_sec * self.sample_rate)

                if sample_idx + self.chunk_size < len(self.audio_series):
                    chunk = self.audio_series[sample_idx : sample_idx + self.chunk_size]

                    # 3. FFT (Analisis Frekuensi)
                    windowed_chunk = chunk * np.hanning(len(chunk))
                    fft_result = np.abs(np.fft.rfft(windowed_chunk))

                    # 4. Beat Processing (Kunci agar terasa "real")
                    # Kita hanya ambil sebagian frekuensi (frekuensi rendah/bass)
                    fft_len = len(fft_result)
                    relevant_len = int(fft_len * (self.freq_max_limit / (self.sample_rate / 2)))
                    fft_relevant = fft_result[:relevant_len]

                    # Resize array agar sesuai jumlah bar (40 bars)
                    # Kita pakai metode 'mean' untuk downsampling
                    if len(fft_relevant) > self.num_bars:
                        new_spectrum = np.array([np.mean(chunk) for chunk in np.array_split(fft_relevant, self.num_bars)])
                    else:
                        new_spectrum = np.zeros(self.num_bars)

                    # 5. Logarithmic Scaling (Agar suara kecil tetap terlihat)
                    new_spectrum = np.log10(new_spectrum + 1) * 0.8

                    # 6. Bass Boost Logic
                    # Bar awal (kiri) adalah bass. Kita cek energinya.
                    bass_energy = np.mean(new_spectrum[:5])
                    if bass_energy > 0.4:
                        new_spectrum *= 1.2 # Boost visual saat ada kick drum!

                    # Normalize (Max 1.0)
                    new_spectrum = np.clip(new_spectrum, 0, 1.0)

                    # 7. Smoothing (Exponential Moving Average)
                    # Ini membuat bar turunnya pelan, tapi naiknya cepat
                    smoothed = (self.previous_spectrum * self.smoothing_factor) + (new_spectrum * (1 - self.smoothing_factor))
                    self.previous_spectrum = smoothed

                    with self.data_lock:
                        self.spectrum_data = smoothed

                time.sleep(0.02) # ~50 FPS agar mulus

            except Exception as e:
                time.sleep(0.1)

    def get_spectrum(self):
        with self.data_lock:
            return self.spectrum_data.copy()

    def get_peaks(self):
        return self.spectrum_data # Placeholder