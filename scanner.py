import socket
from PyQt5.QtCore import QObject, pyqtSignal
from config import config

class PortScannerWorker(QObject):
    """Work class for the port scan"""

    progress = pyqtSignal(int)  
    result = pyqtSignal(str)    
    finished = pyqtSignal()     

    def __init__(self, target, start_port, end_port):
        super().__init__()
        self.target = target
        self.start_port = start_port
        self.end_port = end_port
        self.stop_requested = False 

    def scan_ports(self):
        """scans the ports in the input range"""
        total_ports = self.end_port - self.start_port + 1

        for i, port in enumerate(range(self.start_port, self.end_port + 1)):
            if self.stop_requested:
                self.result.emit("Scan stopped")
                self.finished.emit()
                return  

            if self.is_port_open(self.target, port):
                self.result.emit(f"Open port found: {port}")

            progress_value = int((i / total_ports) * 100)
            self.progress.emit(progress_value)

        self.result.emit("Scan finished")
        self.finished.emit()

    def is_port_open(self, target, port):
        """checks if the port is open"""
        try:
            with socket.create_connection((target, port), timeout=config["timeout"]):
                return True
        except (socket.timeout, ConnectionRefusedError):
            return False