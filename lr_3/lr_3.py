import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton, QComboBox,
                             QTabWidget, QTableView, QGridLayout, QVBoxLayout,
                             QFileDialog, QMessageBox)
from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery

CONNECTION_NAME = "lab3"

SQL_TAB1 = "SELECT * FROM sqlite_master"
SQL_BT1 = "SELECT name FROM sqlite_master"
SQL_TABLES = "SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%' ORDER BY rowid"


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Лабораторная 3")
        self.resize(700, 500)

        self.db = QSqlDatabase.addDatabase("QSQLITE", CONNECTION_NAME)
        self.tables = []

        menu = self.menuBar().addMenu("Menu")
        menu.addAction("Set connection", self.set_connection)
        menu.addAction("Close connection", self.close_connection)

        self.bt1 = QPushButton("SELECT Column")
        self.bt2 = QPushButton("Query2")
        self.bt3 = QPushButton("Query3")
        self.combo = QComboBox()
        self.bt1.clicked.connect(lambda: self.show_query(1, SQL_BT1))
        self.bt2.clicked.connect(lambda: self.show_table(3, 0))
        self.bt3.clicked.connect(lambda: self.show_table(4, 1))
        self.combo.activated.connect(self.on_combo)

        self.tabs = QTabWidget()
        self.models = []
        for i in range(1, 6):
            view = QTableView()
            model = QSqlQueryModel()
            view.setModel(model)
            self.tabs.addTab(view, f"Tab{i}")
            self.models.append(model)

        grid = QGridLayout()
        grid.addWidget(self.bt1, 0, 0)
        grid.addWidget(self.combo, 0, 1)
        grid.addWidget(self.bt2, 1, 0)
        grid.addWidget(self.bt3, 1, 1)

        layout = QVBoxLayout()
        layout.addLayout(grid)
        layout.addWidget(self.tabs)
        central = QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)

    def set_connection(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Выберите БД", "", "SQLite (*.db *.sqlite *.sqlite3);;Все файлы (*)")
        if not path:
            return
        self.close_connection()

        self.db.setDatabaseName(path)
        if not self.db.open():
            QMessageBox.warning(self, "Ошибка", self.db.lastError().text())
            return

        self.show_query(0, SQL_TAB1)
        if self.models[0].lastError().isValid():
            self.close_connection()
            return

        record = self.models[0].record()
        self.combo.addItems([record.fieldName(i) for i in range(record.count())])

        query = QSqlQuery(self.db)
        query.exec_(SQL_TABLES)
        while query.next():
            self.tables.append(query.value(0))

    def close_connection(self):
        for model in self.models:
            model.clear()
        self.combo.clear()
        self.tables = []
        if self.db.isOpen():
            self.db.close()

    def check_connection(self):
        if not self.db.isOpen():
            QMessageBox.information(self, "Нет соединения", "Сначала Menu -> Set connection")
            return False
        return True

    def show_query(self, tab, sql):
        if not self.check_connection():
            return
        model = self.models[tab]
        model.setQuery(sql, self.db)
        if model.lastError().isValid():
            QMessageBox.warning(self, "Ошибка запроса", model.lastError().text())
        else:
            self.tabs.setCurrentIndex(tab)

    def show_table(self, tab, n):
        if not self.check_connection():
            return
        if n >= len(self.tables):
            QMessageBox.information(self, "Нет таблицы", f"В базе нет таблицы №{n + 1}")
            return
        name = self.tables[n].replace('"', '""')
        self.show_query(tab, f'SELECT * FROM "{name}"')

    def on_combo(self):
        self.show_query(2, f"SELECT {self.combo.currentText()} FROM sqlite_master")

    def closeEvent(self, event):
        self.close_connection()
        super().closeEvent(event)


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec_())
