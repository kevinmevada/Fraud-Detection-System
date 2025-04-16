import pandas as pd
import numpy as np

def load_data(file_path='creditcard.csv'):
    """
    Load transaction data from a CSV file.
    
    Args:
        file_path (str): Path to the CSV file (default: 'creditcard.csv').
    
    Returns:
        pd.DataFrame: Loaded transaction data.
    
    Raises:
        FileNotFoundError: If the CSV file is not found.
        ValueError: If required columns are missing or the file is empty.
    """
    try:
        data = pd.read_csv(file_path)
        required_columns = ['Time', 'Amount', 'Class']
        if not all(col in data.columns for col in required_columns):
            raise ValueError(f"Missing required columns: {required_columns}")
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"Could not find {file_path}. Please ensure the file exists.")
    except pd.errors.EmptyDataError:
        raise ValueError(f"{file_path} is empty or corrupted.")

def process_real_time(data, batch_size=10):
    """
    Simulate real-time transaction data by sampling and modifying a batch of transactions.
    
    Args:
        data (pd.DataFrame): Input transaction data.
        batch_size (int): Number of transactions to simulate (default: 10).
    
    Returns:
        pd.DataFrame: Simulated real-time transaction data.
    """
    new_data = data.sample(n=min(batch_size, len(data))).copy()
    new_data['Amount'] = np.maximum(0, new_data['Amount'] + np.random.normal(0, 10, len(new_data)))
    new_data['Time'] = new_data['Time'] + np.random.randint(1, 100, len(new_data))
    return new_data