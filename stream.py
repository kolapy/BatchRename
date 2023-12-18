import ffmpeg
import sys

def extract_metadata(media_file):
    try:
        # Run ffprobe on the media file
        probe_data = ffmpeg.probe(media_file)

        # Print the entire probe_data
        print(probe_data)

        # Extract general stream information
        general_stream = next((stream for stream in probe_data.get("streams", []) if stream.get("@type") == "General"), {})

        # Extract extra information
        extra_info = general_stream.get("extra", {})

        # Combine general and extra information
        metadata = {**general_stream, **extra_info}

        return metadata

    except ffmpeg.Error as e:
        print(f"Error running ffprobe: {e.stderr.decode()}")
        return None

if __name__ == "__main__":
    # Check if a media file is provided as a command-line argument
    if len(sys.argv) < 2:
        print("Usage: python script_name.py path/to/your/media/file.mp4")
        sys.exit(1)

    # Get the path to the media file from the command line
    media_file = sys.argv[1]

    # Extract metadata from the media file
    metadata = extract_metadata(media_file)

    if metadata:
        # Print the extracted metadata
        for key, value in metadata.items():
            print(f"{key}: {value}")
    else:
        print("Failed to extract metadata.")
