
import mutagen.oggopus as mutagen
import os
import json
import shutil
import traceback
import re

#Path Names
STATUS_INFORMATION_FILENAME = "Status Information.json"
ARTIST_NAME_TRANSLATIONS_FILENAME = "artistnames.json"

#TODO Make sure that the count of songs in the output is the same as the songs in the input
#TODO Fix issue with the directory loop overwritting files with the same name
#TODO Delete the old metadata at the end since it's stored in the comment tag
#TODO Check for links (why??) in the metadata and remove them
#TODO Combine JSON file into one file

def write_JSON(location, data):
    with open("/".join([location, STATUS_INFORMATION_FILENAME]), "w") as f:
        json.dump(data, f, indent=4)

def access_artist_name_translations():
    global artist_name_translations
    artist_name_translations = {}
    try:
        with open("/".join([start_location, ARTIST_NAME_TRANSLATIONS_FILENAME]), encoding="UTF8") as f:
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


def check_japanese_characters(strings):
    #https://stackoverflow.com/questions/6787716/regular-expression-for-japanese-characters
    regex = r"[一-龠ぁ-ゔァ-ヴーａ-ｚＡ-Ｚ０-９々〆〤]+"
    return_array = []
    for string in strings:
        match = re.search(regex, string)
        if match != None:
            return_array.append(True)
        else:
            return_array.append(False)
    return return_array



def find_bracket_combination(text):
    for brackets in bracket_types:
        beginning_bracket_index = text.find(brackets[0])
        end_bracket_index = text.find(brackets[1], beginning_bracket_index)
        if beginning_bracket_index != -1 and end_bracket_index != -1:
            return [beginning_bracket_index, end_bracket_index]
    return 0

def remove_character(text, position):
    return text[:position] + text[(position + 1):]

def strip_brackets(text):
    pass



def clean_line(line):
    return_string = None

    for enumerator in enumerate(line):
        if line[enumerator[0]].isalnum():
            return_string = line[enumerator[0]:]
            break
    
    #TODO Get rid of spaces at the end and check for links

    if return_string is None:
        raise Exception("Could not find any alphanumeric character in the parsed line.")
    else:
        return return_string


#Modify the metadata term that was found in the description to the correct format
def parse_term_line(line, key):
    if key == "Artist":
        parsed_line = clean_line(line)
        while(find_bracket_combination(parsed_line) != 0):
            bracket_locations = find_bracket_combination(parsed_line)
            split_line = parsed_line.partition(parsed_line[bracket_locations[0]:(bracket_locations[1] + 1)])
            boolean_list = check_japanese_characters(split_line)
            if boolean_list[1] == False:
                parsed_line = (split_line[1])[1:-1]
            else:
                parsed_line = split_line[0] + split_line[2]

        #Check the final artist string against the list of artist names and translate it if it's found
        for artist in artist_name_translations:
            if artist["Correct Name"] == parsed_line:
                return parsed_line
            else:
                for name in artist["Possible Names"]:
                    if name == parsed_line:
                        return artist["Correct Name"]
        return parsed_line

    elif key == "Date":
        #: Aug 12, 2013 (Comiket 84) -- Matches 2013
        regex = r"20{1}\d{2}"
        match = re.search(regex, line)
        if match is not None:
            return match.group(0)
        else:
            return None

    else:
        return clean_line(line)


def parse_description(description, find_terms):
    return_dictionary = {}

    #TODO Might not be foolproof if there is a term that is matched in a sentence before the list of song information
    for key in find_terms.keys():
        for term in find_terms[key]:
            if description.find(term) != -1:
                term_line = (((description.partition(term))[2]).partition("\n"))[0]
                parsed_line = parse_term_line(term_line, key)
                if parsed_line is not None:
                    return_dictionary[key] = parsed_line
                break

    return return_dictionary


def change_opus_file(file_path):
    music_file = mutagen.OggOpus(file_path)

    upper_keys(music_file)
    music_file["COMMENT"] = create_comment(music_file)

    if "description" in music_file.keys():
        #Compare this against what is returned
        #TODO Make this mutable
        find_terms = {
            "Title": ["Title Translation", "Title"],
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
    #start_location is the main root directory that the program will scan from
    #output_folder_name is the name of the folder that the converted music files will be moved to
    #output_folder_location is the combination of the start_location and the output_folder_name
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