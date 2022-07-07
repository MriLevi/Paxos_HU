def Parser(filename):
    with open(filename) as f:
        inputlines = [i.strip() for i in f.readlines()]

    start = inputlines[0].split(' ')
    n_p, n_a, tmax = int(start[0]), int(start[1]), int(start[2])

    split_lines = [i.split(' ') for i in inputlines[1:-1]]
    events = []
    input_list = []

    for line in split_lines:

        if not input_list:
            input_list = [int(line[0]), [], [], None, None]

        if int(line[0]) != input_list[0]:
            events.append(input_list)
            input_list = [int(line[0]), [], [], None, None]

        input_string = ''
        if 'PROPOSER' in line:
            input_string += 'P'
        else:
            input_string += 'A'
        if 'FAIL' in line:
            input_list[1].append(input_string + line[-1])
        elif 'RECOVER' in line:
            input_list[2].append(input_string + line[-1])
        elif 'PROPOSE' in line:
            input_list[3] = f'P{line[-2]}'
            input_list[4] = int(line[-1])
    events.append(input_list)
    return n_p, n_a, tmax, events