import numpy as np
import scipy.stats as stats

def probability_of_profit(current_price, strike_price, premium_received, iv, days_to_expiration):
    breakeven_point = strike_price - premium_received
    expected_move = current_price * iv * np.sqrt(days_to_expiration / 365)
    
    # Calculate z-score
    z_score = (np.log(breakeven_point / current_price)) / (iv * np.sqrt(days_to_expiration / 365))
    
    # Calculate POP
    pop = stats.norm.cdf(z_score)
    
    return pop

# Example usage
current_price = 50  # Current stock price
strike_price = 45   # Strike price of the put option
premium_received = 2  # Premium received for writing the put option
iv = 0.30  # Implied volatility (30%)
days_to_expiration = 30  # Days to expiration

pop = probability_of_profit(current_price, strike_price, premium_received, iv, days_to_expiration)
print(f"The probability of profit is: {pop:.2%}")
