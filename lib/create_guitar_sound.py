import itertools


# 获取所有的单音组合
def generate_single_notes():
    guitar_notes = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    single_notes = []

    for note in guitar_notes:
        single_notes.append([note, [(i, j + 1) for i, j in enumerate(range(6), 1)]])

    return single_notes


# 获取所有的多音组合
def generate_multiple_notes():
    guitar_notes = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    multiple_notes = []

    for num_notes in range(2, 7):
        combinations = list(itertools.combinations(guitar_notes, num_notes))
        for combination in combinations:
            multiple_notes.append([list(combination), [(i, j + 1) for i, j in enumerate(range(num_notes), 1)]])

    return multiple_notes


# 生成所有的和弦组合
def generate_chords():
    guitar_notes = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    chords = []

    # 编写生成和弦的代码，将和弦信息添加到 chords 列表中

    return chords


# 初始化生成所有的列表
def initialize_lists():
    single_notes = generate_single_notes()
    multiple_notes = generate_multiple_notes()
    chords = generate_chords()

    all_combinations = []

    # 生成包含序号、单音、位置、和弦信息的所有组合
    for i, item in enumerate(single_notes + multiple_notes + chords, 1):
        if len(item[0]) == 1:
            all_combinations.append([i, len(item[0]), item[1], 'NAN'])
        else:
            all_combinations.append([i, len(item[0]), item[1], ''.join(item[0])])

    return all_combinations


# 从列表中删除指定序号的组合
def remove_combination(combinations, index):
    for combination in combinations:
        if combination[0] == index:
            combinations.remove(combination)
            break

    return combinations


# 示例使用
all_combinations = initialize_lists()
print(all_combinations)

# 删除序号为 3 的组合
all_combinations = remove_combination(all_combinations, 3)
print(all_combinations)