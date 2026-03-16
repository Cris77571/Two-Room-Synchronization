# Two-Room-Synchronization
 * Python code for the two-room testbed. Don't need to open up instacal.
 * Got the base code to use the MCC DAQ from their website
 * If you want to run the file, make sure to change the filename to your path on line 114

# How to Set-up the Experiment using Visual Studio to Operate the Testbed
1.	First, make sure all connections are plugged in for the DAQ, Raspberry Pi, Kasa Smart Plugs/Camera, and the Arduino.
2.	Open up Visual Studio and open up the file called “TC Temperature Reader”.
3.	Turn on the Wi-Fi connection to the network called “HVAC Lab”, if not turned on, the code will run an error.
4.	Turn on the DAQ system, if it is not turned on, the code will run an error as well.
5.	Turn on the power supplies.
6.	From this point, click the “Output” button on the power supplies to allow the voltage and current to run.
7.	The code can now be ran and will run for 60 hours, the data will be saved to your specific file path written in the code.
8.	While the test runs for 60 hours, to be able to step away from the experiment, click on OBS and start streaming. **Note**: A Twitch account is needed for this step. IF you don’t have Twitch, YouTube can be used as well, however, a one day waiting period is needed to set-up the account. 
9.	After, the 60 hour test is completed. Switch off the power supplies, Arduino, Smart Plugs/Camera, and Raspberry Pi.
10.	 The data will be saved to the direct path you created in the code. 

