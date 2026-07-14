from pathlib import Path

SUPPORTED_VIDEO_EXTENSIONS = {
    ".mp4",
    ".mov",
    ".mkv",
    ".avi",
    ".wmv",
    ".flv",
    ".webm",
    ".m4v",
    ".mpeg",
    ".mpg",
}


def is_video(path: str | Path) -> bool:
    """
    Returns True if the supplied path appears to be
    a supported video file.
    """

    return Path(path).suffix.lower() in SUPPORTED_VIDEO_EXTENSIONS
