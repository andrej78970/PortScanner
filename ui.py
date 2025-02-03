from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QProgressBar
from PyQt5.QtCore import QThread
from scanner import PortScannerWorker
from config import config

class PortScannerUI(QWidget):
    def __init__(self):
        super().__init__()
        self.thread = None  
        self.worker = None  
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Port Scan")
        self.setGeometry(100, 100, 400, 350)

        layout = QVBoxLayout()

        self.label_target = QLabel("Target IP/Domain:")
        self.input_target = QLineEdit(config["default_target"])
        layout.addWidget(self.label_target)
        layout.addWidget(self.input_target)

        self.label_ports = QLabel("Port Range:")
        self.input_ports = QLineEdit(config["default_ports"])
        layout.addWidget(self.label_ports)
        layout.addWidget(self.input_ports)

        self.scan_button = QPushButton("Start Scan")
        self.scan_button.clicked.connect(self.start_scan)
        layout.addWidget(self.scan_button)

        self.stop_button = QPushButton("Stop Scan")
        self.stop_button.clicked.connect(self.stop_scan)
        self.stop_button.setEnabled(False) 
        layout.addWidget(self.stop_button)

        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        layout.addWidget(self.result_area)

        self.setLayout(layout)

    def start_scan(self):
        """Starts the port scan in a new thread"""
        target = self.input_target.text()
        port_range = self.input_ports.text()

        try:
            start_port, end_port = map(int, port_range.split('-'))
        except ValueError:
            self.result_area.setText("Error: Wrong port range format (e.g. 1-1000)")
            return

        self.result_area.clear()
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)

        self.thread = QThread()
        self.worker = PortScannerWorker(target, start_port, end_port)
        self.worker.moveToThread(self.thread)


        self.worker.progress.connect(self.update_progress)
        self.worker.result.connect(self.update_result)
        self.worker.finished.connect(self.scan_finished)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)


        self.thread.started.connect(self.worker.scan_ports)
        self.thread.start()

        self.scan_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def stop_scan(self):
        """Stops the port scan"""
        if self.worker:
            self.worker.stop_requested = True
            self.result_area.append("Scan is stopping")
        
    def update_progress(self, value):
        """Updates the progress"""
        self.progress_bar.setValue(value)

    def update_result(self, message):
        """Prints the scan result"""
        self.result_area.append(message)

    def scan_finished(self):
        """Gets called when the scan is finished"""
        self.scan_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.result_area.append("Scan finished")