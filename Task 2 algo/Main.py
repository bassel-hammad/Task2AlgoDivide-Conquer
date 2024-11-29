import cmath
from PyQt5.QtWidgets import *
import wfdb
from PyQt5 import QtCore, QtGui, QtWidgets
from New import Ui_MainWindow
import os
import numpy as np
import pandas as pd  
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.graph = self.ui.FrequencyGraph
        self.Freqgraph = self.ui.Graph
        self.file = False
        # self.ui.pushButton_3.clicked.connect(self.zoom_in)
        # self.ui.pushButton_4.clicked.connect(self.zoom_out)
        self.ui.actionOpen.triggered.connect(self.OpenFile)

    def OpenFile(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Supported files (*.hea *.csv)")
        file_dialog.setWindowTitle("Open File")
        file_dialog.setFileMode(QFileDialog.ExistingFile)

        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            file_extension = os.path.splitext(file_path)[1].lower()

            if file_extension == ".hea":
                self.process_hea_file(file_path)
            elif file_extension == ".csv":
                self.process_csv_file(file_path)
            else:
                QMessageBox.warning(self, "Invalid File", "Unsupported file type!")
                return

            self.file = True

    def process_hea_file(self, file_path):
        record = wfdb.rdrecord(file_path[:-4])
        self.sample_rate = record.fs
        self.audio_data = record.p_signal[:, 0]
        self.XtimeValues = np.arange(len(self.audio_data)) / self.sample_rate
        self.YAmpValues = self.audio_data
        self.plotgraph(self.XtimeValues, self.YAmpValues)
        fft_result = self.cooley_tukey_fft(self.audio_data)
        self.plot_fft(fft_result)

    def process_csv_file(self, file_path):
        try:
            # Load CSV data using pandas
            data = pd.read_csv(file_path)
            
            # Assuming the first column is time and the second column is amplitude
            if "time" in data.columns and "amplitude" in data.columns:
                self.XtimeValues = data["time"].to_numpy()
                self.YAmpValues = data["amplitude"].to_numpy()
            else:
                # Assume the first two columns represent time and amplitude
                self.XtimeValues = data.iloc[:, 0].to_numpy()
                self.YAmpValues = data.iloc[:, 1].to_numpy()

            # Set a default sample rate if not provided
            self.sample_rate = 1 / (self.XtimeValues[1] - self.XtimeValues[0])

            self.plotgraph(self.XtimeValues, self.YAmpValues)
            fft_result = self.cooley_tukey_fft(self.YAmpValues)
            self.plot_fft(fft_result)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load CSV file:\n{e}")

    def cooley_tukey_fft(self, signal):
        """
        Recursive implementation of the Cooley-Tukey FFT algorithm.
        Pads the signal with zeros if its length is not a power of 2.
        :param signal: Input signal array.
        :return: Frequency-domain representation.
        """
        n = len(signal)
        if n & (n - 1) != 0:  # Check if n is not a power of 2
            next_power_of_2 = 2 ** int(np.ceil(np.log2(n)))
            signal = np.pad(signal, (0, next_power_of_2 - n), mode='constant', constant_values=0)
            n = len(signal)

        if n <= 1:
            return signal

        even = self.cooley_tukey_fft(signal[::2])
        odd = self.cooley_tukey_fft(signal[1::2])

        T = [cmath.exp(-2j * cmath.pi * k / n) * odd[k] for k in range(n // 2)]
        return [even[k] + T[k] for k in range(n // 2)] + \
            [even[k] - T[k] for k in range(n // 2)]
    

    def get_max_frequency(self,fft_result, frequencies):
        """
        Finds the frequency corresponding to the maximum magnitude in the FFT result.
        :param fft_result: Array of FFT coefficients (complex numbers).
        :param frequencies: Array of frequency bins corresponding to the FFT result.
        :return: Maximum frequency value (Hz).
        """
        # Compute magnitudes of the FFT coefficients
        magnitudes = np.abs(fft_result)
        
        # Focus only on positive frequencies (usually the first half of the spectrum)
        n = len(frequencies)
        positive_frequencies = frequencies[:n // 2]
        positive_magnitudes = magnitudes[:n // 2]
        
        # Find the index of the maximum magnitude
        max_index = np.argmax(positive_magnitudes)
        
        # Get the frequency corresponding to the maximum magnitude
        max_frequency = positive_frequencies[max_index]
        print(f"Maximum Frequency: {max_frequency} Hz")
        return max_frequency

        

    

    def plotgraph(self, x, y):
        self.graph.clear()
        self.graph.plot(x, y, pen='b')
        self.graph.setTitle("Time-Domain Signal")
        self.graph.setLabel('left', 'Amplitude')
        self.graph.setLabel('bottom', 'Time (s)')

    def plot_fft(self, fft_result):
        n = len(fft_result)
        freq = np.fft.fftfreq(n, d=1/self.sample_rate)
        magnitude = np.abs(fft_result)

        half_n = n // 2
        self.Freqgraph.clear()
        self.Freqgraph.plot(freq[:half_n], magnitude[:half_n], pen='r')
        self.Freqgraph.setTitle("Frequency-Domain Signal")
        self.Freqgraph.setLabel('left', 'Magnitude')
        self.Freqgraph.setLabel('bottom', 'Frequency (Hz)')
        self.get_max_frequency(fft_result, freq)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
