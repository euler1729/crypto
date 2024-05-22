import itertools

data = [
    [(8, 'E'), (8, 'y')],
    [(10, 'T'), (10, 'n')],
    [(9, 'I'), (9, 'c')],
    [(10, 'X'), (10, 'r')],
    [(9, 'Y'), (9, 's')],
    [(8, 'V'), (8, 'p')],
    [(11, 'Z'), (11, 't')]
]

# Generate strings
result_strings = []
for combination in itertools.product(*data):
    current_string = ''.join(inner_tuple[1] for inner_tuple in combination)
    result_strings.append(current_string)

# Print the first 128 strings of length 7
for i in range (len(result_strings)):
    print(result_strings[i])
