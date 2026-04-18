
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

# Nano
# nano_caz_stats = [
#     0x46, 0x00, 0xB6, 0x00, 0x04, 0x00, 0x00, 0x00, 0x3D, 0x00, 0xA4, 0x00, 0x04, 0x00, 0x00, 0x00, 0x0E, 0x3E, 0x04, 0x00, 0x10, 0x44, 0x04, 0x00, 0x0D, 0x40, 0x04, 0x00, 0x0E, 0x3E, 0x04, 0x00, 0x0F, 0x43, 0x04, 0x00, 0x0D, 0x3C, 0x04, 0x00, 0x10, 0x40, 0x04, 0x00, 0x3B, 0x00, 0x01, 0x00, 0x85, 0x00, 0x1A, 0x00, 0x45, 0x01, 0x27, 0x00, 0x6C, 0x01, 0x36, 0x00, 0xD2, 0x01, 0x1C, 0x00, 0x15, 0x00, 0x11, 0x00, 0x1D, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
#     ]
# print_stats(nano_caz_stats)

# nano_caz_stats = change_stat(nano_caz_stats, 0x00, 71, 164, 5) # FP
# nano_caz_stats = change_stat(nano_caz_stats, 0x08, 77, 182, 5) # TP
# nano_caz_stats = change_stat(nano_caz_stats, 0x10, 14, 79, 5) # kick
# nano_caz_stats = change_stat(nano_caz_stats, 0x14, 16, 71, 5) # body
# nano_caz_stats = change_stat(nano_caz_stats, 0x18, 13, 69, 5) # guard
# nano_caz_stats = change_stat(nano_caz_stats, 0x1C, 14, 72, 5) # control
# nano_caz_stats = change_stat(nano_caz_stats, 0x20, 15, 77, 5) # speed
# nano_caz_stats = change_stat(nano_caz_stats, 0x24, 13, 68, 5) # guts
# nano_caz_stats = change_stat(nano_caz_stats, 0x28, 16, 67, 5) # stamina

# nano_caz_stats = change_move(nano_caz_stats, 0x2C, 'Illusion Ball', 1)
# nano_caz_stats = change_move(nano_caz_stats, 0x2C + 0x04, 'Phantom Shot', 15)
# nano_caz_stats = change_move(nano_caz_stats, 0x2C + 0x08, 'Quick Draw', 30)
# nano_caz_stats = change_move(nano_caz_stats, 0x2C + 0x0C, 'Big Moves!', 45)

# print_stats(nano_caz_stats)

# print_bytes(nano_caz_stats)

# # Caz

# caz_stats = [
#     0x2A, 0x00, 0xA9, 0x00, 0x04, 0x00, 0x00, 0x00, 0x3F, 0x00, 0xB0, 0x00, 0x01, 0x00, 0x00, 0x00, 0x0B, 0x33, 0x01, 0x00, 0x09, 0x37, 0x02, 0x00, 0x07, 0x2C, 0x05, 0x00, 0x0E, 0x41, 0x02, 0x00, 0x0B, 0x3C, 0x01, 0x00, 0x08, 0x3E, 0x01, 0x00, 0x09, 0x3D, 0x04, 0x00, 0x46, 0x01, 0x13, 0x00, 0x99, 0x00, 0x1B, 0x00, 0x80, 0x00, 0x22, 0x00, 0x42, 0x01, 0x34, 0x00, 0xA1, 0x01, 0x14, 0x00, 0x10, 0x00, 0x16, 0x00, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
# ]
