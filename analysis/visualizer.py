import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.use("TkAgg") #use Tkinter library to use the GUI Engine to display results


def plot_results(mode,stock_name,threshold,df,period):
    """
    Filter out non-trading hours before plotting.
    Pros: Keeps datetime labels, removes gaps
    Cons: Requires datetime index
    """


    plt.figure(figsize=(20, 10))
    

    df_plot = df.copy();

    days_count = len(np.unique(df_plot.index.date))
    


    # Filter to only trading hours (11:00 to 15:00) if we are dealing with intraday data

    if mode == "Intraday":
        df_plot = df_plot[
            (df.index.hour >= 11) & (df.index.hour < 15)
        ]
    
    
    
    # Create sequential x-axis but keep datetime info in hover/labels
    x_values = np.arange(len(df_plot))
    
    plt.plot(x_values, df_plot['close'], label=f"{stock_name} close ({period} Period)")
    plt.plot(x_values, df_plot['SMA_5'], label='SMA 5', linestyle='--', zorder=3)
    plt.plot(x_values, df_plot['SMA_20'], label='SMA 20', linestyle='--', zorder=3)
    plt.plot(x_values, df_plot['EMA_10'], label='EMA 10', linestyle='-.', zorder=3)
    
    anomaly_mask = df_plot['anomalous'].values

    plt.scatter(
        x_values[anomaly_mask],
        df_plot.loc[anomaly_mask, 'close'].values,
        color='red',
        label=f"Detected anomalies ({period})",
        zorder=5
    )
    
    # Set custom x-axis labels showing actual times (every Nth point), i.e 5 labels per day
    step = max(1, len(x_values) // (5 * days_count)) 
    plt.xticks(
        x_values[::step],
        [t.strftime('%H:%M') for t in df_plot.index[::step]],
        rotation=45
    )
    
    title = f"{stock_name} close with IsolationForest anomalies & Moving Averages ({period} Period)";
    plt.title(title)
    plt.xlabel('Transaction Time')
    plt.ylabel('Close Price')
    plt.legend()
    plt.tight_layout()
    plt.show()







    # Diagnostics: distribution of anomaly scores and counts

    title = f"Distribution of IsolationForest anomaly scores ({period} set)";
    plt.figure(figsize=(12, 5))
    plt.hist(df_plot['anomaly_score'], bins=50, color='steelblue', edgecolor='black')
    #draws 50 histogram blocks with blue fills and black borders based on the anomaly score of test data
    plt.axvline(threshold, color='red', linestyle='--', label='Anomaly threshold')
    #draws a vertical red line at threshold value. right side of threshold is anomalies
    plt.title(title)
    plt.xlabel('Anomaly score (higher = more anomalous)')
    plt.ylabel('Frequency')
    plt.legend()
    plt.tight_layout() #this is to make sure the plot is not too crowded
    plt.show()

    print(f'Anomaly counts in {period} set:')
    print(df_plot['anomalous'].value_counts())

    #shows the count of anomalies and normal points
    #also shows that roughly 2% of data were anomalies 