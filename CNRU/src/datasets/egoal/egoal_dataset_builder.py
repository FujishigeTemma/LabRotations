"""egoal dataset."""

import os
import re
from pathlib import Path

import tensorflow_datasets as tfds


class Builder(tfds.core.GeneratorBasedBuilder):
    """DatasetBuilder for egoal dataset."""

    VERSION = tfds.core.Version("1.0.0")
    RELEASE_NOTES = {
        "1.0.0": "Initial release.",
    }
    MANUAL_DOWNLOAD_INSTRUCTIONS = """
    TODO
    """

    # workaround
    pkg_dir_path = Path(__file__).parent

    def _info(self) -> tfds.core.DatasetInfo:
        """Returns the dataset metadata."""
        return self.dataset_info_from_configs(
            features=tfds.features.FeaturesDict(
                {
                    "video": tfds.features.Video(shape=(None, 720, 2560, 3)),
                }
            ),
            supervised_keys=None,
        )

    def _split_generators(self, dl_manager: tfds.download.DownloadManager):
        """Returns SplitGenerators."""
        path = dl_manager.manual_dir
        return {
            tfds.Split.TEST: path,
        }

    def _generate_examples(self, path):
        pattern = re.compile(r"torobo_eyes_(\d+)\.avi")

        file_count = sum(1 for filename in os.listdir(path) if pattern.match(filename))

        for i in range(file_count):
            filename = f"torobo_eyes_{i}.avi"
            yield (
                filename,
                {
                    "video": os.path.join(path, filename),
                },
            )
