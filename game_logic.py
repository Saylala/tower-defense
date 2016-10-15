def in_field(field, point):
    return 0 <= point.row < len(field) and 0 <= point.col < len(field[0])