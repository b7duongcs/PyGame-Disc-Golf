def get_position_array():
    position_array = [None] * 100
    start_z = 80
    for index, position in enumerate(position_array):
        position_array[index] = (index/7, index/7, start_z - index)
    return position_array