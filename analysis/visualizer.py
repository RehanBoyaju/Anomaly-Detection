import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("TkAgg") #use Tkinter library to use the GUI Engine to display results


def plot_results(stock_name,threshold,df_train,df_test):
    # Plot rate with detected anomalies on the test period

    plt.figure(figsize=(20, 10))
    # Plot test rate rates
    plt.plot(df_test.index, df_test['rate'], label=f"{stock_name} rate (Test Period)")

    # Plot moving averages (only for test period)
    plt.plot(df_test.index, df_test['SMA_5'], label='SMA 5', linestyle='--', zorder=3)
    plt.plot(df_test.index, df_test['SMA_20'], label='SMA 20', linestyle='--', zorder=3)
    plt.plot(df_test.index, df_test['EMA_10'], label='EMA 10', linestyle='-.', zorder=3)

    # Highlight anomalies
    anomaly_idx = df_test.index[df_test['Anomaly_IF']]
    plt.scatter(
        anomaly_idx,
        df_test.loc[anomaly_idx, 'rate'],
        color='red',
        label='Detected anomalies (test)',
        zorder=5
    )
    #draws points with x-axis anomalies, y-axis is price of the anomalies. df_test is the test data, loc lets you select the rows by labels and specific columns. i.e the label is the list or index of dates where indexes appear
    #so we select all the rows in anomaly idx and from each row get the value of 'rate Column'

    plt.title(f"{stock_name} rate with IsolationForest anomalies & Moving Averages (test period)")
    plt.xlabel('transaction_time')
    plt.ylabel('rate')
    plt.legend()
    plt.show()

    # df_to_save = df[['rate','quantity','return','SMA_5', 'SMA_20', 'EMA_10']].copy()

    # df_to_save.to_csv("output_plotted_data.csv")







    # Diagnostics: distribution of anomaly scores and counts
    plt.figure(figsize=(12, 5))
    plt.hist(df_test['anomaly_score'], bins=50, color='steelblue', edgecolor='black')
    #draws 50 histogram blocks with blue fills and black borders based on the anomaly score of test data
    plt.axvline(threshold, color='red', linestyle='--', label='Anomaly threshold')
    #draws a vertical red line at threshold value. right side of threshold is anomalies
    plt.title('Distribution of IsolationForest anomaly scores (test set)')
    plt.xlabel('Anomaly score (higher = more anomalous)')
    plt.ylabel('Frequency')
    plt.legend()
    plt.tight_layout() #this is to make sure the plot is not too crowded
    plt.show()

    print('Anomaly counts in test set:')
    print(df_test['Anomaly_IF'].value_counts())

    #shows the count of anomalies and normal points
    #also shows that roughly 2% of data were anomalies 