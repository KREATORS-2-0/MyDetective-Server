import pandas as pd
import traceback
import os
import keyboard

from lie_detection import model
from biosensor_streamer import BiosensorStreamer


class LieAnalyzer():
    def __init__(self):
        self.eeg_data = pd.DataFrame(columns=BiosensorStreamer.columns)
        self.streamer = BiosensorStreamer()
        self.analysis_result = ""

    def reset_data(self):
        self.eeg_data = pd.DataFrame(columns=BiosensorStreamer.columns)
        return self.eeg_data

    def start_streaming(self):
        try:
            self.streamer.start_streaming()
            print("Press 'esc' to stop streaming...")

        except Exception as e:
            # Print out any other exceptions that might occur
            print(f"An error occurred: {e}\n")
            # Print the full stack trace using traceback
            traceback.print_exc()
            print("\n")

    def stop_streaming(self):
        self.streamer.stop_streaming()

    def append_data(self, print_data=False):
        while True:
            partial_eeg_data = self.streamer.read_data()
            if print_data:
                self.streamer.display_data(partial_eeg_data)
            self.eeg_data = pd.concat([self.eeg_data, partial_eeg_data], axis=0, ignore_index=True)

            if keyboard.is_pressed("esc"):
                break
        return

    def write_as_csv_data(self, dataframe, data_dir, filename):
        if dataframe is None or dataframe.empty:
            return False
        
        # Get the directory of the current script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Create the data directory if it doesn't exist
        os.makedirs(os.path.join(current_dir, "..", data_dir), exist_ok=True)
        # Path to the file in the data directory
        filepath = os.path.join(data_dir, filename)
        # Write the data to the file
        dataframe.to_csv(filepath, index=False)
        return True

    def analyze(self):
        # write eeg_data into CSV file
        self.write_as_csv_data(self.eeg_data, "data", "temp_eeg.csv")
        # update analysis_result
        # Get the directory of the current script
        current_dir = os.path.dirname(os.path.abspath(__file__))

        self.analysis_result = model(os.path.join(current_dir, "..", "data", "temp_eeg.csv"))
        # reset the eeg_data
        self.reset_data()
        return True