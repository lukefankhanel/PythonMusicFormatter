
import mutagen.oggopus as mutagen
import os
import json
import shutil
import traceback

#Path Names
STATUS_INFORMATION_FILENAME = "Status Information.json"
ARTIST_NAME_TRANSLATIONS_FILENAME = "artistnames.json"

#TODO Make sure that the count of songs in the output is the same as the songs in the input
#TODO Fix issue with the directory loop overwritting files with the same name
#TODO Delete the old metadata at the end since it's stored in the comment tag

def write_JSON(location, data):
    with open("/".join([location, STATUS_INFORMATION_FILENAME]), "w") as f:
        json.dump(data, f, indent=4)

def access_artist_name_translations():
    global artist_name_translations
    artist_name_translations = {}
    try:
        with open("/".join([start_location, ARTIST_NAME_TRANSLATIONS_FILENAME])) as f:
            artist_name_translations = json.load(f)
        return True
    except OSError:
        return False


def upper_keys(music_file):
    for key in music_file.keys():
        music_file[key.upper()] = music_file.pop(key)

def create_comment(music_file):
    #print("EDITING FILE: " + music_file.filename)
    values = ["---ORIGINAL METADATA---"]
    for key in music_file.keys():
        #print("EDITING KEY: " + key)
        #print(music_file[key])

        values_list = []
        for counter in range(len(music_file[key])):
            values_list.append("".join(["VALUE ", str(counter + 1), ": ", music_file[key][counter]])) # VALUE 1: {}

        values.append(" ".join(["KEY=", key, ":", "VALUES=", "".join(values_list)])) # KEY= {} : VALUES= VALUE 1: {} \n
    return "\n".join(values)


def parse_line(line):
    for counter in range(len(line)):
        if line[counter].isalnum():
            return line[counter:]
    raise Exception("Could not find any alphanumeric character in the parsed line.")

def parse_term_line(line, key):
    if key == "Artist":
        parsed_line = parse_line(line)
        for brackets in bracket_types:
            beginning_bracket_index = parsed_line.find(brackets[0])
            end_bracket_index = parsed_line.find(brackets[1], beginning_bracket_index)
            if beginning_bracket_index != -1 and end_bracket_index != -1:
                parsed_line = parsed_line[beginning_bracket_index + 1 : end_bracket_index]
            print(parsed_line)
            #Find out how to check if a character is Japanese
    
    #Check the final artist string against the list of artist names and translate it if it's found

    elif key == "Date":
        pass
    else:
        return parse_line(line)


def parse_description(description, find_terms):
    return_dictionary = {}


    for key in find_terms.keys():
        for term in find_terms[key]:
            if description.find(term) != -1:
                term_line = (((description.partition(term))[2]).partition("\n"))[0]
                return_dictionary[key] = parse_term_line(term_line, key)
                break

    return return_dictionary


def change_opus_file(file_path):
    music_file = mutagen.OggOpus(file_path)

    upper_keys(music_file)
    music_file["COMMENT"] = create_comment(music_file)

    if "description" in music_file.keys():
        #Compare this against what is returned
        find_terms = {
            "Title": ["Title"],
            "Album": ["Album"],
            "Artist": ["Artist", "Circle"],
            "Date": ["Date"],
            "Origin": ["Original", "Origin", "Source"]
        }
        print(parse_description(music_file["description"][0], find_terms))
    
    music_file.save()

    
        

def change_m4a_file(file_path):
    pass

def copy_file(original, destination):
    print(original + " : " + destination)
    shutil.copyfile(original, destination)

def move_file(original, destination):
    pass

def get_music_files_location_input():
    return input("What is the absolute path of the music folder?")


def get_output_file_name_input():
    return input("What is the name of the folder where the files will be moved to?")


def create_output_folders(location, directory_names):
    try:
        #directory_names = ["complete","partial","failure"]
        for name in directory_names:
            os.makedirs(location + "/" + name)
    except Exception:
        pass


def access_directory():
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
            create_output_folders(output_folder_location, ["complete","partial","failure"])
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
                    copy_file("".join([dirpath, "/", f]), "".join([output_folder_location, "/", f]))

                    change_opus_file("".join([output_folder_location, "/", f]))
                    
                    #Move file based on the success status

                    music_counter += 1
                elif f.endswith(".m4a"):
                    change_m4a_file(dirpath + "/" + f)
                    music_counter += 1
                
            
            directory_counter += 1


        JSON_data["statistics"] = {
                "Number of directories parsed": directory_counter,
                "Number of music files parsed": music_counter
            }

        print("Writing JSON status information...")
        write_JSON(output_folder_location, JSON_data)
        return 0
    except Exception:
        print(traceback.print_exc())
        return 1


    

def main():
    global start_location, output_folder_name, output_folder_location, bracket_types

    start_location = get_music_files_location_input() 
    output_folder_name = get_output_file_name_input() 
    output_folder_location = "".join([start_location, "/", output_folder_name])
    
    #TODO make the bracket types read from a file
    bracket_types = [["(", ")"], ["「", "」"], ["【", "】"]]

    if access_artist_name_translations():
        print("Found Artist Names file!")
    else:
        print("Could not find Artist Names file... (artistnames.json)")

    if access_directory() == 0:
        print("Success!")
    else:
        print("Failure")


if __name__ == "__main__":
    main()