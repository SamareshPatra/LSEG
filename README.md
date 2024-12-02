# LSEG
Script to find outliers from Input

# What this script does?
This script contains input from user as 1 or 2 or no of file wants to process from the selected market folder where output will be generated as CSV file based on randomly selected 30 consecutive rows from the input file with additional fields - mean of 30 data points, actual stock price – mean, % deviation over and above the threshold if found any.

# How to setup the system to run this script?
1. Optoion 1 :
-  With the minimum setup we can run this script. Only Python (python 3 onwards) needs to install in your system to run this script.
To install Python this link (https://www.dataquest.io/blog/installing-python-on-mac/) can be followed or can download from here (https://www.python.org/downloads/) for installation.
-  Once above setup is completed and "python3 --version" is returing result, we are good to follow next step.
-  Now we need to bring the code in local - follow below commands (if github setup is there in sysyem) :
   1. "git clone git@github.com:SamareshPatra/LSEG.git"
   2. Now code has come to your current directory
   3. We need input now before running teh script. "stock_price_data_files" folder you need to place in same directory after unzipping.
(we have skip this step as provided data were not confidencial, so we have added this folder in git code)
   4. Output folder will be created once the code runs first time. We are keeping output in different folder to keep the output files organised.
-  Now we are good with the setup. We just need to run below command to run the script - 
    "python3 app.py"

2. Option 2:
   - If docker is installed in your system, then we have created one docker image here (https://hub.docker.com/r/sampat17/findoutliers/tags).
   - Please run the command - "docker pull sampat17/findoutliers:v1.0" or "docker pull sampat17/findoutliers" to pull the image in local. 
   - We can run this docker image to execute the script. To run the image - please use below command as user needs to interact by providing inputs from terminal. If we do not use '-it' we will end up by 'EOFError: EOF when reading a line error'.
"docker run -it sampat17/findoutliers"


# Execution flow of this script:
1. Execute the script
2. System will ask for which market user wants to select (among the folders we have inside 'stock_price_data_files')
3. Once market is selected, then system will ask for which file to proceed (based on no of files are there inside, input can be given)
4. Based on the input user has given - randon 30 consicutive rows will be selected from input file and if any datapoint that is over 2 standard deviations beyond the mean of the 30 sampled data points - found then one CSV file will be created with this datapoint outliers inside Output folder.

