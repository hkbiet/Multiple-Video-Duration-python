import os
import cv2
import datetime
import argparse
import logging

class VideoDurationCalculator:
    """Initializes the VideoDurationCalculator object with the given filename."""
    def __init__(self, filename):
        self.filename = filename

    def calculate_duration(self):
        """Calculates the duration of the video file."""
        video = cv2.VideoCapture(self.filename)
        fps = video.get(cv2.CAP_PROP_FPS)
        frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
        try:
            seconds = frame_count / fps
        except ZeroDivisionError:
            return datetime.timedelta(seconds=0)
        return datetime.timedelta(seconds=seconds)


class DirectoryIterator:
    """Initializes the DirectoryIterator object with the given directory."""
    def __init__(self, directory):
        self.directory = directory
        self.logger = logging.getLogger(__name__)

    def iterate(self):
        """Iterates through the directory structure to calculate the total duration of all video files."""
        total_duration = datetime.timedelta(seconds=0)
        for root, dirs, files in os.walk(self.directory):
            self.logger.info(f"Current directory: {root}")
            self.logger.info(f"Subdirectories: {dirs}")
            self.logger.info(f"Files: {files}")
            for each_file in files:
                self.logger.debug(f"Processing File: {each_file}")
                video_file = os.path.join(root, each_file)
                video_duration_calculator = VideoDurationCalculator(video_file)
                total_duration += video_duration_calculator.calculate_duration()
            print("\n")
        return total_duration


def initialise_args():
    """Initializes the command-line arguments parser."""
    parser = argparse.ArgumentParser(description='Get flag values')
    parser.add_argument('-p', '--path', required=True, help='root directory for video files and sub directories')
    args = parser.parse_args()
    return args.path


def start(root_dir, debug=False):
    """Entry point function to start processing video files in the specified directory."""
    if debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    logging.basicConfig(level=log_level)

    directory_iterator = DirectoryIterator(root_dir)
    total_duration = directory_iterator.iterate()
    print(f"Total Video Duration: {total_duration}")

if __name__ == "__main__":
    root_directory = initialise_args()
    start(root_directory)
