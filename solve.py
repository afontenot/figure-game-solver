import sys


def find_remove_tiles(game, start_pos):
    """Finds tiles that will be removed if given tile is removed.

    Uses a simple flood filling approach to find tiles connected
    to a given starting tile. New tiles to search are added to a
    stack rather than using recursion.

    Returns a list of positions for tiles that will be removed.
    """
    color = game[start_pos[0]][start_pos[1]]
    stack = [start_pos]

    # we aren't flood filling, so the color of the tiles doesn't
    # change; instead, we keep track of tiles to remove in a set.
    to_remove = {start_pos}
    while stack:
        col, row = stack.pop()
        to_search = [(col + 1, row), (col - 1, row), (col, row + 1), (col, row - 1)]
        for location in to_search:
            if location in to_remove:
                continue
            t_col, t_row = location
            if t_col < 0 or t_row < 0:
                continue
            try:
                new_tile = game[t_col][t_row]
                if new_tile == color:
                    stack.append(location)
                    to_remove.add(location)
            except IndexError:
                continue
    return to_remove


def solve(game, limit):
    """Solves figure.game boards recursively.

    Input format is a list of lists in [column][row] order,
    with rows sorted bottom to top.

    Returns a list of steps that optimally solves the game,
    or None if the game cannot be solved in the allowed
    number of moves.
    """

    best_path = None
    prev_color = None
    limit -= 1

    # consider each of the five columns as possible choices
    for choice in range(5):
        if not game[choice]:
            prev_color = None
            continue
        chosen_color = game[choice][0]

        # track the color of the previous column, skip if identical
        if chosen_color == prev_color:
            continue
        prev_color = chosen_color

        # remove tiles
        new_game = [[] for _ in range(5)]
        removed_tiles = find_remove_tiles(game, (choice, 0))
        unique_tiles = set()
        for i, column in enumerate(game):
            for j, tile in enumerate(column):
                if not (i, j) in removed_tiles:
                    new_game[i].append(tile)
                    unique_tiles.add(tile)

        # process new game
        if len(unique_tiles) == 0:
            # if game is solved in one move, this is best case scenario
            return [choice]

        # if we've reached the depth limit, no more recursion
        # significant optimization: if there are more colors remaining
        # than there are moves, we've reached a dead end. Approx 10x speedup.
        if len(unique_tiles) <= limit:
            solution = solve(new_game, limit)
            if solution:
                # dynamically reduce the limit using best known solution
                limit = len(solution) - 1
                best_path = [choice] + solution

    return best_path


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} game.fg")
        sys.exit(1)

    # see sample file for format
    with open(sys.argv[1]) as f:
        _, title = f.readline().strip().split(maxsplit=1)
        _, limit = f.readline().strip().split()
        limit = int(limit)
        data = f.read().strip().split("\n")

        # convert top-down row-col format to bottom-up col-row
        game = [[] for _ in range(5)]
        for col_i in range(5):
            for row_i in range(5):
                game[col_i].append(data[4 - row_i][col_i])

    print(title)

    solution = solve(game, limit)

    if not solution:
        print("Game has no solution!")
    else:
        print(f"Game solved in {len(solution)} moves.")
        print("Solution:", " ".join([str(x + 1) for x in solution]))
