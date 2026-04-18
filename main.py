from src.ie_files import *


def change_player(
    database,
    player_username,
    new_name=None,
    new_username=None,
    new_gender=None,
    new_age=None,
    new_body_type=None,
    new_position=None,
    new_element=None,
    new_profile=None,
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
    pl_index = find_player_index_by_username(database, player_username)
    change_player_unitbase(
        database,
        pl_index,
        new_name=new_name,
        new_username=new_username,
        new_age=new_age,
        new_position=new_position,
        new_element=new_element,
    )
    if new_profile is not None:
        change_profile(
            database,
            pl_index,
            new_profile=new_profile,
        )
    change_player_stat(
        database,
        pl_index,
        fp=fp,
        tp=tp,
        kick=kick,
        body=body,
        guard=guard,
        control=control,
        speed=speed,
        guts=guts,
        stamina=stamina,
        move_1=move_1,
        move_2=move_2,
        move_3=move_3,
        move_4=move_4,
    )
    output_path = sys.argv[1] if len(sys.argv) > 1 else "./output"
    save_new(database, pl_index, output_path)


def main():
    database = export_database()
    # change_player(database, <player-to-change-nickname>, <params>,...)
    print("Saved!")


if __name__ == "__main__":
    main()
