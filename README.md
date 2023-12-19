  ____        _       _       _____                                      
 |  _ \      | |     | |     |  __ \                                     
 | |_) | __ _| |_ ___| |__   | |__) |___ _ __   __ _ _ __ ___   ___ _ __ 
 |  _ < / _` | __/ __| '_ \  |  _  // _ \ '_ \ / _` | '_ ` _ \ / _ \ '__|
 | |_) | (_| | || (__| | | | | | \ \  __/ | | | (_| | | | | | |  __/ |   
 |____/ \__,_|\__\___|_| |_| |_|  \_\___|_| |_|\__,_|_| |_| |_|\___|_|  

# Batch Rename Script

This Python script renames video files based on their metadata. It utilizes FFmpeg to extract metadata information from video files.

File format is as follows: {date}-{project}-{time}-{shot_class}-{shot_number}.{extension}

## Features

- Rename video files based on metadata information.
- Customize file naming using project name, shot class, time of day, etc.
- Enable debugging, log file output, and recursive file walk options.

## Requirements

- Python 3.x
- FFmpeg (Make sure it's installed and available in the system PATH)

## Usage

```bash
python BatchRename.py [-d] [-l] [-r] [-i INPUT_DIRECTORY]
```

The following options are available:

    -d or --debug: Enable debugging output.
    -l or --log: Enable log file output.
    -r or --recursive: Enable recursive file walk.
    -i INPUT_DIRECTORY or --input INPUT_DIRECTORY: Specify the input directory to process.