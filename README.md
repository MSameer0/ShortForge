# ShortForge

A lightweight desktop editor for converting landscape videos into vertical Shorts, TikToks and Reels.

---

## What is ShortForge?

If you've got a landscape (16:9) video — a podcast clip, a gaming highlight, a talk, a tutorial — and you want it as a clean vertical video for YouTube Shorts, TikTok, or Instagram Reels, ShortForge does the reframing for you. It's a free, open-source desktop app: no uploading your footage to some website, no watermarks, no subscription.

Bring in a video from your computer or paste in a URL, trim it down, reframe it for vertical, add captions or text if you want, and export — all in one simple window.

### Features

- **Import from anywhere** — open a local video file, or paste a URL and let ShortForge download it for you
- **Live preview** — see exactly what your vertical video will look like as you edit
- **Trim & timeline editing** — cut your clip down to the part that matters
- **Smart reframing** — convert 16:9 footage to vertical with a blurred background fill or a plain black background
- **Text overlays** — add titles or captions with custom fonts
- **Flexible output** — export at 720×1280, 1080×1920, or 1440×2560
- **Light & dark themes** — pick whichever is easier on your eyes
- **No watermarks, no cloud** — everything runs locally on your machine

### Getting started

1. Head to the [Releases page](https://github.com/MSameer0/ShortForge/releases) and download the build for your OS (Windows, macOS, or Linux).
2. Run the app — no installation required.
3. Click **Import**, choose a video file or paste a URL, and start editing.
4. Use the timeline to trim your clip, pick a reframing mode, and add any text you'd like.
5. Hit **Export** and choose your output resolution.

That's it — your vertical video will be saved to your computer, ready to upload.

> **Note:** Downloading videos from a URL is subject to that platform's own terms of service — make sure you have the rights to use whatever you download.

---

## For developers

ShortForge is a Python desktop application built with **PySide6** (Qt for Python). Video processing is handled with **OpenCV**, **ffmpeg-python**, and **imageio-ffmpeg**, and URL imports go through **yt-dlp**.

### Tech stack

| Purpose | Library |
|---|---|
| GUI framework | PySide6 (Qt6) |
| Video decoding/frame processing | OpenCV, numpy |
| Encoding/export | ffmpeg-python, imageio-ffmpeg |
| URL-based media import | yt-dlp |

### Project structure

```
ShortForge/
├── main.py                  # Entry point — boots the QApplication and MainWindow
├── ui/                      # Windows, dialogs, panels, and styling
│   ├── main_window.py
│   ├── menu_bar.py
│   ├── preview.py
│   ├── timeline.py
│   ├── settings_panel.py
│   ├── project_settings_dialog.py
│   ├── import_url_dialog.py
│   ├── text_layer_dialog.py
│   ├── theme_dialog.py
│   ├── about_dialogue.py
│   └── styles.py
├── video/                   # Frame processing, encoding, previews
│   ├── encoder.py
│   ├── ffmpeg_runner.py
│   ├── filters.py
│   ├── preview_frame.py
│   ├── metadata.py
│   └── thumbnailer.py
├── widgets/                 # Reusable custom Qt widgets
│   ├── video_widget.py
│   ├── range_slider.py
│   ├── playback_bar.py
│   ├── seek_slider.py
│   ├── thumbnail_strip.py
│   ├── font_combo.py
│   ├── drop_area.py
│   ├── empty_state.py
│   └── loading_spinner.py
├── workers/                 # Background QThread workers (non-blocking I/O)
│   ├── download_worker.py   # yt-dlp downloads
│   ├── export_worker.py     # Video export/encode jobs
│   └── thumbnail_worker.py
└── utils/                   # Shared helpers, app metadata, theming, project files
    ├── app_info.py
    ├── constants.py
    ├── theme_manager.py
    ├── project.py
    ├── media.py
    ├── settings.py
    ├── file_utils.py
    └── time_utils.py
```

Long-running work (downloads, exports, thumbnail generation) runs on dedicated `workers/` threads so the UI never freezes.

### Running from source

Requires Python 3.12+ and [FFmpeg](https://ffmpeg.org/) available on your system (or bundled via `imageio-ffmpeg`).

```bash
git clone https://github.com/MSameer0/ShortForge.git
cd ShortForge
pip install -r requirements.txt
python main.py
```

### Building a standalone executable

Releases are built with [PyInstaller](https://pyinstaller.org/) — see `.github/workflows/release.yml` for the exact CI steps. To build locally:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --collect-binaries imageio_ffmpeg --name shortforge main.py
```

Pushing a `v*` tag (e.g. `v1.0.1`) triggers the release workflow, which builds Windows, macOS, and Linux binaries and attaches them to a GitHub Release automatically.

### Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide. In short:

1. Fork the repo and branch off `main`.
2. Install dependencies with `pip install -r requirements.txt`.
3. Format your code with [Black](https://github.com/psf/black) (`black .`) before opening a PR.
4. Keep UI contributions consistent with the existing dark theme aesthetic.

Bug reports and feature requests are also welcome via [Issues](https://github.com/MSameer0/ShortForge/issues).

---

Made by [Muhammad Sameer Adnan](https://github.com/MSameer0)
