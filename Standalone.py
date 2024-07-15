import requests
import re
import time
import random

ID = 778  # Default Vintage Group ID
TYPE = "GROUP"  # Default is GROUP
MAX_RETRIES = 5  # Max retries for connection
REFRESH_INTERVAL = 12  # Default refresh interval (seconds)

def get_temple_data():
    url = f"https://templeosrs.com/groups/edit_group.php?id={ID}"
    for _ in range(MAX_RETRIES):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise HTTPError for bad responses
            break  # Successful
        except requests.RequestException as e:
            print(f"Error during request: {e}")
            time.sleep(100)  # Wait for 100 seconds before retrying
    
    else:
        print("Failed to retrieve data after multiple attempts. GG")
        return []

    match_names = re.search(r'var names = \[(.+)\]', response.text)
    match_leaders = re.search(r'var leaders = \[(.+)\]', response.text)

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

if __name__ == "__main__":
    print(f"Default mode selected, updating all Vintage members every {REFRESH_INTERVAL} seconds.")

    while True:
        temple_data = get_temple_data()
        for player_name in temple_data:
            update_player(player_name)

        print("--ALL PLAYERS HAVE BEEN UPDATED, TAKING A 30 SEC BREAK BRB")
        time.sleep(30)  # 30 sec break
