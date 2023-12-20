import ffmpeg
from datetime import datetime
import os
import click
import shutil


#--------------------------------- FUNCTIONS -----------------------------

# Fucntion for extracting the meta data and formating it inside a python disctonary
def extract_metadata(media_file):
    try:
        # Run ffprobe on the media file
        probe_data = ffmpeg.probe(media_file)

        # Access information about the first video stream (assuming it exists)
        video_stream = next((stream for stream in probe_data.get("streams", []) if stream.get("codec_type") == "video"), {})
        #general_stream = next((stream for stream in probe_data.get("streams", []) if stream.get("@type") == "General"), {})

        # Extract specific data from the video stream
        video_duration = video_stream.get("duration", "N-A")
        video_codec = video_stream.get("codec_name", "N-A")
        width = video_stream.get("width", "N-A")
        height = video_stream.get("height", "N-A")

        # Extract creation time from the tags
        tags = video_stream.get("tags", {})
        encoded_date = tags.get("creation_time", "N-A")

        # Access information about the format (container)
        format_info = probe_data.get("format", {})

        

        # Extract focal length from the format tags
        format_tags = format_info.get("tags", {})
        #VERY IMPORTANT - use. instead of _ for the format meta data. Use Media info app in HTML view for the proper names.
        focal_length = format_tags.get("com.blackmagic-design.camera.lensFocalLength", "N-A")

        # Create a dictionary with extracted data
        metadata = {
            "Video Duration": video_duration,
            "Video Codec": video_codec,
            "Date": encoded_date,
            "Width": width,
            "Height": height,
            "Focal Length": focal_length,
        }

        return metadata

    except ffmpeg.Error as e:
        print(f"Error running ffprobe: {e.stderr}")
        return {}

# Function for determining if the shot is WS, MS, or CU
def classify_shot(focal_length):
    try:
        focal_length = float(focal_length[:-2])  # Convert to float, removing 'mm'
        if focal_length < 35:
            return "WS"
        elif 35 <= focal_length <= 85:
            return "MS"
        else:
            return "CU"
    except ValueError:
        return "N-A"  # If focal length is not a valid number

# Function for determining if the shot was in the AM or PM.   USING UTC,  May need to adjust this to detect time zone?
def classify_time_of_day(date_string):
    try:
        # Convert the ISO 8601 formatted date string to a datetime object
        date_object = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")

        # Extract the hour from the datetime object
        hour = date_object.hour

        # Classify the time of day based on the hour
        if 6 <= hour < 12:
            return "AM"
        elif 12 <= hour < 18:
            return "PM"
        else:
            return "NT" #NT for night???  sure.
    except ValueError:
        return "N-A"  # If date format is not as expected

#--------------------------------- MAIN LOGIC -----------------------------
@click.command(help="This script renames video files based on their metadata.")
#@click.argument('input_directory', type=click.Path(exists=True))
@click.option('-d','--debug', is_flag=True, help='Enable debugging output.')
@click.option('-l','--log', is_flag=True, help='Enable log file output.')
@click.option('-r','--recursive', is_flag=True, help='Enable recursive file walk.')
@click.option('-i', '--input', type=click.Path(exists=True), help='Input directory to process.')
@click.option('-s','--sub', is_flag=True, help='Enable sub folder naming.')

def main(debug,log,recursive,input,sub):
    wordmark= r"""
  ____        _       _       _____                                      
 |  _ \      | |     | |     |  __ \                                     
 | |_) | __ _| |_ ___| |__   | |__) |___ _ __   __ _ _ __ ___   ___ _ __ 
 |  _ < / _` | __/ __| '_ \  |  _  // _ \ '_ \ / _` | '_ ` _ \ / _ \ '__|
 | |_) | (_| | || (__| | | | | | \ \  __/ | | | (_| | | | | | |  __/ |   
 |____/ \__,_|\__\___|_| |_| |_|  \_\___|_| |_|\__,_|_| |_| |_|\___|_|                                                                                                                                                  
"""
    click.secho(wordmark, fg="green",bold=True, blink=True) #Print the wordmark

    input_directory = input or click.prompt('Enter the input directory', type=click.Path(exists=True))#Default option

    click.echo(f"The input directory is: {click.style(input_directory, fg='green')}")

    print("Please pick a name for this project")
    # Prompt the user for the project name
    project_name = click.prompt('Enter the project name')
    try:
        if not os.path.exists(input_directory):
            raise FileNotFoundError(f"The directory '{input_directory}' does not exist.")
        
        shot_number_int = 0 #initialize this variable
        # Get the list of files in the directory
        files = os.listdir(input_directory)
        num_files = 0
        
        renamed_files = [] #Initialize the renamed list

        if recursive:
            walker = os.walk(input_directory)
        else:
            walker = [(input_directory, [], files) for _, _, files in os.walk(input_directory)]

        # Iterate over the files in the directory
        for root, dirs, files in walker:
            for file_name in files:
                # Construct the full path to the file
                file_path = os.path.join(root, file_name)
                # Check if the item is a file (not a directory)
                if os.path.isfile(file_path):
                    # Check if the file has a valid video extension
                    valid_extensions = {".mov", ".mp4", ".avi", ".mkv", ".flv"}  # Add or modify as needed
                    _, file_extension = os.path.splitext(file_path)

                    if file_extension.lower() in valid_extensions:
                        # Extract metadata for the current file
                        metadata = extract_metadata(file_path)
                        num_files += 1
                        click.echo(f"{click.style('File to rename: ', fg='red')}{file_path}")

                        #-------------------DEBUGGING FLAG-----------------------
                        if debug:
                            click.secho("Debug mode enabled. Printing metadata:", fg='yellow',bold=True)
                            # Print the extracted metadata if available  (For debugging)
                            if metadata:
                                for key, value in metadata.items():
                                    #print(f"{key}: {value}")
                                    click.echo(f"{click.style(f'{key}: ', fg='yellow')}{value}")
                            else:
                                print("Failed to extract metadata.")
                        #-------------------DEBUGGING FLAG-----------------------
                                
                        
                        
                        # Check if the file has metadata
                        if metadata: #Only proceeds if we have meta data
                            # Extract relevant information
                            shot_class = classify_shot(metadata.get("Focal Length", "N-A"))
                            date = metadata.get("Date", "N-A")[:10] #Grabs the first 10 characters of the date string
                            date_string = metadata.get("Date", "N-A") # Assuming your date string is stored in the metadata dictionary
                            time_of_day_classification = classify_time_of_day(date_string)
                            #project_name = "OTW23" #THIS needs to be user input

                            #---- Increment shot number ----
                            shot_number_int += 1
                            shot_numberSTR = str(shot_number_int).zfill(3)
                            #---- Increment shot number ----

                            #---- Sub folder naming -----
                            if sub:
                                # Get the relative path from the input directory to the current file
                                relative_path = os.path.relpath(file_path, input_directory)

                                # Extract individual components from the relative path
                                path_components = relative_path.split(os.path.sep)[:-1]

                                #Hack for MacOs to drop the . from the start of the file path
                                if len(path_components) > 0 and path_components[0] ==".":
                                    path_components = path_components[1:]
                                    print("PATH IF 0",path_components)
                                
                                click.echo(f"{click.style('Path components: ', fg='yellow')}{path_components}")

                                # Use the extracted components in the new file name
                                num_components = len(path_components)
                                click.echo(f"{click.style('Num components: ', fg='yellow')}{num_components}")
                                sub_path = "_".join(path_components[-num_components:],)

                                #Only add the trailing underscore if the file is in a sub directory
                                if num_components > 0:
                                    sub_path += "_"
                                
                                click.echo(f"{click.style('Sub path: ', fg='yellow')}{sub_path}")
                            else:
                                sub_path = ""
                            #---- Sub folder naming -----

                            # Generate the new file name
                            new_file_name = f"{date}_{project_name}_{sub_path}{shot_class}_{time_of_day_classification}_{shot_numberSTR}{file_extension}"
                            click.echo(f"{click.style('New file name: ', fg='green')}{new_file_name}")

                            #Print a responsive seperation line
                            terminal_width, _ = shutil.get_terminal_size()
                            click.secho("-" * terminal_width, fg="green",bold=True)

        
                            # Construct the full path to the new file
                            new_file_path = os.path.join(root, new_file_name)

                            # Rename the file
                            os.rename(file_path, new_file_path)

                        #-------------------LOGGING FLAG-------------------------
                        if log:
                            # Create a log file
                            renamed_files.append(new_file_name)

                            # Save the list of renamed files to a text file
                            report_file_path = os.path.join(input_directory, "renamed_files_report.txt")

                            with open(report_file_path, 'w') as report_file:

                                # Add a title to the log file
                                report_file.write("Renamed Files Report\n")
                                report_file.write("=" * 20 + "\n\n")

                                # Add information about the script, date, etc.
                                report_file.write("Script: BatchRename.py\n")
                                report_file.write("Date: {}\n\n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

                                report_file.write("\n".join(renamed_files))
                        #-------------------LOGGING FLAG-------------------------
                    else:
                    #What to do with the non valid extensions
                        click.echo(f"{click.style('Non-video file: ', fg='yellow')}{file_path}")
           
        print(f"Number of files renamed: {num_files}")

    except Exception  as e:
        print(f"Error: {e}")

#---------------------------------------------------------------------------------

if __name__ == '__main__':
    main()
    pass