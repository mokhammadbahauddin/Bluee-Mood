"""
CustomTkinter Visualizer UI Components (Oceanova Theme Edition)
Provides canvas-based visualizer widgets with Blue-White Gradient.
"""

import customtkinter as ctk
import numpy as np


class AudioVisualizer(ctk.CTkCanvas):
    """
    Real-time audio visualizer canvas with Oceanova Blue-White Gradient.
    """

    def __init__(self, master, visualizer_engine, mode='bars', **kwargs):
        # Default canvas settings
        default_kwargs = {
            'width': 600,
            'height': 200,
            'bg': '#1E1A3D', # Background Gelap sesuai tema
            'highlightthickness': 0
        }
        default_kwargs.update(kwargs)

        super().__init__(master, **default_kwargs)

        self.engine = visualizer_engine
        self.mode = mode
        self.animating = False
        self.animation_id = None

        # Animation settings
        self.fps = 45
        self.frame_delay = int(1000 / self.fps)

        self.bind('<Configure>', self._on_resize)

    def start_animation(self):
        if not self.animating:
            self.animating = True
            self._animate()

    def stop_animation(self):
        self.animating = False
        if self.animation_id:
            self.after_cancel(self.animation_id)
            self.animation_id = None
        self.delete('all')

    def _animate(self):
        if not self.animating: return
        self._render_bars() # Kita fokus ke mode bars saja untuk beat detection
        self.animation_id = self.after(self.frame_delay, self._animate)

    def _get_ocean_gradient(self, intensity):
        """
        Menghasilkan warna gradasi dari Biru Laut (#2E86DE) ke Putih (#FFFFFF)
        berdasarkan intensitas (0.0 - 1.0).
        """
        # Batasi intensitas max 1.0
        if intensity > 1.0: intensity = 1.0
        if intensity < 0.0: intensity = 0.0

        # Warna Awal (Biru Laut Oceanova) - RGB: (46, 134, 222) -> Hex #2E86DE
        r1, g1, b1 = 46, 134, 222

        # Warna Akhir (Putih Buih) - RGB: (255, 255, 255) -> Hex #FFFFFF
        r2, g2, b2 = 255, 255, 255

        # Hitung campuran warna
        r = int(r1 + (r2 - r1) * intensity)
        g = int(g1 + (g2 - g1) * intensity)
        b = int(b1 + (b2 - b1) * intensity)

        # Format ke Hex string
        return f"#{r:02x}{g:02x}{b:02x}"

    def _render_bars(self):
        """Render bars dari tengah (Center-Out) dengan gradasi Biru-Putih."""
        self.delete('all')

        spectrum = self.engine.get_spectrum()
        if len(spectrum) == 0:
            return

        canvas_width = self.winfo_width()
        canvas_height = self.winfo_height()
        center_x = canvas_width / 2

        num_bars = len(spectrum)
        vis_width = canvas_width * 0.9
        bar_width = (vis_width / 2) / num_bars

        gap = 2
        actual_bar_width = bar_width - gap
        if actual_bar_width < 1: actual_bar_width = 1

        for i, value in enumerate(spectrum):
            # Tinggi Bar
            bar_height = value * canvas_height * 0.8
            if bar_height < 4: bar_height = 4

            y_start = canvas_height
            y_end = canvas_height - bar_height

            # --- BAGIAN GRADASI ---
            # Semakin tinggi bar (value besar), semakin putih warnanya.
            # Kita boost sedikit value-nya agar warna putih lebih mudah muncul saat beat drop.
            color_intensity = value * 1.2
            fill_color = self._get_ocean_gradient(color_intensity)
            # ----------------------

            # Posisi X Kanan
            x_right = center_x + (i * bar_width)
            self.create_rectangle(
                x_right, y_end,
                x_right + actual_bar_width, y_start,
                fill=fill_color, outline=""
            )

            # Posisi X Kiri (Mirror)
            x_left = center_x - ((i + 1) * bar_width)
            self.create_rectangle(
                x_left, y_end,
                x_left + actual_bar_width, y_start,
                fill=fill_color, outline=""
            )

    def _on_resize(self, event):
        pass

    def set_mode(self, mode):
        pass # Fitur mode dimatikan sementara untuk fokus ke beat bars


# Kelas Fullscreen (Jika masih diperlukan)
class FullscreenVisualizer(ctk.CTkToplevel):
    def __init__(self, parent, visualizer_engine, song_title="Now Playing"):
        super().__init__(parent)
        self.title("Visualizer")
        self.geometry("1200x800")
        self.configure(fg_color="#0A0A0A")

        self.visualizer = AudioVisualizer(
            self,
            visualizer_engine,
            width=1200,
            height=600,
            bg='#0A0A0A'
        )
        self.visualizer.pack(fill="both", expand=True, padx=20, pady=20)
        self.visualizer.start_animation()
        self.bind('<Escape>', lambda e: self.destroy())