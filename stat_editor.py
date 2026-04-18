
from moves import moves

def move_index_by_id(id):
    for i, (move_id, move_name) in enumerate(moves):
        if move_id == id:
            return i
    return -1
    
def move_index_by_name(name):
    for i, (move_id, move_name) in enumerate(moves):
        if name.lower() == move_name.lower():
            return i
    return -1
    
def stat(stats, start):
    if start < 0x10:
        min = int(f'0x{stats[start + 1]:02X}{stats[start]:02X}', 16)
        max = int(f'0x{stats[start + 3]:02X}{stats[start + 2]:02X}', 16)
        freedom = int(f'0x{stats[start + 5]:02X}{stats[start + 4]:02X}', 16)
    else:
        min = int(f'0x{stats[start]:02X}', 16)
        max = int(f'0x{stats[start + 1]:02X}', 16)
        freedom = int(f'0x{stats[start + 3]:02X}{stats[start + 2]:02X}', 16)
    return (min, max, freedom)
    
def move(stats, start):
    move_id = int(f'0x{stats[start + 1]:02X}{stats[start]:02X}', 16)
    move_id_dup, move_name = moves[move_index_by_id(move_id)]
    learn_lvl = int(f'0x{stats[start + 3]:02X}{stats[start + 2]:02X}', 16)
    return (move_name, learn_lvl)

def print_stats(stats):
    for i in range(9):
        if (i < 2):
            print(stat(stats, i * 0x08))
        else:
            print(stat(stats, (i - 2) * 0x04 + 0x10))
    
    for j in range(4):
        print(move(stats, 0x2C + 0x04 * j))

def change_stat(stats, start, min, max, freedom):
    hex_min = f'{min:04X}'
    hex_max = f'{max:04X}'
    hex_freedom = f'{freedom:04X}'
    if(start < 0x10):
        stats[start] = int(f'0x{hex_min[2:4]}', 16)
        stats[start + 1] =  int(f'0x{hex_min[0:2]}', 16)
        stats[start + 2] =  int(f'0x{hex_max[2:4]}', 16)
        stats[start + 3] =  int(f'0x{hex_max[0:2]}', 16)
        stats[start + 4] =  int(f'0x{hex_freedom[2:4]}', 16)
        stats[start + 5] =  int(f'0x{hex_freedom[0:2]}', 16)
    else:
        stats[start] = int(f'0x{hex_min[2:4]}', 16)
        stats[start + 1] =  int(f'0x{hex_max[2:4]}', 16)
        stats[start + 2] =  int(f'0x{hex_freedom[2:4]}', 16)
        stats[start + 3] =  int(f'0x{hex_freedom[0:2]}', 16)
    return stats

def change_move(stats, start, move_name, level):
    mv_id, mv_name = moves[move_index_by_name(move_name)]
    move_id = f'{mv_id:04X}'
    move_lvl = f'{level:04X}'
    stats[start] = int(f'0x{move_id[2:4]}', 16)
    stats[start + 1] = int(f'0x{move_id[0:2]}', 16)
    stats[start + 2] = int(f'0x{move_lvl[2:4]}', 16)
    stats[start + 3] = int(f'0x{move_lvl[0:2]}', 16)
    return stats

def print_bytes(stats):
    for bt in stats:
        print(f'{bt:02X}', end=' ')
    print('')
