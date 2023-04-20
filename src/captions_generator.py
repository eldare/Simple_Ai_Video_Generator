#
#  captions_generator.py
#
#  Created by Eldar Eliav on 2023/05/13.
#

from os import path
from PIL import Image
from dalle2_image_generator import Dalle2ImageGenerator

# TODO - speed this up by making all requests in parallel

# TODO - retry if network fails

class CaptionsGenerator:
    # api memthods
    def generate_captions(
        self,
        captions_string: str,
        destination_dir: str,
        is_crop_to_ratio_16_9: bool = False
    ) -> list[str]:
        # returns a list of paths to the generated images
        list_of_created_image_files: list[str] = []
        captions_list = self._convert_string_into_list(captions_string)
        image_generator = Dalle2ImageGenerator()
        for index, caption in enumerate(captions_list):
            image_file_path = path.join(destination_dir, f"caption_{index}.jpg")
            try:
                image_generator.generate_image_and_download(
                    image_file_destination_with_extension = image_file_path,
                    prompt = caption
                )
                if is_crop_to_ratio_16_9:
                    self._crop_image_to_ratio_16_9(image_file_path, image_file_path)
                list_of_created_image_files.append(image_file_path)
            except Exception as error:
                print(f"skiping {image_file_path} - {error}")
        return list_of_created_image_files

    # private methods
    def _convert_string_into_list(self, captions_string: str) -> list[str]:
        captions_list = [caption.strip() for caption in captions_string.strip().split('\n') if caption]
        return [caption.strip() for caption in captions_list]

    def _crop_image_to_ratio_16_9(self, source_image_file_path: str, destination_image_file_path: str):
        image = Image.open(source_image_file_path)
        width, height = image.size

        total_to_crop = height - (height * 9/16)
        top = int(total_to_crop * 1/4)
        bottom = int(height - total_to_crop * 3/4)

        cropped_image = image.crop((0, top, width, bottom))
        cropped_image.save(destination_image_file_path)
