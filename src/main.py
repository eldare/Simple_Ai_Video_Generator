#!/usr/bin/env python3

#
#  main.py
#
#  Created by Eldar Eliav on 2023/05/11.
#

from os import path, makedirs
from log import log
from script_generator import ScriptGenerator
from script_narration import ScriptNarration
from captions_generator import CaptionsGenerator
from video_maker import VideoMaker

def main(channel_name: str, topic: str, voice_name: str, destination_dir: str):
    if not path.exists(destination_dir):
        makedirs(destination_dir)
        log.info(f"new destination directory created: {destination_dir}")

    log.info("STEP 1 - script")
    script, captions, _ = ScriptGenerator().generate(
        channel_name,
        topic,
        is_verbose_print = True
    )

    log.info("STEP 2 - narration")
    mp3_file_destination_with_extension = path.join(destination_dir, "awesome_voice.mp3")
    ScriptNarration().narrate(
        voice_name,
        script,
        mp3_file_destination_with_extension
    )

    log.info("STEP 3 - captions")
    generated_images_path_list = CaptionsGenerator().generate_captions(
        captions_string = captions,
        destination_dir = destination_dir,
        is_crop_to_ratio_16_9 = True
    )

    log.info("STEP 4 - video")
    VideoMaker().create_video(
        images_list = generated_images_path_list,
        mp3_audio_file_path = mp3_file_destination_with_extension,
        mp4_file_destination_with_extension = path.join(destination_dir, "video.mp4"),
        is_duplicate_images_count_to_improve_smoothness = True
    )

if __name__ == "__main__":
    main(
        channel_name = "THE AWESOME YOUTUBE CHANNEL",
        topic = "Explore the idea of how awesome it could be if everyone was awesome to one another.",
        voice_name = "Adam",
        destination_dir = "./demo_output/"
    )
