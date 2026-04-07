def load_data():
    try:
        df = pd.read_csv('data/health_data.csv')
        
        # Process the data here ...
        
        return df
        
    except FileNotFoundError:
        print("The file 'health_data.csv' does not exist in the 'data' directory.")
        return None
    except pd.errors.EmptyDataError:
        print("The file 'health_data.csv' is empty.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
