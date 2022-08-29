import dateutil.rrule
from PyQt5 import uic
from PyQt5.Qt import *
import sys
import os, subprocess, platform
import network

plat = platform.system().lower()
bug=""

codeing = {"linux": "utf-8", "windows": "gbk"}
cmd = {"linux": "touch", "windows": "echo #coding:utf-8 >"}
app = QApplication(sys.argv)
with open("datas", "r") as data:
    last_dir = data.readline()[:-1]
    python_path = data.readline()[:-1]
    user_name=data.readline()[:-1]
    password = data.readline()[:-1]


def save_data(last_dir):
    with open("datas", "w") as data:
        data.write(last_dir + "\n")
        data.write(python_path + "\n")
        data.write(user_name + "\n")
        data.write(password +"\n")

class Ui(QWidget):
    def __init__(self):
        super().__init__()
        self.st = 0
        uic.loadUi('main.ui', self)
        self.open.clicked.connect(self.open_file)
        self.run.clicked.connect(self.run_file)
        self.add.clicked.connect(self.add_file)
        self.commit.clicked.connect(self.commit_solution)
        self.loginbut.clicked.connect(self.login)
        m = QFontMetrics(self.code.font())
        self.code.setTabStopWidth(4 * m.width(" "))
        self.havebug=False
    def message(self,mess):
        msgBox = QMessageBox()
        msgBox.setText(mess)
        msgBox.exec_()

    def open_file(self):
        global last_dir
        self.directory = QFileDialog.getOpenFileName(
            self, "选取文件", last_dir, "*.py *.pyw")
        self.directory = self.directory[0]
        if self.directory=="":
            self.load_error()
        else:
            self.load_file()
            with open(self.directory, "r+", encoding=" utf-8 ") as codes:
                self.code.setText(codes.read())
            self.new_file()
    def run_file(self):
        global bug
        with open(self.directory, "w") as codes:
            codes.write(self.code.toPlainText())
        if plat == "windows":
            result = os.system("python "+self.directory)
            if result==1:
                with subprocess.Popen("python "+self.directory, stderr=subprocess.PIPE) as result:
                    n = []
                    r = result.communicate()[1]
                    for i in range(r.__len__()):
                        if chr(r[i]) == "\n":
                            n.append(i)
                    if self.havebug==False:
                        bug=str(r[n[len(n) - 2] + 1:n[len(n) - 1] - 1])[2:-1]
                    self.havebug=True
                    self.message("检测到你有一个bug，可以通过search查找解决方案")
                    os.system("cmd/k echo "+bug)
            else:
                if self.havebug==True:
                    self.commit.setEnabled(True)
                    self.message("恭喜你成功解决了问题！如果愿意，可以在commit中上传")
        else:
            os.system("konsole --noclose -e " + python_path + " " + self.directory)

    def add_file(self):
        global FILE, last_dir, t
        self.directory = QFileDialog.getExistingDirectory(self, "选择文件夹", last_dir)
        if self.directory == '':
            self.load_error()

        else:
            last_dir = self.directory
            title, okPressed = QInputDialog.getText(self, "file name", "file name:", QLineEdit.Normal, "")
            title = str(title)
            if title[-3:] != ".py" or title[-4:] != ".pyw":
                title += ".py"
            if okPressed == True:
                self.directory += ("/" + title)
                os.system(cmd[plat] + " " + self.directory)
                self.load_file()
            else:
                self.load_error()
            with open(self.directory, "r+") as codes:
                self.code.setText(codes.read())
            self.new_file()
    def new_file(self):
        self.code.setEnabled(True)
        self.run.setEnabled(True)
        self.commit.setEnabled(False)
        self.havebug=False
    def load_error(self):
        self.message("请选择正确的文件")
        self.code.setText("")
        self.code.setEnabled(False)
        self.run.setEnabled(False)
        self.commit.setEnabled(False)
        self.havebug=False

    def load_file(self):
        if self.directory == '':
            self.load_error()
        else:
            global last_dir
            self.st = 0
            for i in range(0, len(self.directory)):
                if self.directory[i] == '/':
                    self.st = i
            last_dir = self.directory[:self.st]
            save_data(last_dir)
            self.file_name.setText(str(self.directory[self.st + 1:]))
    def commit_solution(self):
        global bug
        if user_name=="":
            self.message("还未登录或注册，请登录或注册")
        else:
            send.error.setText(bug)
            send.show()

    def login(self):

        self.hide()
        login_win.show()


class Login(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("login.ui", self)
        self.joinbut.clicked.connect(self.join)
        self.enter.clicked.connect(self.try_login)
    def try_login(self):
        global user_name,password
        re=network.login(self.username.text(),self.password.text())
        if re["message"]=="error":
            if re["error"]=="password is not right":
                self.message("密码错误请重试")
            if re["error"]=="don't have the user name":
                self.message("没有这个用户名，请问你是否注册了")
        else:
            self.message("登录成功")
            user_name = self.username.text()
            password = self.password.text()
            save_data(last_dir)
            self.hide()
            ui.show()
    def message(self,mess):
        msgBox = QMessageBox()
        msgBox.setText(mess)
        msgBox.exec_()

    def join(self):
        self.hide()
        join_win.show()

class Join(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("join.ui",self)
        self.enter.clicked.connect(self.try_join)
    def try_join(self):
        global user_name,password
        re=network.join(self.username.text(), self.password.text())
        if re["message"]=="error":
            if re["error"]=="same name":
                self.message("名字已经被用过了，换一个吧！")
            if re["error"]=="the password is too long or to short":
                self.message("密码需要是由6位的字母和数字组成！")
        else:
            self.message("注册成功")
            user_name=self.username.text()
            password=self.password.text()
            save_data(last_dir)
            self.hide()
            ui.show()

    def message(self,mess):
        msgBox = QMessageBox()
        msgBox.setText(mess)
        msgBox.exec_()


class Send(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("send.ui",self)
        self.handup.clicked.connect(self.send)
    def send(self):
        global user_name,bug
        if (self.reason.toPlainText()!=""and self.body.toPlainText()!=""):
            network.add_article(user_name,bug,self.reason.toPlainText(),self.body.toPlainText())
        else:
            self.message("输入不能为空")
    def message(self, mess):
        msgBox = QMessageBox()
        msgBox.setText(mess)
        msgBox.exec_()


send=Send()
join_win=Join()
login_win=Login()
ui = Ui()
ui.show()

sys.exit(app.exec_())
