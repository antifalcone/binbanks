from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QSize, Qt
import psycopg2
from config import host, user, password, db_name
import requests
from requests.exceptions import ConnectionError,JSONDecodeError
from PyQt6.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QHeaderView

URL = "https://lookup.binlist.net/"

def get_name(bank_bin):
    try:
        bank_name = 'No info'
        bank_country = 'No info'
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT bank_name,bank_country FROM binlist WHERE bank_bin = {bank_bin};
                """
            )
            connection.commit()
            list_bank_name_country = cursor.fetchone()
            if (list_bank_name_country) == None:
                list_bank_name_country = []
                list_bank_name_country.append('No info')
                list_bank_name_country.append('No info')
            print(list_bank_name_country)
            print("Success 1 ")
        return list_bank_name_country
    except Exception as _ex:
        print(_ex)
    finally:
        if connection:
            connection.close()
            print("Close connection")






def get_name_country(bank_bin):
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    with connection.cursor() as cursor:
        cursor.execute(
            f"""select bank_name,bank_country from binlist where bank_bin = {bank_bin}""")
        connection.commit()
        list_info = cursor.fetchone()
    return list_info


def check_bin(bank_bin):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        with connection.cursor() as cursor:
            cursor.execute(
                f"""select count(*) <> 0 from binlist where bank_bin = {bank_bin}""")
            connection.commit()
            check_our_bin = cursor.fetchone()
            print(check_our_bin)
            return check_our_bin[0]
    except Exception as _ex:
        print(_ex)
    finally:
        if connection:
            connection.close()
            print("Close connection")


def check_internet(bank_bin):
    try:
            list_info = []
            req = requests.get(URL + f"{bank_bin}")
            req = req.json()
            bank_name = 'No info'
            bank_country = 'No info'
            print(req)
            if ('bank' in req):
                print(req['bank'])
                if req['bank'] is not None:
                    if ('name' in req['bank']):
                        print(req)
                        bank_name = req['bank']['name']
            if ('country' in req):
                if req['country'] is not None:
                    if ('name' in req['country']):
                        bank_country = req['country']['name']
            list_info.append(bank_bin)
            list_info.append(bank_name)
            list_info.append(bank_country)
            return list_info
    except JSONDecodeError:
        list_info.append(bank_bin)
        list_info.append("No info")
        list_info.append("No info")
        return list_info
    except ConnectionError:
        print("Check your internet connection")
        list_info.append(bank_bin)
        list_info.append("No info")
        list_info.append("No info")
        return list_info

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        super().__init__()
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(QSize(1024, 668))
        MainWindow.setStyleSheet("*, *:before, *:after {\n"
"  box-sizing: border-box;\n"
"  margin: 0;\n"
"  padding: 0;\n"
"}\n"
"$openSans: \'Open Sans\', Helvetica, Arial, sans-serif;\n"
"body {\n"
"  background: #333;\n"
"  font-family: $openSans;\n"
"}\n"
"\n"
".buttons {\n"
"  margin-top: 50px;\n"
"  text-align: center;\n"
"  border-radius:30px;\n"
"}\n"
"\n"
"$cyan: #0505A9;\n"
"$dark: #FFFFFF;\n"
"$borderW: 2px;\n"
"\n"
".blob-btn {\n"
"  $numOfBlobs: 4;\n"
"  z-index: 1;\n"
"  position: relative;\n"
"  padding: 20px 46px;\n"
"  margin-bottom: 30px;\n"
"  text-align: center;\n"
"  text-transform: uppercase;\n"
"  color: $cyan;\n"
"  font-size: 16px;\n"
"  font-weight: bold;\n"
"  background-color: transparent;\n"
"  outline: none;\n"
"  border: none;\n"
"  transition: color 0.5s;\n"
"  cursor: pointer;\n"
"  border-radius:30px;\n"
"  \n"
"  &:before {\n"
"    content: \"\";\n"
"    z-index: 1;\n"
"    position: absolute;\n"
"    left: 0;\n"
"    top: 0;\n"
"    width: 100%;\n"
"    height: 100%;\n"
"    border: $borderW solid $cyan;\n"
"    border-radius:30px;\n"
"  }\n"
"  \n"
"  &:after {\n"
"    content: \"\";\n"
"    z-index: -2;\n"
"    position: absolute;\n"
"    left: $borderW*1.5;\n"
"    top: $borderW*1.5;\n"
"    width: 100%;\n"
"    height: 100%;\n"
"\n"
"    transition: all 0.3s 0.2s;\n"
"    border-radius:30px;\n"
"  }\n"
"  \n"
"  &:hover {\n"
"    color: $dark;\n"
"    border-radius:30px;\n"
"    \n"
"    &:after {\n"
"      transition: all 0.3s;\n"
"      left: 0;\n"
"      top: 0;\n"
"      border-radius:30px;\n"
"    }\n"
"  }\n"
"  \n"
"  &__inner {\n"
"    z-index: -1;\n"
"    overflow: hidden;\n"
"    position: absolute;\n"
"    left: 0;\n"
"    top: 0;\n"
"    width: 100%;\n"
"    height: 100%;\n"
"    border-radius:30px;\n"
"    background:#ffffff;\n"
"  }\n"
"  \n"
"  // additional container created, because in FF blobs are breaking overflow:hidden of element with svg gooey filter\n"
"  &__blobs {\n"
"    position: relative;\n"
"    display: block;\n"
"    height: 100%;\n"
"    filter: url(\'#goo\');\n"
"  }\n"
"  \n"
"  &__blob {\n"
"    position: absolute;\n"
"    top: $borderW;\n"
"    width: 100% / $numOfBlobs;\n"
"    height: 100%;\n"
"    background: $cyan;\n"
"    border-radius: 100%;\n"
"    transform: translate3d(0,150%,0) scale(1.7);\n"
"    transition: transform 0.45s;\n"
"    \n"
"    @supports(filter: url(\'#goo\')) {\n"
"      transform: translate3d(0,150%,0) scale(1.4);\n"
"    }\n"
"    \n"
"    @for $i from 1 through $numOfBlobs {\n"
"      &:nth-child(#{$i}) {\n"
"        left: ($i - 1) * (120% / $numOfBlobs);\n"
"        transition-delay: ($i - 1) * 0.08s;\n"
"      }\n"
"    }\n"
"    \n"
"    .blob-btn:hover & {\n"
"      transform: translateZ(0) scale(1.7);\n"
"      \n"
"      @supports(filter: url(\'#goo\')) {\n"
"        transform: translateZ(0) scale(1.4);\n"
"      }\n"
"    }\n"
"  }\n"
"  \n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)

        self.centralwidget.setStyleSheet("background-color: #22222e")
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 1024, 200))
        self.frame.setStyleSheet("background-color: #fb5b5d")
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(30, 40, 581, 90))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(610, 40, 90, 90))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("D:/Загрузки/kisspng-shoping-brugnato-5terre-embroidery-sewing-machines-credit-card-icon-5b20b1e136fed4.2785010715288693452253.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(160, 250, 200, 50))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Symbol")
        font.setPointSize(35)
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet("background-color: #22222e;\n"
"border: 2px solid #f66867;\n"
"border-radius: 30;\n"
"color: white\n"
"")
        self.lineEdit.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lineEdit.setObjectName("lineEdit")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(155, 200, 270, 51))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(160, 310, 186, 30))
        self.pushButton.setStyleSheet("background-color: red;\n"
"border-width: 2px;\n"
"border-radius: 10px;\n"
"border-color: beige;\n"
"font: bold 14px;\n"
"min-width: 10em;\n"
"padding: 6px;\n"
"")
        self.pushButton.setCheckable(False)
        self.pushButton.setAutoDefault(False)
        self.pushButton.setObjectName("pushButton")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(650, 210, 360, 50))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(20, 410, 600, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(20, 470, 600, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(20, 530, 600, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(660, 310, 324, 295))
        self.tableWidget.setStyleSheet("background-color: rgb(255, 116, 88);")
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(9)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.pushButton.clicked.connect(self.add_functions)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "BIN Checker"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:28pt; font-weight:600;\">Bank Identification Number</span></p></body></html>"))
        self.label_3.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#ffffff;\">Enter your BIN:</span></p></body></html>"))
        self.pushButton.setText(_translate("MainWindow", "Check"))
        self.label_4.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:26pt; color:#ffffff;\">Last 10 BIN-checking:</span></p><p><span style=\" font-size:26pt; color:#ffffff;\"/></p></body></html>"))
        self.label_5.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt; color:#ffffff;\">Bank name:</span></p></body></html>"))
        self.label_6.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt; color:#ffffff;\">Bank country:</span></p></body></html>"))
        self.label_7.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt; color:#ffffff;\">BIN:</span></p></body></html>"))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "1"))
        item = self.tableWidget.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "2"))
        item = self.tableWidget.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "3"))
        item = self.tableWidget.verticalHeaderItem(3)
        item.setText(_translate("MainWindow", "4"))
        item = self.tableWidget.verticalHeaderItem(4)
        item.setText(_translate("MainWindow", "5"))
        item = self.tableWidget.verticalHeaderItem(5)
        item.setText(_translate("MainWindow", "6"))
        item = self.tableWidget.verticalHeaderItem(6)
        item.setText(_translate("MainWindow", "7"))
        item = self.tableWidget.verticalHeaderItem(7)
        item.setText(_translate("MainWindow", "8"))
        item = self.tableWidget.verticalHeaderItem(8)
        item.setText(_translate("MainWindow", "10"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "BIN\'s"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Name"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Country"))


    def add_functions(self):
        global connection
        list_top_10 = list()
        list_bank_info = list()
        bank_bin = self.lineEdit.text()
        while type(bank_bin) != int:
            try:
                bank_bin = abs(int(bank_bin))
            except ValueError:
                bank_bin = self.lineEdit.text()
        self.lineEdit.clear()
        print(bank_bin)
        self.label_7.setText("BIN: " + f"{bank_bin}")
        self.label_7.setStyleSheet("color: white")
        check_flag = check_bin(bank_bin)
        if check_flag == True:
            try:
                connection = psycopg2.connect(
                    host=host,
                    user=user,
                    password=password,
                    database=db_name
                )
                with connection.cursor() as cursor:
                    cursor.execute(
                        f"""
                        SELECT bank_bin,bank_name,bank_country FROM binlist WHERE bank_bin = {bank_bin};
                        """
                    )
                    connection.commit()
                    list_bank_info = cursor.fetchone()
                    cursor.execute(f"""DO $$
                        BEGIN
                        FOR i IN REVERSE 10..1 LOOP
                            update top10 set top[i]=top[i-1];
                        END LOOP;
                        update top10 set top[1] = {bank_bin};
                        END$$;
                    """)
                    print(list_bank_info)
                    cursor.execute("""SELECT top[:10] FROM top10""")
                    connection.commit()
                    list_top_10 = cursor.fetchone()
                    print(list_top_10,bank_name)
                    print("Success 1 ")
            except Exception as _ex:
                print(_ex)
            finally:
                if connection:
                    connection.close()
                    print("Close connection")
        elif check_flag == False:
            list_bank_info = check_internet(bank_bin)
            print(list_bank_info)
            bank_name = list_bank_info[1]
            bank_country = list_bank_info[2]
            try:
                connection = psycopg2.connect(
                    host=host,
                    user=user,
                    password=password,
                    database=db_name
                )
                print(bank_name)
                with connection.cursor() as cursor:
                    cursor.execute(
                        f"""INSERT INTO binlist(bank_bin,bank_name, bank_country) VALUES
                        ({bank_bin},'{bank_name}','{bank_country}');
                            """
                    )
                    connection.commit()
                    cursor.execute(f"""DO $$
                        BEGIN
                        FOR i IN REVERSE 10..1 LOOP
                            update top10 set top[i]=top[i-1];
                        END LOOP;
                        update top10 set top[1] = {bank_bin};
                        END$$;""")
                    connection.commit()
                    cursor.execute(
                        f"""
                        SELECT bank_bin,bank_name,bank_country FROM binlist WHERE bank_bin = {bank_bin};
                        """
                    )
                    connection.commit()
                    list_bank_info = cursor.fetchone()
                    cursor.execute("""SELECT top[:10] FROM top10""")
                    connection.commit()
                    list_top_10 = cursor.fetchone()
                    print(list_top_10,bank_name)
                    print("Success 2")
            except Exception as _ex:
                print(_ex)
            finally:
                if connection:
                    connection.close()
                    print("Close connection")
        else:
            print("Error to connect DB")
        print(list_top_10, list_bank_info)
        bank_name = list_bank_info[1]
        bank_country = list_bank_info[2]

        self.label_5.setText("Bank name: " + f"{bank_name}")
        self.label_5.setStyleSheet("color: white")
        self.label_6.setText("Bank country: " + f"{bank_country}")
        self.label_6.setStyleSheet("color: white")
        print(list_top_10)
        for j in range(0,9):
            if type(bank_bin) == int:
                bank_bin = list_top_10[0][j]
                list_info = get_name_country(bank_bin)
                print(list_info)
                self.tableWidget.setItem(j, 0, QTableWidgetItem(f"{bank_bin}"))
                self.tableWidget.setItem(j, 1, QTableWidgetItem(f"{get_name(bank_bin)[0]}"))
                self.tableWidget.setItem(j, 2, QTableWidgetItem(f"{get_name(bank_bin)[1]}"))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
