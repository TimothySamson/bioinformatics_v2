import numpy as np

# TODO: as the array grows, remove the tail end since we only go back so far to calculate the next value
def DPChange(money, coins):
    coins = np.array(coins)
    min_coins = np.array([0])
    for i in range(1, money+1):
        indices = i - coins
        indices = indices[indices >= 0]
        min_amount = min(min_coins[indices]) + 1
        min_coins = np.append(min_coins, min_amount)

    return min_coins


