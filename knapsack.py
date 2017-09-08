import argparse
import sys


def knapsack(items, maxweight):
    """
    Solve the knapsack problem by finding the most valuable
    subsequence of `items` subject that weighs no more than `maxweight`.

    `items` is a sequence of pairs `(weight, value)`, where `weight` and
    `value` are non-negative integers.

    `maxweight` is a non-negative integer.

    Return a pair whose first element is the sum of values in the most
    valuable subsequence, and whose second element is the subsequence.

    >>> items = [(2, 3), (3, 4), (4, 5), (5, 5)]
    >>> knapsack(items, 7)
    (9, [(3, 4), (4, 5)])
    """
    n = len(items)
    # Prepopulate table with 0s
    m = [[0 for w in range(maxweight + 1)] for i in range(n + 1)]

    # Build table bottom up
    for i in range(n + 1):
        for w in range(maxweight + 1):
            weight, value = items[i - 1]
            if i == 0 or w == 0:
                m[i][w] = 0
            elif weight <= w:
                m[i][w] = max(value + m[i - 1][w - weight], m[i - 1][w])
            else:
                m[i][w] = m[i - 1][w]

    # Get optimal items
    w = maxweight
    selected_items = []
    for i in range(n, 0, -1):
        if m[i][w] != m[i - 1][w]:
            selected_items.append(items[i - 1])
            w -= items[i - 1][0]
    selected_items.reverse()

    return m[n][maxweight], selected_items


def parse_input(input_file):
    """
    Parse `input_file` and return pair (`items`, `maxweight`)
    in the format that is needed for knapsack function.

    First line of input file is max weight.
    Next line provides number N, the number of items that are available.
    The following line contains N integers that represent the weight for a
    given item and the last line of input represents the value.

    Example input file
    7
    4
    2 3 4 5
    3 4 5 5
    """
    lines = [l.rstrip() for l in input_file]
    maxweight = int(lines[0])
    items_len = int(lines[1])
    weights = [int(w) for w in lines[2].split()]
    values = [int(v) for v in lines[3].split()]

    if (maxweight < 0 or
            any(w < 0 for w in weights) or any(v < 0 for v in values)):
        raise ValueError('All numbers must be non-negative integers.')
    elif len(weights) != items_len or len(values) != items_len:
        raise ValueError('Value and weight lists must match.')

    items = list(zip(weights, values))
    return items, maxweight


def write_result(value, items):
    """
    Print result of knapsack problem to console.

    First line should output the total value of items in the knapsack.
    Each next line outputs a item weight with the corresponding value.

    Example output
    9
    3 4
    4 5
    """
    print(value)
    for item in items:
        print(item[0], item[1])


def main():
    # Parse arguments
    desc = ('Solve the knapsack problem by finding the most valuable '
            'subsequence of items.')
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('file', type=argparse.FileType('r'), nargs='?',
                        help='input file')
    args = parser.parse_args()
    input_file = args.file or sys.stdin
    # Parse input file
    try:
        items, maxweight = parse_input(input_file)
    except (IndexError, ValueError) as e:
        print('Incorrect input file:', e, file=sys.stderr, sep='\n')
        sys.exit(1)
    # Solve knapsack
    sum_value, selected_items = knapsack(items, maxweight)
    # Write result
    write_result(sum_value, selected_items)


if __name__ == '__main__':
    main()
