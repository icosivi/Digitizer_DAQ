import ROOT as rt
from array import array
import ctypes, os, math

MAX_FILE_SIZE = 500 # GB
CHANNELS = 32

class TreeFile():

    def __init__(self, path, name, event_length, compression = 1):
        path = os.path.join(path, "{}.root".format(name))

        while(os.path.isfile(path)):
            path = path.replace(".root", "_.root")
        self.file = rt.TFile(path, "RECREATE", name, compression)
        self.tree = rt.TTree("wfm", "Digitizer waveforms")
        self.tree.SetMaxTreeSize(math.floor(MAX_FILE_SIZE * 1E9))

        self.event_length = event_length

        self.length = array("f", [float(event_length)])
        self.tree.Branch("size", self.length, "size/F")

        self.ttt = array("I", [0])
        self.tree.Branch("ttt", self.ttt, "ttt/i")

        self.evtcnt = array("I", [0])
        self.tree.Branch("evtcnt", self.evtcnt, "evtcnt/i")

        self.channels = []
        for c in range(CHANNELS):
            wave = array("f", [0.0] * event_length)
            self.tree.Branch("w{}".format(c), wave,
                "w{}[{}]/F".format(c, event_length))
            self.channels.append(wave)

        # one digitized trigger for each group of 8 channels
        self.triggers = []
        for t in range(int(CHANNELS / 8)):
            wave = array("f", [0.0] * event_length)
            self.tree.Branch("trg{}".format(t), wave,
                "trg{}[{}]/F".format(t, event_length))
            self.triggers.append(wave)

    def fill(self):
        self.tree.Fill()

    def write(self):
        self.file.Write()

    def close(self):
        self.file.Write()
        self.file.Close()

    def setEventInfo(self, ttt, evtcnt):
        self.ttt[0] = ttt
        self.evtcnt[0] = evtcnt

    def setChannel(self, index, data, length):
        ctypes.memmove(
            self.channels[index].buffer_info()[0],
            ctypes.cast(data, ctypes.c_void_p).value,
            length * 4)

    def setTrigger(self, index, data, length):
        ctypes.memmove(
            self.triggers[index].buffer_info()[0],
            ctypes.cast(data, ctypes.c_void_p).value,
            length * 4)
