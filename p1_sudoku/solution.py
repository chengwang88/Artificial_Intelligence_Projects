assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a + b for a in A for b in B]


rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

# for diagonal sudoku, add diagonal_units
diagonal_units = [[i+j for i,j in zip(rows, cols)], [i+j for i,j in zip(rows, cols[::-1])]]
unitlist = row_units + column_units + square_units + diagonal_units 

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    for unit in unitlist:
        # Find all instances of naked twins
        # collect box with length 2 for this unit
        boxn2 = [box for box in unit if len(values[box]) == 2]
        n2 = len(boxn2)
        # if less than 2, no naked twins, continue
        if n2 < 2:
            continue
        # get naked twins list 
        twinboxlist = []
        for i in range(n2-1):
            for j in range(i+1,n2):
                if values[boxn2[i]] == values[boxn2[j]]:
                    twinboxlist.append((boxn2[i], boxn2[j]))
        # eliminated the value in naked twins from their peers in this unit
        for twin in twinboxlist:
            box1, box2 = twin
            twinv = values[box1]
            for peer in unit:
                if peer not in [box1, box2]:
                    for v in twinv:
                        if v in values[peer]:
                            values = assign_value(values, peer, values[peer].replace(v, ''))
    return values


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    values = {}
    for box, v in zip(boxes, grid):
        if v == '.':
            values[box] = '123456789'
        else:
            values[box] = v            
    return values


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print


def eliminate(values):
    """
    Eliminate values from peers of each box with a single value
    Args:
        values: Sudoku in dict format
    Returns:
        values: Sudoku in dict format after eliminate values
    """
    solved = [box for box in values.keys() if len(values[box]) == 1]

    for box in solved:
        v = values[box]
        for peerbox in peers[box]:
            values = assign_value(values, peerbox, values[peerbox].replace(v, ''))
    return values


def only_choice(values):
    """
    Finalize all values that are the only choice for a unit
    Args:
        values: Sudoku in dict format
    Returns:
        values: Sudoku in dict format after filling in only choice
    """
    for unit in unitlist:
        for v in '123456789':
            vpos = [box for box in unit if v in values[box]]
            if len(vpos) == 1:
                values = assign_value(values, vpos[0], v)
    return values


def reduce_puzzle(values):
    """
    Solve the Sudoku by eliminate and only choice until no further improvement
    Args:
        values: original Sudoku in dict format
    Returns:
        values: Sudoku after solved by eliminate and only choice
        or False if there is a box with zero available values
    """
    # solved box
    solved = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        # number of boxes solved before
        solved_before = len(solved)
        # eliminate values
        values = eliminate(values)
        # fill value with only choice
        values = only_choice(values)
        # solved boxes after two procedures above
        solved = [box for box in values.keys() if len(values[box]) == 1]
        # number of boxes solved after two procedures above
        solved_after = len(solved)
        # if no new value is solved, stop 
        stalled = solved_before == solved_after
        # return false if there is a box with zero available values
        for box in values.keys():
            if len(values[box]) == 0:
                return False
    return values


def search(values):
    """
    Using depth-first search and propagation, try all possible values
    Args:
        values: Sudoku in dict format
    Returns:
        if sudoku is solved, return solved Sudoku in dict format
        or False if the try if wrong.
    """
    # solve the Sudoku with elimination and only choice method
    values = reduce_puzzle(values)
    
    if values is False:
        return False  # wrong previous try
    if all(len(values[box]) == 1 for box in boxes):
        return values # solved

    # find unfilled box with fewest choices
    _, smbox = min((len(values[box]), box) for box in boxes if len(values[box]) > 1)

    # use recurrence to search value each unfilled box
    for v in values[smbox]:
        # copy values to have a new try
        newvalues = values.copy() 
        # assign one possible value for the copy of sudoku
        newvalues[smbox] = v
        # search the solution given value v for smbox
        attempt = search(newvalues) 
        # if attempt is False, continue to next v
        # if attempt is values, return values
        if attempt:
            return attempt
            

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    return search(values)


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
