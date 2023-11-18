import os
import traceback
import pandas as pd
import keyboard
from eeg.src.eeg_streamer import EEGStreamer

class FileIO:
    def __init__(self, default_data_dir=os.path.join("..", "data"), default_filename="default_name.csv"):
        self.data_dir = default_data_dir
        self.default_filename = default_filename

    def save_data(self, dataframe, filename=None):
        if filename is None:
            filename = self.default_filename

        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(current_dir, self.data_dir)
        file_path = os.path.join(data_path, filename)

        if os.path.exists(file_path):
            print(f"\nA file named {filename} already exists in the data directory.\n")
            print("Select an option:")
            print("\t1. Append data to the existing file. Type (a/append).")
            print("\t2. Save data in a new file. Type (n/new/new_file).")
            print("\t3. Overwrite the existing file. Type (o/overwrite).")
            print("\t4. Delete current data frame. Type(d/delete).")
            print("\n")
            option = input("\nEnter your option: ")
            print("\n")

            if option.lower() in ['a', 'append']:
                try:
                    dataframe.to_csv(file_path, mode='a', header=False, index=False)
                    print(f"Data appended at: {os.path.abspath(file_path)}")
                except Exception as e:
                    print(f"Data append error occurred: {e}")
                    return
            elif option.lower() in ['n', 'new', 'new_file']:
                new_filename = input("Enter the new filename: ")
                new_data_path = os.path.join(data_path, new_filename)
                try:
                    dataframe.to_csv(new_data_path, index=False)
                    print(f"Data saved at: {os.path.abspath(new_data_path)}")
                except Exception as e:
                    print(f"Data save error occurred: {e}")
                    return
            elif option.lower() in ['o', 'overwrite']:
                try:
                    dataframe.to_csv(file_path, index=False)
                    print(f"Data overwritten at: {os.path.abspath(file_path)}")
                except Exception as e:
                    print(f"Data overwrite error occurred: {e}")
                    return
            elif option.lower() in ['d', 'delete']:
                print("Data not saved.")
                return
            else:
                print("Invalid option. Data not saved.")
                return self.save_data(dataframe, filename)
        else:
            # Save the data in a new file if the file does not exist
            try:
                dataframe.to_csv(file_path, index=False)
                print(f"Data saved at: {os.path.abspath(file_path)}")
            except Exception as e:
                print(f"Data save error occurred: {e}")
                return
            

if __name__ == "__main__":
    df = pd.DataFrame(columns=['EXG Channel 1', 'EXG Channel 2', 'EXG Channel 3', 'EXG Channel 4', 'Timestamp', 'Response'])
    streamer = EEGStreamer(sampling_rate=0.001) # port number and sampling rate in seconds
    file_io = FileIO()

    escape = False
    try:
        streamer.start_streaming()
        while not escape:
            if keyboard.is_pressed("q"):
                escape = True

            temp_df = streamer.read_data()
            if temp_df is not None:
                response = "yes" if keyboard.is_pressed("left") else ""
                temp_df['Response'] = response
                df = pd.concat([df, temp_df], ignore_index=True)
                streamer.display_data(df)  # Use the renamed method

    except KeyboardInterrupt:
        file_io.save_data(df)  # Will use the instance's default filename
        print("\nKeyboard interrupted.")
        print("Program terminated by user.\n")

    except Exception as e:
        # Print out any other exceptions that might occur
        print(f"An error occurred: {e}\n")
        # Print the full stack trace using traceback
        traceback.print_exc()
        print("\n")

    finally:
        streamer.stop_streaming()
        if not df.empty:
            file_io.save_data(df)
        else:
            print("No data collected. Nothing to save.")