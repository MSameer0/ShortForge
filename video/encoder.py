import sys
import ffmpeg
import imageio_ffmpeg
import os
from utils.project import active_project


def get_font_file(font_family: str) -> str:
    """Finds the actual .ttf/.otf file for a given font family name."""
    if sys.platform == "win32":
        import winreg
        try:
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts",
            )
            i = 0
            while True:
                try:
                    name, value, _ = winreg.EnumValue(key, i)
                    if font_family.lower() in name.lower():
                        if not os.path.isabs(value):
                            font_path = os.path.join(
                                os.environ.get("WINDIR", "C:\\Windows"), "Fonts", value
                            )
                        else:
                            font_path = value
                        return font_path.replace("\\", "/")
                except OSError:
                    break
                i += 1
        except Exception:
            pass
        return "C:/Windows/Fonts/arial.ttf"
    elif sys.platform == "darwin":
        # Fallback for mac
        return "/System/Library/Fonts/Helvetica.ttc"
    else:
        # Fallback for linux
        return "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def export_short(output_path: str):
    if not active_project.video_path:
        return

    start_sec = active_project.trim_start_ms / 1000.0
    end_sec = active_project.trim_end_ms / 1000.0

    # Input video stream
    stream = ffmpeg.input(active_project.video_path, ss=start_sec, to=end_sec)
    v = stream.video
    a = stream.audio

    target_w, target_h = active_project.export_width, active_project.export_height

    if active_project.blur_background:
        # Background: scale to fit height, crop to target width/height, blur
        bg = (
            v.filter("scale", -1, target_h)
            .filter("crop", target_w, target_h)
            .filter("boxblur", luma_radius=active_project.blur_intensity)
        )
        # Foreground: scale to fit width
        fg = v.filter("scale", target_w, -1)
        # Overlay fg onto bg in the center
        v = ffmpeg.overlay(bg, fg, x="(main_w-overlay_w)/2", y="(main_h-overlay_h)/2")
    else:
        # Scale to fit width and pad with black bars
        v = v.filter("scale", target_w, -1).filter(
            "pad",
            width=target_w,
            height=target_h,
            x="(ow-iw)/2",
            y="(oh-ih)/2",
            color="black",
        )

    # Add text layers
    trim_duration_sec = (
        active_project.trim_end_ms - active_project.trim_start_ms
    ) / 1000.0
    for layer in active_project.text_layers:
        t_start = max(0.0, (layer.start_ms - active_project.trim_start_ms) / 1000.0)
        t_end = max(0.0, (layer.end_ms - active_project.trim_start_ms) / 1000.0)

        if t_end <= 0 or t_start >= trim_duration_sec:
            continue

        x_pos = int(target_w * layer.x_position_ratio)
        y_pos = int(target_h * layer.y_position_ratio)

        preview_w = max(active_project.preview_canvas_w, 1)
        export_font_size = int(layer.font_size * (target_w / preview_w))

        font_path = get_font_file(layer.font_family)

        v = v.drawtext(
            text=layer.text,
            fontfile=font_path,
            fontsize=export_font_size,
            fontcolor=layer.color,
            x=f"{x_pos}-(text_w/2)",
            y=f"{y_pos}-(text_h/2)",
            enable=f"between(t,{t_start},{t_end})",
            borderw=layer.stroke_width * 2,
            bordercolor=layer.stroke_color,
        )

    # Output stream
    out = ffmpeg.output(
        v, a, output_path, vcodec="libx264", acodec="aac", strict="experimental", r=active_project.export_fps
    )

    # Run the FFmpeg command using the bundled ffmpeg binary
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    ffmpeg.run(out, cmd=ffmpeg_exe, overwrite_output=True)
