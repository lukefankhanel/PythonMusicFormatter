
import mutagen
import os
import json

def write_JSON(location, data):
    with open(location + "/Status Information.json", "w") as f:
        json.dump(data, f, indent=4)

def copy_opus_file(file_path):
    pass

def copy_m4a_file(file_path):
    pass

def copy_file():
    pass

def get_music_files_location_input():
    return input("What is the absolute path of the music folder?")


def get_output_file_name_input():
    return input("What is the name of the folder where the files will be moved to?")


def create_output_files(location, output_name, JSON_data):
    try:
        directory_names = ["complete","partial","failure"]
        for name in directory_names:
            os.makedirs(location + "/" + output_name + "/" + name)
    except Exception:
        pass


def access_directory(start_location, output_folder_name):
    try:
        JSON_data = {}
        JSON_data["statistics"] = {}
        JSON_data["success"] = []
        JSON_data["partial"] = []
        JSON_data["failure"] = []
        # JSON_data["success"].append(
        #     {"fileName" : "Testfile",
        #     "successStatus": "1"})

        if os.path.isdir(start_location):
            print("Creating output folders...")
            create_output_files(start_location, output_folder_name, JSON_data)
        else:
            return 1

        directory_counter = 0
        music_counter = 0
        for (dirpath, dirnames, filenames) in os.walk(start_location):
            print(dirnames)
            if directory_counter == 0:
                dirnames.remove(output_folder_name)
            for f in filenames:
                if f.endswith(".opus"):
                    copy_opus_file(dirpath + "/" + f)
                    music_counter = music_counter + 1
                elif f.endswith(".m4a"):
                    copy_m4a_file(dirpath + "/" + f)
                    music_counter = music_counter + 1
                
            
            directory_counter = directory_counter + 1


        JSON_data["statistics"] = {
                "Number of directories parsed": directory_counter,
                "Number of music files parsed": music_counter
            }

        print("Writing JSON status information...")
        write_JSON(start_location + "/" + output_folder_name, JSON_data)
        return 0
    except Exception:
        return 1


    

def main():
    start_location = get_music_files_location_input()
    output_folder_name = get_output_file_name_input()

    if access_directory(start_location, output_folder_name) == 0:
        print("Success!")
    else:
        print("Failure")


if __name__ == "__main__":
    main()