def get_position_array():
    position_array = [None] * 100
    start_z = 40
    for index, position in enumerate(position_array):
        position_array[index] = (index*4, index*4, start_z - index/2)
    return position_array