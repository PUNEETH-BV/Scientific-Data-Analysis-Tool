import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def create_dummy_data(filename='experiment_data.csv'):
    """Creates a dummy dataset for demonstration purposes."""
    # Generate synthetic experimental data
    # Relationship: V = I * R + noise (Ohm's law with noise)
    np.random.seed(42)
    current = np.linspace(0, 10, 50)  # 0 to 10 Amps
    resistance = 5  # Ohms
    noise = np.random.normal(0, 2.5, 50) # Random noise
    voltage = current * resistance + noise
    
    # Introduce some missing values to demonstrate cleaning
    voltage[5] = np.nan
    voltage[15] = np.nan

    data = {
        'Current_A': current,
        'Voltage_V': voltage
    }
    
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Created dummy dataset: {filename}")
    return filename

def process_and_analyze(filename):
    """Ingests, cleans, analyzes, and visualizes the data."""
    
    # 1. Ingest Data
    if not os.path.exists(filename):
        print(f"Error: File {filename} not found.")
        return

    print(f"Loading data from {filename}...")
    df = pd.read_csv(filename)
    
    # 2. Data Cleaning (Pandas)
    print("Raw data shape:", df.shape)
    
    # Check for missing values
    if df.isnull().values.any():
        print("Missing values detected. Dropping incomplete rows...")
        df = df.dropna()
    
    print("Cleaned data shape:", df.shape)

    # Extract arrays for NumPy analysis
    current = df['Current_A'].values
    voltage = df['Voltage_V'].values

    # 3. Statistical Analysis (NumPy)
    print("\n--- Statistical Analysis ---")
    
    # Mean
    mean_v = np.mean(voltage)
    mean_i = np.mean(current)
    
    # Variance
    var_v = np.var(voltage)
    
    # Standard Deviation
    std_v = np.std(voltage)
    
    print(f"Voltage Mean: {mean_v:.2f} V")
    print(f"Voltage Variance: {var_v:.2f} V^2")
    print(f"Voltage Std Dev: {std_v:.2f} V")
    
    # Correlation Coefficient
    correlation = np.corrcoef(current, voltage)[0, 1]
    print(f"Correlation (Current vs Voltage): {correlation:.4f}")

    # 4. Visualization (Matplotlib)
    plt.figure(figsize=(10, 6))
    
    # Scatter plot of raw data
    plt.scatter(current, voltage, color='blue', label='Experimental Data', alpha=0.7)
    
    # Linear fit (Trend line)
    # Fit a polynomial of degree 1 (linear)
    m, b = np.polyfit(current, voltage, 1)
    plt.plot(current, m*current + b, color='red', linestyle='--', label=f'Linear Fit (R={resistance}Ω approx)')
    
    plt.title('V-I Characteristics (Ohm\'s Law Experiment)')
    plt.xlabel('Current (A)')
    plt.ylabel('Voltage (V)')
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.6)
    
    # Show plot
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Check if data exists, if not, create it
    data_file = 'experiment_data.csv'
    if not os.path.exists(data_file):
        create_dummy_data(data_file)
        
    process_and_analyze(data_file)
