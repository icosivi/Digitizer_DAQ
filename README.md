------ Acquisition with 2 digitizers with the UFSDPyDAQ suite ------

-   Run the setup of the CAEN dependancies
        source setup.sh
The two digitizers run in parallel, everything is doubled
-   First check the LinkNums: 
        1) turn on and connect ONE digitizer
        2) execute the FindDigitizer script
                ./FindDigitizer.bin
        3) write down the number found
        4) turn on and connect the second digitizer
                -> the LinkNum of the second device should be sequential (i.e. if the first one had LinkNum=3 the second should be LinkNum=4)
        5) check if it is possible to connect to both digitizers using wavedump by editing the UNCOMMENTED line that contains 
                OPEN USB xxx 0
           where xxx corresponds to the desired LinkNum. Wavedump can be executed using the command
                wavedump wavedump_config_file
           Examples of wavedump config files can be found in the config_wavedump/ folder.
-   Check the thresholds on the input trigger by employing wavedump:
        edit the WaveDumpConfig_X742.txt file in the [TR0] section. 
                DC_OFFSET              30000  should corresponds to the baseline offset from which the threshold is computed. Normally a value of 30000 is reasonable for signals with baseline ~= 0 and normally does not need tuning 
                TRIGGER_THRESHOLD      31000  is the value corresponding to the threshold. N.B. 1 ADC count corresponds to about .25 mV
        additional bonus parameters to be set are
                POST_TRIGGER  0 moves the trigger within the time acquisition window. To be tuned with the setup (cables, trigger generation delay, etc.) 
                PULSE_POLARITY  POSITIVE polarity of the trigger (? probably, was set to positive)
                FAST_TRIGGER   ACQUISITION_ONLY	needed to enable the tr0 channel
                ENABLED_FAST_TRIGGER_DIGITIZING		YES	needed to digitize the tr0 channel
                DC_OFFSET              0 baseline level
                DRS4_FREQUENCY 0 should be set to 0 for 5 GS/s acquisition
        some examples are provided at the end of the config file
-   Edit the config_1.ini and config_2.ini files with the optimized values found in the previous steps. Make sure to put the same amount of events in the "MAX_EVENTS" field to avoid mismatch between acquisitions. Make sure to set the [STAGE] and [HIGHVOLTAGE] fields to manual so that they are not activated.
-   Open two terminals and navigate to /home/daq/Desktop/DigiDAQ/UFSDPyDAQ_FAST3_DESY, execute `python3 1_main.py` in the first terminal and `python3 2_main.py` in the second.

Happy DESY acquisition!


OPTIONAL: a script that starts the flow {backup->analysis->merge->corry analysis->tracks+stats merge} once the acquisition is finished could be a smart thing to develop.
