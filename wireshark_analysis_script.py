import pandas as pd
import matplotlib.pyplot as plt
import os

# Mapping for time resolution options.
# "s": seconds, "ms": milliseconds, "us": microseconds, "ps": picoseconds.
resolution_multipliers = {
    "s": 1,
    "ms": 1e3,
    "us": 1e6,
    "ps": 1e12
}


def analyze_csv_by_protocol(csv_file, resolution="s", max_time=10.0):
    """
    Reads a Wireshark-exported CSV file and generates graphs for each protocol.

    For each protocol, the script:
      - Filters the data to only include packets up to max_time seconds.
      - Groups packets into bins of the specified resolution (s, ms, us, or ps).
      - Calculates packets per bin, the mean, and standard deviation.
      - Plots a graph with time (in seconds) on the X-axis and packet count on the Y-axis,
        showing the mean (as a horizontal line) and a shaded area representing ± one standard deviation.

    The graphs are saved in the "output_graphs" directory.
    """
    # Get the multiplier based on resolution choice.
    multiplier = resolution_multipliers[resolution]

    # Load the CSV into a DataFrame.
    df = pd.read_csv(csv_file)
    figure_name = os.path.basename(csv_file).split('.')[0]

    # We assume the CSV has at least "Time" and "Protocol" columns.
    # Convert "Time" to numeric.
    df["Time"] = pd.to_numeric(df["Time"], errors='coerce')
    df.dropna(subset=["Time", "Protocol"], inplace=True)

    # Normalize time so that the first packet starts at 0 seconds.
    min_time = df["Time"].min()
    df["time_offset"] = df["Time"] - min_time

    # Filter the data to only include packets up to max_time seconds.
    df = df[df["time_offset"] <= max_time]

    # Create a new column 'time_bin' by converting the time_offset to the chosen resolution.
    # For instance, if resolution is "ms", each bin corresponds to 0.001 sec.
    df["time_bin"] = (df["time_offset"] * multiplier).astype(int)

    # Create output directory for graphs.
    output_dir = "output_graphs"
    os.makedirs(output_dir, exist_ok=True)

    # Get the unique protocols.
    protocols = df["Protocol"].unique()

    # Loop through each protocol and generate its graph.
    for proto in protocols:
        # Filter data for the current protocol.
        df_proto = df[df["Protocol"] == proto]
        # Group by the time_bin and count packets per bin.
        grouped = df_proto.groupby("time_bin").size().reset_index(name="packets")
        # Convert time_bin back to seconds for the X-axis.
        grouped["time_sec"] = grouped["time_bin"] / multiplier

        # Calculate the mean and standard deviation.
        mean_val = grouped["packets"].mean()
        std_val = grouped["packets"].std()

        # Plot the graph for the current protocol.
        plt.figure(figsize=(12, 6))
        plt.plot(grouped["time_sec"], grouped["packets"], marker="o", linestyle="-",
                 label=f"{proto} packets per {resolution} bin")
        plt.axhline(mean_val, color="green", linestyle="--", label=f"Mean: {mean_val:.2f}")
        plt.fill_between(grouped["time_sec"], mean_val - std_val, mean_val + std_val, color="green", alpha=0.2,
                         label=f"Std Dev: {std_val:.2f}")
        plt.xlabel("Time (seconds)")
        plt.ylabel(f"Packets per {resolution.upper()} bin")
        plt.title(f"{proto} Packets per {resolution.upper()} bin (0 - {max_time} sec)")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        # Save the graph.
        output_path = os.path.join(output_dir, f"{figure_name}_{proto}_packets_per_{resolution}_up_to_{max_time}_sec.png")
        plt.savefig(output_path)
        plt.close()
        print(f"Graph for protocol {proto} saved to {output_path}")


if __name__ == "__main__":
    # Specify the path to your CSV file.
    csv_file = "/Users/baruhifraimov/Desktop/CYBER/cyber_lab/rep2/3302025_TARHISH_2/figures/trahish_2_raz/response.csv"

    # Ask the user for resolution and maximum time.
    resolution = input(
        "Enter resolution (s for seconds, ms for milliseconds, us for microseconds, ps for picoseconds): ").strip().lower()
    if resolution not in resolution_multipliers:
        print("Invalid resolution option. Defaulting to seconds ('s').")
        resolution = "s"
    max_time = float(input("Enter the maximum time (in seconds) to include: "))

    analyze_csv_by_protocol(csv_file, resolution, max_time)
