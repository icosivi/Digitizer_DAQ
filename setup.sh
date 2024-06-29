GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}installing CAEN Digitizer packages${NC}"
#CAENVMELib
cd /home/daq/Desktop/DigiDAQ/Drivers/Digitizer/from_ws_lab/CAENVMELib-v3.4.1/lib
sudo ./install_x64
echo -e "CAENVMELib installed"
#CAENComm
cd /home/daq/Desktop/DigiDAQ/Drivers/Digitizer/from_ws_lab/CAENComm-v1.6.0/lib
sudo ./install_x64
echo -e "CAENComm installed"
#CAENDigitizer
cd /home/daq/Desktop/DigiDAQ/Drivers/Digitizer/from_ws_lab/CAENDigitizer-v2.17.3/lib
sudo ./install_x64
echo -e "CAENDigitizer installed"
#CAEN USB
cd /home/daq/Downloads/CAENUSBdrvB-1.5.5
sudo make && sudo make install
echo -e "CAENUSB installed"
echo -e "${GREEN}finished with the setup of CAEN dependancies${NC}"
cd /home/daq/Desktop/DigiDAQ/UFSDPyDAQ_FAST3_DESY
