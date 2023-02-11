#!/usr/bin/env python3

import argparse
import logging
import sys
import os
import multiprocessing



from lib.ffmpeg import FFMpegFile, FFMpegFileError, CMDError

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)

parser = argparse.ArgumentParser()
parser.add_argument('-r', '--root-dir', type=str, required=False, default='/workdir', help='Root directory to search for files')

args = parser.parse_args(sys.argv[1:])

files = []
for root,d_names,f_names in os.walk(os.path.abspath(args.root_dir)):
    for f in f_names:
        fpath = os.path.join(root, f)
        try:
            ffmpeg_file = FFMpegFile(fpath)
            if ffmpeg_file.is_video:
                for data in ffmpeg_file.convert(threads=multiprocessing.cpu_count()):
                    progress = data['progress']
                    logging.info(f'Conversion progress {progress}%.')
                files.append()
        except FFMpegFileError:
            pass

