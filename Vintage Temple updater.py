import requests
import re
import time
import random

ID = 778 #Default Vintage Group ID
TYPE = "GROUP" # Default is GROUP, can change to COMPETITIVE
MAX_RETRIES = 5 #Max retries for connection
REFRESH_INTERVAL = 15 # Default refresh interval (seconds)

# Vintage URL
# https://templeosrs.com/groups/overview.php?id=778

def get_temple_data():
    if TYPE == "GROUP":
        url = f"https://templeosrs.com/groups/edit_group.php?id={ID}"
    elif TYPE == "COMPETITION":
        url = f"https://templeosrs.com/competitions/edit.php?id={ID}"
    for _ in range(MAX_RETRIES):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise HTTPError for bad responses
            break  # succesful
        except requests.RequestException as e:
            print(f"Error during request: {e}")
            time.sleep(100)  # Wait for 100 seconds before retrying
    
    else:
        print("Failed to retrieve data after multiple attempts. GG")
        return []

    #the page should always have names
    match_names = re.search(r'var names = \[(.+)\]', response.text)
    
    if TYPE == "GROUP":
        match_leaders = re.search(r'var leaders = \[(.+)\]', response.text)
    else:
        match_leaders = None

    if match_names or match_leaders:
        names = match_names.group(1)
        player_names = re.findall(r'"([^,]+?)"', names)
        
        if match_leaders is None:
            random.shuffle(player_names)
            return player_names
        leaders = match_leaders.group(1)
        leader_names = re.findall(r'"([^,]+?)"', leaders)

        combined_names = player_names + leader_names
        random.shuffle(combined_names)

        return combined_names

    return []

def update_player(player_name):
    url = f"https://templeosrs.com/php/add_datapoint.php?player={player_name}"

    for _ in range(MAX_RETRIES):
        try:
            response = requests.post(url)
            response.raise_for_status()  # Raise HTTPError for bad responses
            break  # Successful request, exit the loop
        except requests.RequestException as e:
            print(f"Error during request: {e}")
            time.sleep(10000)  # Slow retry 
    else:
        print(f"Failed to update player '{player_name}' after multiple attempts.")
        return
    
    if response.status_code == 200:
        print(f"Player '{player_name}' has been successfully updated. Yippee!!")
    else:
        print(f"Failed to update player '{player_name}'. Status code: {response.status_code} :(")

    time.sleep(REFRESH_INTERVAL)

def ask_for_mode():
    while True:
        mode_input = input("Enter mode (D for Default / M for Manual): ").strip().lower()
        if "m" in mode_input:
            return "M"
        elif "d" in mode_input:
            return "D"
        else:
            print("Invalid mode, please choose D for Default or M for Manual.")

def ask_for_type():
    while True:
        type_input = input("Enter type (G for Group / C for Competition): ").strip().lower()
        if "c" in type_input:
            return "COMPETITION"
        elif "g" in type_input:
            return "GROUP"
        else:
            print("Invalid type, please choose G for Group / C for Competition.")

if __name__ == "__main__":
    # Ask for mode selection
    
    mode = ask_for_mode()  # Get the mode from the user

    if mode == "M":  # If Manual mode is selected
        TYPE = ask_for_type()  # Get the type from the user
        ID = int(input(f"Enter the ID of the {TYPE.lower()}: "))
        REFRESH_INTERVAL = int(input("Enter the refresh interval (in seconds): "))
    elif mode == "D":
        print(f"Default mode selected, updating all Vintage members every {REFRESH_INTERVAL} seconds.")
    else:
        print(f"Something went wrong, mode is set to {MODE}, how did you do that?")
        
    while True:
        temple_data = get_temple_data()
        for player_name in temple_data:
            update_player(player_name)

        print("--ALL PLAYERS HAVE BEEN UPDATED, TAKING A 30 SEC BREAK BRB")
        time.sleep(30)  # 30 sec breaky breaky
