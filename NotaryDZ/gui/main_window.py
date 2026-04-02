import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, 
                             QTableWidget, QTableWidgetItem, QComboBox, QFormLayout, 
                             QMessageBox, QFileDialog)
from PyQt6.QtCore import Qt
from database.models import Session, Client, Acte, init_db
from ai.assistant import NotaryAIAssistant

class NotaryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("نظام تسيير مكتب التوثيق - الجزائر (AI Notary DZ)")
        self.setGeometry(100, 100, 1000, 700)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft) # Arabic support
        
        self.ai_assistant = NotaryAIAssistant()
        self.session = Session()
        
        self.init_ui()
        
    def init_ui(self):
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        # Add Tabs
        self.tabs.addTab(self.create_dashboard_tab(), "لوحة التحكم")
        self.tabs.addTab(self.create_clients_tab(), "إدارة العملاء")
        self.tabs.addTab(self.create_actes_tab(), "إدارة العقود")
        self.tabs.addTab(self.create_ai_tab(), "مساعد الذكاء الاصطناعي")
        
    def create_dashboard_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        
        label = QLabel("مرحباً بك في نظام تسيير مكتب التوثيق")
        label.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        stats_layout = QHBoxLayout()
        
        # Simple stats
        client_count = self.session.query(Client).count()
        acte_count = self.session.query(Acte).count()
        
        stats_layout.addWidget(self.create_stat_card("عدد العملاء", str(client_count)))
        stats_layout.addWidget(self.create_stat_card("عدد العقود", str(acte_count)))
        
        layout.addWidget(label)
        layout.addLayout(stats_layout)
        layout.addStretch()
        
        tab.setLayout(layout)
        return tab

    def create_stat_card(self, title, value):
        card = QWidget()
        card.setStyleSheet("background-color: #ecf0f1; border-radius: 10px; padding: 20px;")
        layout = QVBoxLayout()
        
        t_label = QLabel(title)
        t_label.setStyleSheet("font-size: 16px; color: #7f8c8d;")
        v_label = QLabel(value)
        v_label.setStyleSheet("font-size: 32px; font-weight: bold; color: #2980b9;")
        
        layout.addWidget(t_label)
        layout.addWidget(v_label)
        card.setLayout(layout)
        return card

    def create_clients_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Form to add client
        form_layout = QFormLayout()
        self.client_name = QLineEdit()
        self.client_nif = QLineEdit()
        self.client_type = QComboBox()
        self.client_type.addItems(["شخص طبيعي (PH)", "شخص معنوي (PM)"])
        
        form_layout.addRow("الاسم واللقب / التسمية:", self.client_name)
        form_layout.addRow("رقم التعريف الجبائي (NIF):", self.client_nif)
        form_layout.addRow("نوع الشخص:", self.client_type)
        
        add_btn = QPushButton("إضافة عميل")
        add_btn.clicked.connect(self.add_client)
        
        # Table to list clients
        self.client_table = QTableWidget()
        self.client_table.setColumnCount(4)
        self.client_table.setHorizontalHeaderLabels(["ID", "الاسم", "NIF", "النوع"])
        self.refresh_clients()
        
        layout.addLayout(form_layout)
        layout.addWidget(add_btn)
        layout.addWidget(self.client_table)
        
        tab.setLayout(layout)
        return tab

    def add_client(self):
        name = self.client_name.text()
        nif = self.client_nif.text()
        ctype = "PH" if "PH" in self.client_type.currentText() else "PM"
        
        if not name or not nif:
            QMessageBox.warning(self, "خطأ", "يرجى ملء جميع الحقول الإجبارية")
            return
            
        new_client = Client(nom=name, num_nif=nif, type_personne=ctype)
        self.session.add(new_client)
        self.session.commit()
        self.refresh_clients()
        self.client_name.clear()
        self.client_nif.clear()

    def refresh_clients(self):
        clients = self.session.query(Client).all()
        self.client_table.setRowCount(len(clients))
        for i, client in enumerate(clients):
            self.client_table.setItem(i, 0, QTableWidgetItem(str(client.id)))
            self.client_table.setItem(i, 1, QTableWidgetItem(client.nom))
            self.client_table.setItem(i, 2, QTableWidgetItem(client.num_nif))
            self.client_table.setItem(i, 3, QTableWidgetItem(client.type_personne))

    def create_actes_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("إدارة العقود والوثائق الموثقة"))
        
        self.acte_table = QTableWidget()
        self.acte_table.setColumnCount(4)
        self.acte_table.setHorizontalHeaderLabels(["ID", "نوع العقد", "رقم القيد", "التاريخ"])
        self.refresh_actes()
        
        layout.addWidget(self.acte_table)
        tab.setLayout(layout)
        return tab

    def refresh_actes(self):
        actes = self.session.query(Acte).all()
        self.acte_table.setRowCount(len(actes))
        for i, acte in enumerate(actes):
            self.acte_table.setItem(i, 0, QTableWidgetItem(str(acte.id)))
            self.acte_table.setItem(i, 1, QTableWidgetItem(acte.type_acte))
            self.acte_table.setItem(i, 2, QTableWidgetItem(acte.numero_repertoire))
            self.acte_table.setItem(i, 3, QTableWidgetItem(str(acte.date_acte)))

    def create_ai_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("صياغة العقود بالذكاء الاصطناعي"))
        
        self.ai_acte_type = QComboBox()
        self.ai_acte_type.addItems(["VENTE (بيع)", "DON (هبة)", "SOCIETE (تأسيس شركة)", "PROCURATION (وكالة)"])
        
        self.ai_input_data = QTextEdit()
        self.ai_input_data.setPlaceholderText("أدخل بيانات الأطراف والعقار هنا (مثال: البائع أحمد، المشتري محمد، عقار في العاصمة، الثمن 500 مليون سنتيم)")
        
        gen_btn = QPushButton("توليد العقد")
        gen_btn.clicked.connect(self.generate_ai_contract)
        
        self.ai_output = QTextEdit()
        self.ai_output.setReadOnly(True)
        
        layout.addWidget(QLabel("نوع العقد:"))
        layout.addWidget(self.ai_acte_type)
        layout.addWidget(QLabel("البيانات:"))
        layout.addWidget(self.ai_input_data)
        layout.addWidget(gen_btn)
        layout.addWidget(QLabel("العقد المولد:"))
        layout.addWidget(self.ai_output)
        
        tab.setLayout(layout)
        return tab

    def generate_ai_contract(self):
        acte_type = self.ai_acte_type.currentText()
        input_data = self.ai_input_data.toPlainText()
        
        if not input_data:
            QMessageBox.warning(self, "خطأ", "يرجى إدخال البيانات")
            return
            
        self.ai_output.setText("جاري معالجة البيانات وصياغة العقد محلياً...")
        QApplication.processEvents()
        
        # Data for the local engine
        client_data = {"info": input_data}
        bien_data = {"info": input_data}
        
        # Enhanced AML Check for the local engine
        # Look for numbers in the text to estimate amount
        import re
        amounts = re.findall(r'\d+', input_data.replace(',', ''))
        max_amount = max([int(a) for a in amounts]) if amounts else 0
        
        if max_amount >= 500000 or "50 مليون" in input_data:
            compliance = self.ai_assistant.compliance_check("Unknown", max_amount if max_amount else 600000)
            if compliance['alerts']:
                QMessageBox.warning(self, "تنبيه غسل الأموال (AML)", "\n".join(compliance['alerts']))

        # Generate using the local smart engine (No API Key needed)
        result = self.ai_assistant.generate_contract(acte_type, client_data, bien_data)
        self.ai_output.setText(result)

if __name__ == "__main__":
    init_db()
    app = QApplication(sys.argv)
    window = NotaryApp()
    window.show()
    sys.exit(app.exec())
