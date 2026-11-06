import random
from math import inf


def minimax(stones, maximizing, alpha, beta):
    if stones == 0:
        return (-1 if maximizing else 1), None

    best_score = -inf if maximizing else inf
    best_move = None

    for move in range(1, min(2, stones) + 1):
        score, _ = minimax(stones - move, not maximizing, alpha, beta)

        better = score > best_score if maximizing else score < best_score

        if better:
            best_score, best_move = score, move

        alpha = max(alpha, best_score) if maximizing else alpha
        beta = min(beta, best_score) if not maximizing else beta

        if alpha >= beta:  # PRUNE
            break

    return best_score, best_move


def main():
    stones = random.randint(5, 20)
    print(f"Starting number of stones: {stones}")

    ai_turn = True

    while stones > 0:
        if ai_turn:
            _, move = minimax(stones, True, -inf, inf)
            print(f"Computer removes {move} stones.")
        else:
            while True:
                try:
                    move = int(input("Remove 1 or 2 stones: "))
                    if 1 <= move <= min(2, stones):
                        break
                except ValueError:
                    pass

                print("Invalid move!")

        stones -= move
        print(f"Remaining stones: {stones}")

        if stones == 0:
            print("Computer wins!" if ai_turn else "You win!")
            break

        ai_turn = not ai_turn


if __name__ == "__main__":
    main()
