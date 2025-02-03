import sys
from PyQt5.QtWidgets import QApplication
from ui import PortScannerUI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PortScannerUI()
    window.show()
    sys.exit(app.exec_())