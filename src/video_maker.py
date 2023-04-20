#
#  video_maker.py
#
#  Created by Eldar Eliav on 2023/05/13.
#

from log import log
from os import path, system
from pydub import AudioSegment

class VideoMaker:
    def create_video(
        self,
        images_list: list[str],
        mp3_audio_file_path: str,
        mp4_file_destination_with_extension: str,
        is_duplicate_images_count_to_improve_smoothness: bool
    ):
        log.info("generating video...")

        tools_dir = "./tools"  # TODO - this path is problematice, because it cares from where the main.py is called
        maker_script = "maker.rb"

        audio_duration_in_seconds = self._get_audio_duration_in_seconds(mp3_audio_file_path)

        if is_duplicate_images_count_to_improve_smoothness:
            images_list = self._duplicate_images_list_by_factor(
                images_list = images_list,
                audio_duration_in_seconds = audio_duration_in_seconds
            )

        slide_duration = self._calculate_slide_daration_in_seconds(
            audio_duration_in_seconds = audio_duration_in_seconds,
            number_of_images = len(images_list)
        )

        images_string = " ".join(images_list)

        cmd = f'ruby {path.join(tools_dir, maker_script)} {images_string} {mp4_file_destination_with_extension} --size=1280x800 --slide-duration={slide_duration} --fade-duration=1 --zoom-rate=0.1 --zoom-direction=top-left-in --scale-mode=pad --fps=120 --audio={mp3_audio_file_path} -y'
        system(cmd)

        log.info(f"video generated: {mp4_file_destination_with_extension}")

    # private methods
    def _calculate_slide_daration_in_seconds(self, audio_duration_in_seconds: int, number_of_images: int) -> float:
        return audio_duration_in_seconds / number_of_images

    def _get_audio_duration_in_seconds(self, mp3_audio_file_path: str) -> int:
        audio_object = AudioSegment.from_file(mp3_audio_file_path, format="mp3")
        return audio_object.duration_seconds

    def _duplicate_images_list_by_factor(self, images_list: list[str], audio_duration_in_seconds: int) -> list[str]:
        images_count_duplication_factor = int(audio_duration_in_seconds / 6 / 10)
        return images_list * images_count_duplication_factor
