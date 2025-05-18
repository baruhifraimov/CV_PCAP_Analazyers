import pandas as pd
import matplotlib.pyplot as plt
import os

# Path to your CSV file
csv_file = "/Users/baruhifraimov/Desktop/CYBER/cyber_lab/rep2/3302025_TARHISH_1/figures/תיעוד_חומת_אש.csv"

# Load the CSV file into a DataFrame
df = pd.read_csv(csv_file)

# Check if the 'Time' column is numeric. If not, try to convert it from datetime.
if not pd.api.types.is_numeric_dtype(df["Time"]):
    try:
        df["Time"] = pd.to_datetime(df["Time"], errors='coerce')
        # Convert to epoch seconds (nanoseconds to seconds)
        df["Time"] = df["Time"].astype('int64') // 10 ** 9
    except Exception as e:
        print("Error converting 'Time' column:", e)
else:
    df["Time"] = pd.to_numeric(df["Time"], errors='coerce')

# Drop rows with missing or non-parsable Time values
df.dropna(subset=["Time"], inplace=True)

if df.empty:
    print("No valid Time data found in the CSV.")
else:
    # Normalize time so that the first event starts at 0 seconds
    min_time = df["Time"].min()
    df["time_offset"] = df["Time"] - min_time

    # Create a new column 'second' by converting the time_offset to integer seconds
    df["second"] = df["time_offset"].astype(int)

    # Group the data by 'second' and count the number of events per second
    events_per_second = df.groupby("second").size().reset_index(name="events")

    if events_per_second.empty:
        print("No events found after grouping by second. Please check the CSV file format.")
    else:
        # Create an output directory for the graph if it doesn't exist
        output_dir = "output_graphs"
        os.makedirs(output_dir, exist_ok=True)

        # Plot the graph
        plt.figure(figsize=(12, 6))
        plt.plot(events_per_second["second"], events_per_second["events"], marker="o", linestyle="-", color="red")
        plt.xlabel("Time (seconds)")
        plt.ylabel("Number of Events")
        plt.title("Firewall Events per Second during DNS Amplification Attack")
        plt.grid(True)
        plt.tight_layout()

        # Save and show the graph
        output_path = os.path.join(output_dir, "firewall_events_per_second.png")
        plt.savefig(output_path)
        plt.show()

        print(f"Graph saved to {output_path}")
