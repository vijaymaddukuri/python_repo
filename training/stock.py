def profit(stock_prices):
    # Start minimum price marker at first price
    min_stock_price = stock_prices[0]

    # Start off with a profit of zero
    max_profit = 0

    for price in stock_prices:
        # Check to set the lowest stock price so far
        min_stock_price = min(min_stock_price, price)

        # Check the current price against our minimum for a profit
        # comparison against the max_profit
        comparison_profit = price - min_stock_price

        # Compare against our max_profit so far
        max_profit = max(max_profit, comparison_profit)

    return max_profit
print(profit([30,22,21,5]))