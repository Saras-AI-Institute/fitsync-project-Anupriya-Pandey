import pandas as pd

def load_data():
    """
    This function loads the health data CSV file and processes it by handling missing values intelligently.
    - It fills missing 'Steps' with its median value,
    - Fills missing 'Sleep_Hours' with 7.0,
    - Fills missing 'Heart_Rate_bpm' with 68,
    - Fills other columns with their respective median,
    - Converts the 'Date' column to datetime objects.
    Returns:
    - A cleaned pandas DataFrame.
    """
    try:
        # Load the CSV file
    df = pd.read_csv('data/health_data.csv')
    
        # Fill missing values for 'Steps' with the median value
    if 'Steps' in df.columns:
        df['Steps'].fillna(df['Steps'].median(), inplace=True)
    
        # Fill missing values for 'Sleep_Hours' with 7.0
        if 'Sleep_Hours' in df.columns:
            df['Sleep_Hours'].fillna(7.0, inplace=True)
    
        # Fill missing values for 'Heart_Rate_bpm' with 68
        if 'Heart_Rate_bpm' in df.columns:
            df['Heart_Rate_bpm'].fillna(68, inplace=True)
    
        # Fill missing values for other columns with their median values
        for column in df.columns:
            if df[column].isnull().sum() > 0:
        df[column].fillna(df[column].median(), inplace=True)
    
        # Convert the 'Date' column to datetime objects
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
    
    return df

    except FileNotFoundError:
        print("The file 'health_data.csv' does not exist in the 'data' directory.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def calculate_recovery_score(df):
    """
    Calculate and add a 'Recovery_score' column to the DataFrame based on sleep hours, heart rate, and steps.

    Parameters:
        df (pd.DataFrame): DataFrame containing health metrics.

    Returns:
        pd.DataFrame: DataFrame with a new 'Recovery_score' column.
    """
    # Initialize 'Recovery_score' column with a base score of 50
    df['Recovery_score'] = 50

    # Adjust score based on Sleep Hours
    df.loc[df['Sleep_Hours'] >= 7, 'Recovery_score'] += 20  # Good sleep improves score
    df.loc[df['Sleep_Hours'] < 6, 'Recovery_score'] -= 15   # Poor sleep reduces score

    # Adjust score based on Heart Rate bpm
    df.loc[df['Heart_Rate_bpm'] <= 70, 'Recovery_score'] += 10  # Lower heart rate improves score
    df.loc[df['Heart_Rate_bpm'] > 85, 'Recovery_score'] -= 10   # Higher heart rate reduces score

    # Adjust score based on Steps
    df.loc[(df['Steps'] >= 8000) & (df['Steps'] <= 14000), 'Recovery_score'] += 5  # Moderate activity is good
    df.loc[df['Steps'] < 4000, 'Recovery_score'] -= 5   # Very low activity reduces score
    df.loc[df['Steps'] > 16000, 'Recovery_score'] -= 5  # High activity might cause strain
    # Ensure the Recovery_score stays within the range [0, 100]
    df['Recovery_score'] = df['Recovery_score'].clip(lower=0, upper=100)
    return df