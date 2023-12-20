![Wordmark](https://github.com/kolapy/BatchRename/blob/main/batchrenamer.png)

# Batch Rename Script

This Python script renames video files based on their metadata. It utilizes FFmpeg to extract metadata information from video files.

File format is as follows: {date}_{project}_{sub-folder-path}_{time}_{shot_class}_{shot_number}.{extension}

## Features

- Rename video files based on metadata information.
- Customize file naming using project name, shot class, time of day, etc.
- Enable debugging, log file output, and recursive file walk options.
- Enable sub folder naming to maintain pre existing file organization.

## Requirements

- Python 3.x
- FFmpeg (Make sure it's installed and available in the system PATH)
- FFmpeg-python (pip install ffmpeg-python)
- Click (pip install click)

Also feel free to use the requirements.txt file.  Preferably in a Python virtual environment.

```bash
pip install -r requirements.txt
```

## Usage

```bash
python BatchRename.py [-s] [-d] [-l] [-r] [-i INPUT_DIRECTORY]
```

The following options are available:

    -d or --debug: Enable debugging output.
    -l or --log: Enable log file output.
    -r or --recursive: Enable recursive file walk.
    -s or --sub: Enable sub folder naming.
    -i INPUT_DIRECTORY or --input INPUT_DIRECTORY: Specify the input directory to process.

## Executable

The executable can be run from the terminal as well

```bash
BatchRename.exe [-s] [-d] [-l] [-r] [-i INPUT_DIRECTORY]
```

## Workflow

For the best results you should organize your raw footage into a sensible folder hierarchy before running this script.
In this case you would run with the -r and -s flags to search through and maintain that folder structure.  Also important to note that in this configuration you would want to run at the root of the hierarchy.