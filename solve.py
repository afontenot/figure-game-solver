import sys


def find_remove_tiles(game, start_pos):
    color = game[start_pos[0]][start_pos[1]]
    queue = [start_pos]
    to_remove = {start_pos}
    while queue:
        col, row = queue.pop()
        to_search = [(col + 1, row), (col - 1, row), (col, row + 1), (col, row - 1)]
        for t_col, t_row in to_search:
            if t_col < 0 or t_row < 0:
                continue
            try:
                new_tile = game[t_col][t_row]
                if new_tile == color:
                    location = (t_col, t_row)
                    if not location in to_remove:
                        queue.append(location)
                        to_remove.add(location)
            except IndexError:
                continue
    return to_remove


def solve(game, limit, depth=1):
    best_path = None

    for choice in range(5):
        if not game[choice]:
            continue
        chosen_color = game[choice][0]

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
            return ([choice], depth)

        if depth < limit and len(unique_tiles) <= limit - depth:
            solution, sol_depth = solve(new_game, limit, depth + 1)
            if solution and sol_depth <= limit:
                limit = sol_depth
                best_path = [choice] + solution

    return (best_path, limit)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} game.fg")
        sys.exit(1)
    with open(sys.argv[1]) as f:
        _, title = f.readline().strip().split(maxsplit=1)
        _, limit = f.readline().strip().split()
        limit = int(limit)
        data = f.read().strip().split("\n")
        game = [[] for _ in range(5)]
        for col_i in range(5):
            for row_i in range(5):
                game[col_i].append(data[4 - row_i][col_i])

    print(title)

    s_path, s_limit = solve(game, limit)

    if not s_path:
        print("Game has no solution!")
    else:
        print(f"Game solved in {s_limit} moves.")
        print("Solution:", " ".join([str(x + 1) for x in s_path]))
