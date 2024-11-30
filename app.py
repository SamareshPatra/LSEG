import os
import csv
import time
import math
import random


"""
/* Function to get the list of folders/files in the given directory */
Parameters:
    path from where inputs are taken
Returns:
    list: A list of folder/file names in the given directory.
"""
def get_content_in_given_path(input_path, check_type):
    global error    
    
    script_directory = os.path.dirname(os.path.abspath(__file__)) + input_path      # Get current_directory/input_path
    # Filter with check_type and get all folders/files inside given path
    try:
        if (check_type == 'folder'):
            folders = [item for item in os.listdir(script_directory) if os.path.isdir(os.path.join(script_directory, item))]
            if(len(folders)):
                return folders
            else:
                return False
        
        elif(check_type == 'file'):
            # files = [item for item in os.listdir(script_directory) if os.path.isfile(os.path.join(script_directory, item))]   # To check if files (all types) exist
            
            files = [item for item in os.listdir(script_directory) if item.lower().endswith('.csv')]    #To check if only csv file exist
            if(len(files)):
                return files
            else:
                return False
    except FileNotFoundError:
        print("Error: The folder or file name does not matched.")
        error = 1
    
    except Exception as e:
        print(f"An error occurred: {e}")

    return False


"""
/* Function to pickup random 30 consicutive records from given csv file*/
Parameters:
    path of the input file to proceed
Returns:
    return picked rows for next actions
"""
def pickup_input_from_file(full_input_file_path):
    global error
    input_file = os.path.dirname(os.path.abspath(__file__)) + full_input_file_path      # Get full path of market

    try:
        with open(input_file, 'r') as file:         
            row_count = sum(1 for _ in file)                    # Get total row count
            if (row_count > 30):
                start_row = random.randint(0, row_count - 29)   # Get random start row
                end_row = start_row + 29                        # Get consicutive 30 rows from preivious value
            else:
                if (row_count > 0 ):
                    start_row = 0
                    end_row = row_count - 1
            
        return start_row, end_row
    
    except FileNotFoundError:
        print(f"Error: The file at '{input_file}' does not exist.")
        error = 1
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return False

"""
/* Function to fetch data from input file and process for output */
Parameters:
    path for input file, starting row position ending row position
Return:
    .csv file as output
"""
def process_from_file(full_input_file_path, start_row, end_row):
    global error
    input_file = os.path.dirname(os.path.abspath(__file__)) + full_input_file_path      # Get full path of input file
    try:
        with open(input_file, 'r') as file:
            reader = list(csv.reader(file))                          # Convert CSV reader to a list
            header = ["Stock-ID", "Timestamp", "Stock Price Value"]  # Extract the header row
            data = reader[0:]                                        # Extract data rows
            selected_rows = data[start_row:end_row]                  # Extract 30 consecutive rows

        return selected_rows, header

    except FileNotFoundError:
        print(f"Error: The file at '{input_file}' does not exist.")
        error = 1
    except Exception as e:
        print(f"An error occurred: {e}")

    return False

"""
/* Function to calculate outliers and create csv file as output */
Parameters:
    fetched random 30 consecutive data, Output_header, output_folder_name
Return:
    .csv file as output
"""
def calculate_outliers(data, header, output_folder):
    stock_price_index = header.index("Stock Price Value")

    # Extract stock_price and calculate mean, standard deviation and threshold
    stock_price = [float(row[stock_price_index]) for row in data]
    mean = sum(stock_price) / len(stock_price)
    variance = sum((x - mean) ** 2 for x in stock_price) / len(stock_price)
    std_dev = math.sqrt(variance)
    threshold = mean + 2 * std_dev

    # Identify outliers
    outliers = []
    for row in data:
        actual_price = float(row[stock_price_index])
        if actual_price > threshold:
            deviation = actual_price - mean
            percent_deviation = ((deviation - 2 * std_dev) / (2 * std_dev)) * 100
            outliers.append(row + [round(mean, 2), round(deviation, 2), round(percent_deviation, 2)])   # Restrict values till 2 decimal
        
    try:
        # Prepare the output as CSV
        now = int(time.time())                                              # Use time value to avoid duplicate file name
        output_file_name = "./" + output_folder + "/" + str(now) + ".csv"   # Create output file path with file_name

        if outliers:
            output_header = header + ["30_data_mean", "actual_stock_price - mean", "percent_deviation"]
            
            with open(output_file_name, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(output_header)                               # Write header in output file
                for line in outliers:
                    writer.writerow(line)                                    # Write each row in output file
            print(f"Outliers have been written to '{output_file_name}'")
            return True
        else:
            print("No outliers found in the sampled data.")
            return True
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return False 
    
if __name__ == "__main__":
    input_folder = "/stock_price_data_files"                        # Take the input form this folder
    output_folder = "Output"                                        # Store the Output in this folder
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)                                  # Create the folder if was not before

    folders = get_content_in_given_path(input_folder, 'folder')     # Get all listed market
    if(folders != False):
        if folders:    
            for folder in folders:
                print(f"- {folder}")

            market_name = input("\n Select the Folder name from above for input: ").strip()
            full_market_path = str(input_folder + "/" + market_name)

            all_files = get_content_in_given_path(full_market_path, 'file')     # Get all available csv files
            if(all_files != False):
                file_count = len(all_files)

                if (file_count > 1):                            # Check if input files are more than 1, else process only available file
                    position = 1
                    for file in all_files:
                        print(f"{position} - {file}")           # Display files inside market
                        position = position + 1
                    
                    file_seq = int(input("\n Enter the file sequence from above to proceed (Example 1 or 2): "))      # Take input (as 1 or 2) file to process
                    while (file_seq > position - 1):
                        print("\n Sequence no is more than no of files we have, please use correct sequence no")
                        file_seq = int(input("\n Enter the file sequence from above to proceed (Example 1 or 2): "))      # Take input again if pressed by mistake instead of re-run the script
                        if(file_seq > position - 1):
                            continue
                    
                    index = file_seq - 1    
                    file_to_process = all_files[index]
                else:
                    file_to_process = all_files[0]
                
                full_input_file_path = full_market_path + "/" + file_to_process         # Create full path for file to proceed

                start_row, end_row = pickup_input_from_file(full_input_file_path)       # Pickup random start and end row no

                selected_rows, header = process_from_file(full_input_file_path, start_row, end_row)     # Fetch random 30 records, header
                
                if (calculate_outliers(selected_rows, header, output_folder)):          # Calculate outliers
                    print("\n Process completed")
                else:
                    print("Process Not completed")
            else:
                if(error != 1):
                    print("\n No files found in the same directory or Folder name entered wrong.")
    else:
        if (error != 1):
            print("\n No folders found in the same directory as this script.")
