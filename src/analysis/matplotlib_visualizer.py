import matplotlib
import matplotlib.pyplot as plt
import numpy as np


matplotlib.use("TkAgg")

def plot_results(mode, stock_name, threshold, df, period):
    """
    Plot financial data with different handling for Train vs Test periods.
    """

    
    plt.figure(figsize=(20, 10))
    
    df_plot = df.copy()
    days_count = len(np.unique(df_plot.index.date))
    
    # Filter to trading hours if intraday
    if mode == "Intraday":
        df_plot = df_plot[
            (df_plot.index.hour >= 11) & (df_plot.index.hour < 15)
        ]
    
    # Create sequential x-axis for clean plotting
    x_values = np.arange(len(df_plot))
    
    # Plot lines
    plt.plot(x_values, df_plot['close'], label=f"{stock_name} close ({period} Period)")
    plt.plot(x_values, df_plot['SMA_5'], label='SMA 5', linestyle='--', zorder=3)
    plt.plot(x_values, df_plot['SMA_20'], label='SMA 20', linestyle='--', zorder=3)
    plt.plot(x_values, df_plot['EMA_10'], label='EMA 10', linestyle='-.', zorder=3)
    
    # Plot anomalies
    anomaly_mask = df_plot['anomalous'].values
    plt.scatter(
        x_values[anomaly_mask],
        df_plot.loc[anomaly_mask, 'close'].values,
        color='red',
        label=f"Detected anomalies ({period})",
        zorder=5,
    )
    
    # Set x-axis labels based on period
    if mode == "Intraday" and period == "Test":
        # Test: Show ~6 labels per day (times only)
        step = max(1, len(x_values) // (6 * days_count))
        plt.xticks(
            x_values[::step],
            [t.strftime('%H:%M') for t in df_plot.index[::step]],
            rotation=45
        )
    elif mode == "Intraday" and period == "Train":
        # Train: Show dates only (one per day)
        step = max(1, len(x_values) // days_count)
        plt.xticks(
            x_values[::step],
            [t.strftime('%m-%d') for t in df_plot.index[::step]],
            rotation=45
        )
    else:
        # Daily data: Show date labels
        step = max(1, len(x_values) // 10)
        plt.xticks(
            x_values[::step],
            [t.strftime('%Y-%m-%d') for t in df_plot.index[::step]],
            rotation=45
        )
    
    title = f"{stock_name} close with IsolationForest anomalies & Moving Averages ({period} Period)"
    plt.title(title)
    plt.xlabel('Transaction Time')
    plt.ylabel('Close Price')
    plt.legend()
    plt.tight_layout()
    plt.show()
    
    # Diagnostics
    title = f"Distribution of IsolationForest anomaly scores ({period} set)"
    plt.figure(figsize=(12, 5))
    plt.hist(df_plot['anomaly_score'], bins=50, color='steelblue', edgecolor='black')
    plt.axvline(threshold, color='red', linestyle='--', label='Anomaly threshold')
    plt.title(title)
    plt.xlabel('Anomaly score (higher = more anomalous)')
    plt.ylabel('Frequency')
    plt.legend()
    plt.tight_layout()
    plt.show()
    
    print(f'Anomaly counts in {period} set:')
    print(df_plot['anomalous'].value_counts())