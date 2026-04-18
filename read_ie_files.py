from pathlib import Path 
from stat_editor import *

unitbase_path = "./ie_2_og/unitbase.dat"
unitbase_chunk_size = 0x60

unitstr_path = "./ie_2_og/unitbase.STR"
unitstr_chunk_size = 0x80

unitstat_path = "./ie_2_og/unitstat.dat"
unitstat_chunk_size = 0x50

elements = {
    0x01: "AIR",
    0x02: "WOOD",
    0x03: "FIRE",
    0x04: "EARTH"
}

positions = {
    0x20: "GK",
    0x40: "DF",
    0x60: "MF",
    0x80: "FW",
    0x00: "N/A"
}

# UNITBASE DATA
# Each players occupies 6 lines with 16 bytes = 90 bytes or 0x5A
# 0x00 up to 0x5F is garbage
# NAME: 0x00 until 0x1F
# USERNAME: 0x20 until 0x2F
# GENDER: 0x52
# AGE: 0x53
# BODY TYPE: 0x54
# POSITION: 0x55
# ELEMENT: 0x5A
def get_player_base():
    file_path = Path(unitbase_path)
    data_base = file_path.read_bytes()
    player_base = []
    for i in range(unitbase_chunk_size, len(data_base), unitbase_chunk_size):
        chunk = data_base[i:i + unitbase_chunk_size]
        if(chunk[0x00] < 0x96): # Remove last players that don't exist
            name = [x for x in chunk[0x00:0x20] if x != 0x81]
            username = [x for x in chunk[0x20:0x30] if x != 0x81]
            player = {
                "unitbase": chunk,
                "name": bytes(name).decode(encoding='latin1').rstrip('\x00'),
                "username": bytes(username).decode(encoding='latin1').rstrip('\x00') if chunk[0x20] != 0x82 else '',
                "gender": "M" if chunk[0x52] == 0x01 else "F",
                "age": chunk[0x53],
                "body_type": chunk[0x54],
                "position": positions.get(chunk[0x55] & 0xF0),
                "element": elements.get(chunk[0x5A])
            }
            player_base.append(player)
    return player_base

def add_players_stat(database):
    file_path = Path(unitstat_path)
    data_stat = file_path.read_bytes()
    for i in range(0, len(database)):
        player_stat_idx = unitstat_chunk_size * (i + 1)
        database[i]['unitstat'] = data_stat[player_stat_idx:player_stat_idx + unitstat_chunk_size]
    return database

def add_players_profile(database):
    file_path = Path(unitstr_path)
    data_str = file_path.read_bytes()
    for i in range(0, len(database)):
        player_profile_idx = unitstr_chunk_size * (i + 1)
        database[i]['profile'] = data_str[player_profile_idx:player_profile_idx + unitstr_chunk_size].decode('latin1').strip('\x00')
    return database

def find_player_by_username(database, username):
    for player in database:
        if player['username'].upper() == username.upper():
            return player
    return None

def find_player_index_by_username(database, username):
    for i in range(0, len(database)):
        if database[i]['username'].upper() == username.upper():
            return i
    return None

def print_database(database):
    print(f'{"NAME":<32} | {"USERNAME":<16} | {"GENDER":<8} | {"AGE":<4} | {"BODY TYPE":<10} | {"POSITION":<10} | {"ELEMENT":<10}')
    print('-' * 120)
    for player in database:
        print(f'{player["name"]:<32} | {player["username"]:<16} | {player["gender"]:<8} | {player["age"]:<4} | {player["body_type"]:<10} | {player["position"]:<10} | {player["element"]:<10}')

def main():
    database = get_player_base()
    database = add_players_profile(database)
    database = add_players_stat(database)
    print_database(database)

if __name__ == '__main__':
    main()