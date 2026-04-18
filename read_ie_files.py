from hashlib import new
from pathlib import Path
from stat_editor import *

unitbase_path = "./ie_2_og/unitbase.dat"
unitbase_chunk_size = 0x60

unitstr_path = "./ie_2_og/unitbase.STR"
unitstr_chunk_size = 0x80

unitstat_path = "./ie_2_og/unitstat.dat"
unitstat_chunk_size = 0x50

elements = {0x01: "AIR", 0x02: "WOOD", 0x03: "FIRE", 0x04: "EARTH"}

positions = {0x20: "GK", 0x40: "DF", 0x60: "MF", 0x80: "FW", 0x00: "N/A"}


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
        chunk = data_base[i : i + unitbase_chunk_size]
        if chunk[0x00] < 0x96:  # Remove last players that don't exist
            name = [x for x in chunk[0x00:0x20] if x != 0x81]
            username = [x for x in chunk[0x20:0x30] if x != 0x81]
            player = {
                "unitbase": chunk,
                "name": bytes(name).decode(encoding="latin1").rstrip("\x00"),
                "username": (
                    bytes(username).decode(encoding="latin1").rstrip("\x00")
                    if chunk[0x20] != 0x82
                    else ""
                ),
                "gender": "M" if chunk[0x52] == 0x01 else "F",
                "age": chunk[0x53],
                "body_type": chunk[0x54],
                "position": positions.get(chunk[0x55] & 0xF0),
                "element": elements.get(chunk[0x5A]),
            }
            player_base.append(player)
    return player_base


def add_players_stat(database):
    file_path = Path(unitstat_path)
    data_stat = file_path.read_bytes()
    for i in range(0, len(database)):
        player_stat_idx = unitstat_chunk_size * (i + 1)
        database[i]["unitstat"] = data_stat[
            player_stat_idx : player_stat_idx + unitstat_chunk_size
        ]
    return database


def add_players_profile(database):
    file_path = Path(unitstr_path)
    data_str = file_path.read_bytes()
    for i in range(0, len(database)):
        player_profile_idx = unitstr_chunk_size * (i + 1)
        database[i]["profile"] = (
            data_str[player_profile_idx : player_profile_idx + unitstr_chunk_size]
            .decode("latin1")
            .strip("\x00")
        )
    return database


def find_player_by_username(database, username):
    for player in database:
        if player["username"].upper() == username.upper():
            return player
    return None


def find_player_index_by_username(database, username):
    for i in range(0, len(database)):
        if database[i]["username"].upper() == username.upper():
            return i
    return None


def print_database(database):
    print(
        f'{"NAME":<32} | {"USERNAME":<16} | {"GENDER":<8} | {"AGE":<4} | {"BODY TYPE":<10} | {"POSITION":<10} | {"ELEMENT":<10}'
    )
    print("-" * 120)
    for player in database:
        print(
            f'{player["name"]:<32} | {player["username"]:<16} | {player["gender"]:<8} | {player["age"]:<4} | {player["body_type"]:<10} | {player["position"]:<10} | {player["element"]:<10}'
        )


def replace_player_unitbase(
    database,
    player_index,
    new_name=None,
    new_username=None,
    new_gender=None,
    new_age=None,
    new_body_type=None,
    new_position=None,
    new_element=None,
):
    player = database[player_index]
    unitbase = bytearray(player["unitbase"])
    if new_name is not None:
        name_bytes = new_name.encode(encoding="latin1")
        name_bytes = name_bytes[:0x20] + bytes([0x00] * (0x20 - len(name_bytes)))
        unitbase[0x00:0x20] = name_bytes[0x00:0x20]
    if new_username is not None:
        username_bytes = new_username.encode(encoding="latin1")
        username_bytes = username_bytes[:0x10] + bytes(
            [0x00] * (0x10 - len(username_bytes))
        )
        unitbase[0x20:0x30] = username_bytes[0x00:0x10]
    if new_gender is not None:
        unitbase[0x52] = 0x01 if new_gender == "M" else 0x00
    if new_age is not None and new_age in range(0, 99):
        unitbase[0x53] = new_age
    if new_body_type is not None and new_body_type in [0x00, 0x01, 0x02]:
        unitbase[0x54] = new_body_type
    if new_position is not None and new_position in positions.values():
        unitbase[0x55] = list(positions.keys())[
            list(positions.values()).index(new_position)
        ]
    if new_element is not None and new_element in elements.values():
        unitbase[0x5A] = list(elements.keys())[
            list(elements.values()).index(new_element)
        ]
    database[player_index]["unitbase"] = bytes(unitbase)
    update_player_data(database, player_index)


def change_player_stat(
    database,
    player_index,
    fp=None,
    tp=None,
    kick=None,
    body=None,
    guard=None,
    control=None,
    speed=None,
    guts=None,
    stamina=None,
    move_1=None,
    move_2=None,
    move_3=None,
    move_4=None,
):
    player_stats = bytearray(database[player_index]["unitstat"])

    if fp is not None:
        (min, max, freedom) = fp
        player_stats = change_stat(player_stats, 0x00, min, max, freedom)
    if tp is not None:
        (min, max, freedom) = tp
        player_stats = change_stat(player_stats, 0x08, min, max, freedom)
    if kick is not None:
        (min, max, freedom) = kick
        player_stats = change_stat(player_stats, 0x10, min, max, freedom)
    if body is not None:
        (min, max, freedom) = body
        player_stats = change_stat(player_stats, 0x14, min, max, freedom)
    if guard is not None:
        (min, max, freedom) = guard
        player_stats = change_stat(player_stats, 0x18, min, max, freedom)
    if control is not None:
        (min, max, freedom) = control
        player_stats = change_stat(player_stats, 0x1C, min, max, freedom)
    if speed is not None:
        (min, max, freedom) = speed
        player_stats = change_stat(player_stats, 0x20, min, max, freedom)
    if guts is not None:
        (min, max, freedom) = guts
        player_stats = change_stat(player_stats, 0x24, min, max, freedom)
    if stamina is not None:
        (min, max, freedom) = stamina
        player_stats = change_stat(player_stats, 0x28, min, max, freedom)

    if move_1 is not None:
        (move_name, level) = move_1
        player_stats = change_move(player_stats, 0x2C, move_name, level)
    if move_2 is not None:
        (move_name, level) = move_2
        player_stats = change_move(player_stats, 0x2C + 0x04, move_name, level)
    if move_3 is not None:
        (move_name, level) = move_3
        player_stats = change_move(player_stats, 0x2C + 0x08, move_name, level)
    if move_4 is not None:
        (move_name, level) = move_4
        player_stats = change_move(player_stats, 0x2C + 0x0C, move_name, level)

    print_stats(player_stats)


def update_player_data(database, player_index):
    name = [x for x in database[player_index]["unitbase"][0x00:0x20] if x != 0x81]
    username = [x for x in database[player_index]["unitbase"][0x20:0x30] if x != 0x81]
    database[player_index]["name"] = (
        bytes(name).decode(encoding="latin1").rstrip("\x00")
    )
    database[player_index]["username"] = (
        bytes(username).decode(encoding="latin1").rstrip("\x00")
        if database[player_index]["unitbase"][0x20] != 0x82
        else ""
    )
    database[player_index]["gender"] = (
        "M" if database[player_index]["unitbase"][0x52] == 0x01 else "F"
    )
    database[player_index]["age"] = database[player_index]["unitbase"][0x53]
    database[player_index]["body_type"] = database[player_index]["unitbase"][0x54]
    database[player_index]["position"] = positions.get(
        database[player_index]["unitbase"][0x55] & 0xF0
    )
    database[player_index]["element"] = elements.get(
        database[player_index]["unitbase"][0x5A]
    )


def main():
    database = get_player_base()
    database = add_players_profile(database)
    database = add_players_stat(database)
    print_database(database)


if __name__ == "__main__":
    main()
