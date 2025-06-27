import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 

def calculate_normmalized_implied_probabilities(actual_odds):
    """
    Calculate implied probabilities from odds.
    
    Args:
        odds (pd.DataFrame): DataFrame containing 'Home Odds' and 'Away Odds'.
        
    Returns:
        pd.DataFrame: DataFrame with implied probabilities for home and away teams.
    """
    actual_probs = 1 / actual_odds
    total_prob = actual_probs.sum(axis=1)
    fair_probs = actual_probs.div(total_prob, axis=0)
    fair_probs.columns = ['Home Probs', 'Away Probs'] 
    fair_odds = 1 / fair_probs
    fair_odds.columns = ['Home Odds', 'Away Odds']
    return fair_odds, fair_probs

def calculate_weighted_implied_probabilities(actual_odds: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate fair odds assuming the bookmaker margin is distributed
    proportionally based on odds — higher odds get less margin.

    Args:
        actual_odds (pd.DataFrame): DataFrame with 'Home Odds' and 'Away Odds'.

    Returns:
        (pd.DataFrame, pd.DataFrame): fair odds and fair probabilities
    """
    implied_probs = 1 / actual_odds
    margin = implied_probs.sum(axis=1) - 1.0  # total bookmaker margin

    # TODO try compute inverse-odds weights (lower odds → more margin share)
    weights = actual_odds.sum(axis=1).values.reshape(-1, 1) / actual_odds.values
    # Normalize weights so each row sums to 1
    normalized_weights = weights / weights.sum(axis=1).reshape(-1, 1)
    # Distribute the margin based on weights
    margin_allocation = normalized_weights * margin.values.reshape(-1, 1)
    # TODO redo formula 
    fair_probs = implied_probs.values - margin_allocation
    fair_probs_df = pd.DataFrame(fair_probs, columns=['Home Probs', 'Away Probs'])
    fair_odds_df = 1 / fair_probs_df
    fair_odds_df.columns = ['Home Odds', 'Away Odds']

    return fair_odds_df, fair_probs_df

def simulate_favourite_betting_strategy(odds, probs, outcomes, stake=10):
    """
    Simulate a betting strategy where you bet on the favourite team.
    
    Args:
        odds (pd.DataFrame): DataFrame containing 'Home Odds' and 'Away Odds'.
        probs (pd.DataFrame): DataFrame containing 'Home Probs' and 'Away Probs'.
        outcomes (pd.Series): Series with actual outcomes (1 for Home win, 0 for Away).
        stake (int): Amount to bet each time.
        
    Returns:
        np.ndarray: Array of profits for each bet. 
    """
    home_odds = odds["Home Odds"].values
    away_odds = odds["Away Odds"].values

    # Identify the favourite team based on odds
    is_home_favourite = home_odds < away_odds
    favourite_odds = np.where(is_home_favourite, home_odds, away_odds)

    # Determin if favourite team won
    favourite_wins = np.where(is_home_favourite, outcomes, 1 - outcomes)

    # Calculate total winnings
    profits = np.where(favourite_wins, (favourite_odds * stake) - stake, -stake)
    total_wins = np.sum(favourite_wins)

    return profits, total_wins 

def calculate_brier_score(probs, outcomes):
    """
    Calculate the Brier Score for the given probabilities and outcomes.
    """
    # Step 1: Brier Score (2-class: Home vs Away)
    probs = np.vstack([probs['Home Probs'], probs['Away Probs']]).T
    actuals = np.vstack([outcomes, 1 - outcomes]).T
    brier_score = np.mean(np.sum((probs - actuals) ** 2, axis=1))

    return brier_score

def plot_calibration_curve(odds_df, outcomes, n_bins=10, ax=None):
    """
    Plots a calibration curve: implied probability vs actual outcomes.
    
    Parameters:
        odds_df (pd.DataFrame): Columns ["Home Odds", "Away Odds"]
        outcomes (pd.Series): 1 = home win, 0 = away win
        n_bins (int): Number of bins to group probabilities
        ax (matplotlib.axes.Axes, optional): Axis to draw the plot on. If None, creates new.
    
    Returns:
        matplotlib.axes.Axes: The axis with the plotted calibration curve
    """
    assert "Home Odds" in odds_df and "Away Odds" in odds_df

    implied_home_prob = 1 / odds_df["Home Odds"]
    implied_away_prob = 1 / odds_df["Away Odds"]
    total_prob = implied_home_prob + implied_away_prob
    norm_home_prob = implied_home_prob / total_prob

    bins = np.linspace(0, 1, n_bins + 1)
    bin_ids = np.digitize(norm_home_prob, bins) - 1

    bin_centers = (bins[:-1] + bins[1:]) / 2
    avg_pred_prob = []
    actual_win_rate = []

    for i in range(n_bins):
        mask = bin_ids == i
        if np.sum(mask) == 0:
            continue
        avg_pred_prob.append(np.mean(norm_home_prob[mask]))
        actual_win_rate.append(np.mean(outcomes[mask]))

    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 6))

    ax.plot(avg_pred_prob, actual_win_rate, marker='o', label='Observed')
    ax.plot([0, 1], [0, 1], linestyle='--', color='gray', label='Perfect Calibration')
    ax.set_xlabel("Implied Home Win Probability")
    ax.set_ylabel("Observed Home Win Rate")
    ax.set_title("Calibration Plot")
    ax.grid(True)
    ax.legend()
    
    return ax

def plot_cumulative_profit(profits, ax=None):
    """
    Plots cumulative profit over time from a series of betting profits.
    
    Parameters:
        profits (pd.Series): Profit or loss for each bet (level stakes assumed)
        ax (matplotlib.axes.Axes, optional): If provided, plot on this axis
    
    Returns:
        matplotlib.axes.Axes: The axis with the plotted curve
    """
    cumulative_profit = profits.cumsum()
    
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 5))
    
    ax.plot(cumulative_profit, label="Cumulative Profit", color="blue")
    ax.axhline(0, color='gray', linestyle='--', linewidth=1)
    ax.set_xlabel("Bet Number")
    ax.set_ylabel("Cumulative Profit")
    ax.set_title("Cumulative Profit from Level-Stake Betting")
    ax.grid(True)
    ax.legend()
    
    return ax