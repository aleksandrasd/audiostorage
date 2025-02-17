import subprocess

from core.audio_editor import AudioMeta, ConversionStrategy


class FFmpegWAVConversion(ConversionStrategy):
    def convert(self, file_path: str, output_path: str, **kwargs) -> None:
        cmd = [
            "ffmpeg",
            "-i",
            file_path,
            "-vn",
            "-acodec",
            "pcm_s16le",
            "-ar",
            "44100",
            "-ac",
            "2",
            output_path,
        ]
        subprocess.run(cmd, check=True)


class FFmpegMP3Conversion(ConversionStrategy):
    def convert(self, file_path: str, output_path: str, **kwargs) -> None:
        bitrate = kwargs.get("bitrate", "320k")
        cmd = [
            "ffmpeg",
            "-i",
            file_path,
            "-vn",
            "-acodec",
            "libmp3lame",
            "-ab",
            bitrate,
            "-ar",
            "44100",
            "-ac",
            "2",
            output_path,
        ]
        subprocess.run(cmd, check=True)


class FFmpegAudioMeta(AudioMeta):
    def get_audio_duration(self, file_path: str) -> float:
        cmd = [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            file_path,
        ]
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        return float(output.decode("utf-8").strip())
