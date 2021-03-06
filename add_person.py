import os
from shutil import copyfile

import utils

PEOPLE_PATH = "./_people"
VALID_TITLES = [
    "Professor",
    "Associate Professor",
    "Assistant Professor",
    "Postdoc",
    "PhD Candidate",
    "PhD Student",
    "Researcher",
    "Master's Student",
    "Bachelor's Student",
    "High School Student"
]

TITLE_PRIORITIES = {k: v for k, v in zip(VALID_TITLES, 
                                         range(len(VALID_TITLES)))}


def name_to_person_filename(name):
    return name.replace(" ", "").lower().strip() + ".md"


def get_new_headshot_filename(name, headshot_path_old):
    name_stripped = name.replace(" ", "").lower().strip()
    _, extension = os.path.splitext(headshot_path)
    new_filename = name_stripped + extension
    return new_filename


# Ugly hack :()
def clean_url(url):
    if "https://" not in url or "http://" not in url:
        url = "https://" + url
    return url


def person_exists(name):
    person_path = os.path.join(PEOPLE_PATH, name_to_person_filename(name))
    return os.path.exists(person_path)


def build_person(name, headshot_path, title, website=None, research_areas="",
                 is_visiting=False): 
    if not website:
        website = None
    else:
        website = clean_url(website)
        
    if not research_areas:
        research_areas = None
    else:
        research_areas = research_areas.split(",")
    
    if not headshot_path == "":
        jeyll_config = utils.load_jeykll_config()
        headshots_dir = os.path.join(jeyll_config["RESOURCES_PATH"], "headshots")

        new_headshot_filename = get_new_headshot_filename(name, headshot_path)
        new_headshot_path = os.path.join(headshots_dir, new_headshot_filename)
        copyfile(headshot_path, new_headshot_path)
    else:
        new_headshot_filename = "dubs.png"

    person = {
        "name": name,
        "title": title,
        "site": website,
        "headshot": new_headshot_filename,
        "research_areas": research_areas,
        "priority": TITLE_PRIORITIES[title],
        "is_visiting": is_visiting
    }

    person_file_path = os.path.join(PEOPLE_PATH, name_to_person_filename(name))
    utils.dump_dict_to_yaml(person, person_file_path)
    return person_file_path


if __name__ == "__main__":
    print("---------------------------")
    print("""This script adds a new person to this site's 'Our Team' 
    section. Please provide the following information:""")
    print("---------------------------")

    name = input("Full Name:")
    if person_exists(name):
        print(name_to_person_filename(name), "already exists.")
        do_exit = not utils.y_or_n("Do you want to overwrite this user?")
        if do_exit:
            quit()

    headshot_path = input("Local path to headshot [Optional]:").strip()
    
    while not headshot_path=="" and not os.path.exists(headshot_path):
        print("File not found. Please try again.")
        headshot_path = input("Path to headshot [Optional]:")

    title = utils.input_options("Your title:", VALID_TITLES)
    website = input("""Personal website URL [Optional]:""")
    research_areas = input("Research areas, seperated by commas [Optional]:")
    is_visiting = utils.y_or_n("""Are you a visitor (e.g. an intern or visiting PhD Student)?""")

    out_path = build_person(name, headshot_path, title,
                            website, research_areas, 
                            is_visiting=is_visiting)
    print("New person created at {}".format(out_path))





