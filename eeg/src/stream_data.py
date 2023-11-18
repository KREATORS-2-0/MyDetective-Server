import keyboard
import traceback
from eeg.src.eeg_streamer import EEGStreamer


def escape_function():
    if keyboard.is_pressed("q"):
        return True

if __name__ == "__main__":
    sampling_rate = 0.001
    results_file = "results.json"
    streamer = EEGStreamer(sampling_rate=sampling_rate) # port number and sampling rate in seconds

    
    try:
        streamer.start_streaming()
        print("Press 'q' to stop streaming...\n")

        escape = False
        while not escape:
            escape = escape_function()
            new_data = streamer.read_data()
            if new_data is not None and not new_data.empty:
                # Convert only the last row of the DataFrame to JSON
                # Using 'records' orientation which gives a list of rows
                json_data = new_data.to_json(orient='records', lines=True)
                # Since it's a list with a single record, we can strip the square brackets to get a single JSON object
                json_data = json_data.strip("[]") 
                # Ensure the line is long enough to overwrite any previous output
                # line_to_print = f'\r{json_data}' + ' ' * (80 - len(json_data))
                # print(line_to_print, end='', flush=True)

                with open(results_file, 'w') as f:
                    f.write(json_data)


    except KeyboardInterrupt:
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