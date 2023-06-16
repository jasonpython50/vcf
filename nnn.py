import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox, QPushButton, QDialog, QVBoxLayout

def convert_csv_to_vcf(filename):
    try:
        df = pd.read_csv(filename)
    except pd.errors.ParserError:
        QMessageBox.critical(None, 'Error', 'Failed to parse CSV file.')
        return
    except FileNotFoundError:
        QMessageBox.critical(None, 'Error', 'File not found.')
        return

    if not {'first_name', 'last_name', 'mobile_phone'}.issubset(df.columns):
        QMessageBox.critical(None, 'Error', 'The CSV file should have "first_name", "last_name", and "mobile_phone" columns.')
        return

    try:
        with open(filename.rsplit('.', 1)[0] + '.vcf', 'w') as vcf_file:
            for _, row in df.iterrows():
                vcf_file.write(f"BEGIN:VCARD\n")
                vcf_file.write(f"VERSION:3.0\n")
                vcf_file.write(f"N:{row['last_name']};{row['first_name']}\n")
                vcf_file.write(f"FN:{row['first_name']} {row['last_name']}\n")
                vcf_file.write(f"TEL;TYPE=CELL:{row['mobile_phone']}\n")
                vcf_file.write(f"END:VCARD\n\n")
    except Exception as e:
        QMessageBox.critical(None, 'Error', f'Failed to write VCF file: {e}')
        return

    QMessageBox.information(None, 'Success', 'The CSV file was successfully converted to VCF.')
    show_dialog()

def choose_file():
    dialog = QFileDialog()
    dialog.setFileMode(QFileDialog.ExistingFile)
    dialog.setNameFilter("CSV (*.csv)")
    if dialog.exec_():
        filename = dialog.selectedFiles()[0]
        convert_csv_to_vcf(filename)

def show_dialog():
    dialog = QDialog()
    layout = QVBoxLayout()
    dialog.setLayout(layout)

    btn_convert = QPushButton('Convert CSV file')
    btn_convert.clicked.connect(choose_file)
    layout.addWidget(btn_convert)

    btn_exit = QPushButton('Exit')
    btn_exit.clicked.connect(dialog.close)
    layout.addWidget(btn_exit)

    dialog.exec_()

def main():
    app = QApplication(sys.argv)
    show_dialog()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

