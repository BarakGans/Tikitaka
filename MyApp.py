import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem, QLabel, QFormLayout, QMessageBox, QComboBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class TokoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.items = {}
        self.purchase_history = []
        self.sale_history = []

    def initUI(self):
        # Layout utama
        mainLayout = QVBoxLayout()

        # Layout untuk logo
        logoLayout = QHBoxLayout()
        self.logoLabel = QLabel(self)
        self.logoPixmap = QPixmap("logo.png")  # Path ke gambar logo
        self.logoLabel.setPixmap(self.logoPixmap)
        logoLayout.addWidget(self.logoLabel)
        
        # Layout untuk input
        inputLayout = QFormLayout()
        self.itemNameInput = QLineEdit(self)
        self.itemNameInput.setPlaceholderText("Nama Barang")
        self.itemPriceInput = QLineEdit(self)
        self.itemPriceInput.setPlaceholderText("Harga Barang")
        self.addButton = QPushButton('Tambahkan Barang', self)
        self.addButton.clicked.connect(self.addItem)
        self.sellButton = QPushButton('Jual Barang', self)
        self.sellButton.clicked.connect(self.sellItem)
        self.deleteButton = QPushButton('Hapus Barang', self)
        self.deleteButton.clicked.connect(self.deleteItem)

        # ComboBox untuk metode pembayaran
        self.paymentMethodCombo = QComboBox(self)
        self.paymentMethodCombo.addItems(["Cash", "Kartu Kredit/Debit", "Online Payment"])

        inputLayout.addRow(QLabel("Nama Barang:"), self.itemNameInput)
        inputLayout.addRow(QLabel("Harga Barang:"), self.itemPriceInput)
        inputLayout.addWidget(self.addButton)
        inputLayout.addWidget(self.sellButton)
        inputLayout.addWidget(self.deleteButton)
        inputLayout.addRow(QLabel("Metode Pembayaran:"), self.paymentMethodCombo)

        # Layout untuk tabel utama (Barang Tersedia)
        self.itemTable = QTableWidget(self)
        self.itemTable.setRowCount(0)
        self.itemTable.setColumnCount(2)
        self.itemTable.setHorizontalHeaderLabels(["Nama Barang", "Harga"])
        self.itemTable.setSelectionMode(QTableWidget.SingleSelection)
        self.itemTable.setSelectionBehavior(QTableWidget.SelectRows)

        # Layout untuk tabel riwayat
        self.purchaseTable = QTableWidget(self)
        self.purchaseTable.setRowCount(0)
        self.purchaseTable.setColumnCount(2)
        self.purchaseTable.setHorizontalHeaderLabels(["Nama Barang", "Harga"])

        self.saleTable = QTableWidget(self)
        self.saleTable.setRowCount(0)
        self.saleTable.setColumnCount(3)
        self.saleTable.setHorizontalHeaderLabels(["Nama Barang", "Harga", "Metode Pembayaran"])

        # Layout utama
        mainLayout.addLayout(logoLayout)  # Tambahkan layout logo
        mainLayout.addLayout(inputLayout)
        mainLayout.addWidget(QLabel("Barang Tersedia:"))
        mainLayout.addWidget(self.itemTable)
        mainLayout.addWidget(QLabel("Riwayat Pembelian:"))
        mainLayout.addWidget(self.purchaseTable)
        mainLayout.addWidget(QLabel("Riwayat Penjualan:"))
        mainLayout.addWidget(self.saleTable)

        self.setLayout(mainLayout)
        self.setWindowTitle('Aplikasi Toko')
        self.setGeometry(100, 100, 800, 600)

    def addItem(self):
        item_name = self.itemNameInput.text()
        item_price = self.itemPriceInput.text()
        if item_name and item_price:
            self.items[item_name] = item_price
            self.updateItemTable()
            self.purchase_history.append((item_name, item_price))
            self.updatePurchaseTable()
            self.itemNameInput.clear()
            self.itemPriceInput.clear()

    def sellItem(self):
        item_name = self.itemNameInput.text()
        payment_method = self.paymentMethodCombo.currentText()
        if item_name in self.items:
            item_price = self.items[item_name]
            del self.items[item_name]
            self.updateItemTable()
            self.sale_history.append((item_name, item_price, payment_method))
            self.updateSaleTable()
            self.itemNameInput.clear()

    def deleteItem(self):
        selected_row = self.itemTable.currentRow()
        if selected_row >= 0:
            item_name = self.itemTable.item(selected_row, 0).text()
            if item_name in self.items:
                del self.items[item_name]
                self.updateItemTable()
                QMessageBox.information(self, 'Info', f'Barang "{item_name}" telah dihapus dari daftar.')
            else:
                QMessageBox.warning(self, 'Peringatan', 'Barang tidak ditemukan.')
        else:
            QMessageBox.warning(self, 'Peringatan', 'Silakan pilih baris untuk dihapus.')

    def updateItemTable(self):
        self.itemTable.setRowCount(0)
        for i, (name, price) in enumerate(self.items.items()):
            self.itemTable.insertRow(i)
            self.itemTable.setItem(i, 0, QTableWidgetItem(name))
            self.itemTable.setItem(i, 1, QTableWidgetItem(price))

    def updatePurchaseTable(self):
        self.purchaseTable.setRowCount(0)
        for i, (name, price) in enumerate(self.purchase_history):
            self.purchaseTable.insertRow(i)
            self.purchaseTable.setItem(i, 0, QTableWidgetItem(name))
            self.purchaseTable.setItem(i, 1, QTableWidgetItem(price))

    def updateSaleTable(self):
        self.saleTable.setRowCount(0)
        for i, (name, price, payment_method) in enumerate(self.sale_history):
            self.saleTable.insertRow(i)
            self.saleTable.setItem(i, 0, QTableWidgetItem(name))
            self.saleTable.setItem(i, 1, QTableWidgetItem(price))
            self.saleTable.setItem(i, 2, QTableWidgetItem(payment_method))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    toko = TokoApp()
    toko.show()
    sys.exit(app.exec_())
