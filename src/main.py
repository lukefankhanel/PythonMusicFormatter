

def get_music_files_location_input():
    return input("What is the absolute path of the music folder?")


def get_output_file_name_input():
    return input("What is the name of the folder where the files will be moved to?")


def main():
    get_music_files_location_input()
    get_output_file_name_input()

if __name__ == "__main__":
    main()