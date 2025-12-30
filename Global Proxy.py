import winreg
import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt


import requests
from packaging import version  # 需要安装: pip install packaging

CURRENT_VERSION = "1.0.0"

def check_for_update():
    try:
        resp = requests.get("https://yourdomain.com/app/version.txt", timeout=5)
        latest = resp.text.strip()
        if version.parse(latest) > version.parse(CURRENT_VERSION):
            return latest
    except Exception:
        pass
    return None

def get_proxy_settings():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Internet Settings")
    proxy_enable, _ = winreg.QueryValueEx(key, "ProxyEnable")
    if proxy_enable == 1:  # 只有当启用代理时才读取代理服务器设置
        proxy_server, _ = winreg.QueryValueEx(key, "ProxyServer")
        winreg.CloseKey(key)
        return proxy_server
    else:
        winreg.CloseKey(key)
        return None


proxy_settings = get_proxy_settings()




# 模拟 get 算法
def get():
    proxy_settings = get_proxy_settings()
    print("Proxy Settings:", proxy_settings)

    # 设置HTTP代理
    os.environ['HTTP_PROXY'] = proxy_settings

    # 设置HTTPS代理，如果需要的话
    os.environ['HTTPS_PROXY'] = proxy_settings

# 模拟 del 算法
def del_algorithm():
    # 删除HTTP代理
    if 'HTTP_PROXY' in os.environ:
        del os.environ['HTTP_PROXY']

    # 删除HTTPS代理
    if 'HTTPS_PROXY' in os.environ:
        del os.environ['HTTPS_PROXY']

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("后台程序")
#         self.setFixedSize(300, 100)
#         self.setWindowFlags(Qt.WindowCloseButtonHint)  # 只保留关闭按钮
#         self.statusBar().showMessage("程序已在后台运行，关闭窗口将退出全局")
#
#         # 启动时执行 get 算法
#         get()
#
#     def closeEvent(self, event):
#         # 用户尝试关闭窗口时触发
#         del_algorithm()
#         event.accept()  # 接受关闭事件，退出程序
#
# if __name__ == "__main__":
#     if proxy_settings != None:
#         app = QApplication(sys.argv)
#         window = MainWindow()
#         window.show()
#         sys.exit(app.exec_())



import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QSystemTrayIcon, QMenu, QAction,
    QLabel, QWidget, QVBoxLayout, QMessageBox
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt



class MainWindow(QMainWindow):
    from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("后台程序")
        self.setFixedSize(300, 120)
        # # 初始化托盘
        # self.tray_icon = QSystemTrayIcon(self)
        # if self.tray_icon.isSystemTrayAvailable():
        #     self.setup_tray()
        #     Text1 = "代理已开启" + proxy_settings
        #     Text2 = proxy_settings
        #     self.hint_label1.setText(Text1)  # 托盘可用
        #     self.hint_label2.setText(Text2)  # 托盘可用
        # else:
        #     self.hint_label.setText("BBBB")  # 托盘不可用

        # from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout
        # from PyQt5.QtCore import Qt

        # 在 MainWindow.__init__ 中替换中央 widget 部分：
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)  # 整体居中

        Text1 = "初始化完成"
        Text2 = proxy_settings

        # 第一个标签（上）
        self.label1 = QLabel(Text1)
        self.label1.setAlignment(Qt.AlignCenter)
        self.label1.setWordWrap(True)

        # 第二个标签（下）
        self.label2 = QLabel(Text2)
        self.label2.setAlignment(Qt.AlignCenter)
        self.label2.setWordWrap(True)

        # 添加到布局
        layout.addWidget(self.label1)
        layout.addWidget(self.label2)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)



        get()  # 启动时执行 get 算法

    def setup_tray(self):
        """设置系统托盘图标和菜单"""
        # 可选：设置一个图标（这里用默认应用图标，你也可以加载自定义图标）
        # self.tray_icon.setIcon(QIcon("icon.png"))

        tray_menu = QMenu()
        restore_action = QAction("显示", self)
        quit_action = QAction("退出", self)

        restore_action.triggered.connect(self.show_window)
        quit_action.triggered.connect(self.quit_app)

        tray_menu.addAction(restore_action)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.tray_icon_activated)
        self.tray_icon.show()
        # # 在 setup_tray() 中添加：
        # self.tray_icon.setIcon(QIcon.fromTheme("application-x-executable"))  # Linux
        # 或使用默认应用图标（Windows/macOS 通常有）
        if self.tray_icon.icon().isNull():
            self.tray_icon.setIcon(QApplication.style().standardIcon(QApplication.style().SP_ComputerIcon))

    def show_window(self):
        """从托盘恢复窗口"""
        self.showNormal()
        self.activateWindow()

    def quit_app(self):
        """通过托盘退出"""
        del_algorithm()
        QApplication.quit()

    def closeEvent(self, event):
        """用户点击 X 关闭按钮时触发"""
        # 如果托盘可用，我们改为隐藏而不是退出
        if self.tray_icon and self.tray_icon.isVisible():
            event.ignore()  # 忽略关闭事件
            self.hide()     # 隐藏窗口
            self.tray_icon.showMessage(
                "后台运行中",
                "程序已在系统托盘中运行，右键托盘图标可退出。",
                QSystemTrayIcon.Information,
                2000
            )
        else:
            # 托盘不可用，则直接退出
            del_algorithm()
            event.accept()

    def changeEvent(self, event):
        """监听窗口状态变化（如最小化）"""
        if event.type() == event.WindowStateChange:
            if self.isMinimized() and self.tray_icon and self.tray_icon.isVisible():
                self.hide()  # 最小化时隐藏窗口
                self.tray_icon.showMessage(
                    "已最小化到托盘",
                    "程序正在后台运行。",
                    QSystemTrayIcon.Information,
                    1000
                )
        super().changeEvent(event)

    def tray_icon_activated(self, reason):
        """托盘图标被激活（例如左键单击）"""
        if reason == QSystemTrayIcon.Trigger:  # 左键单击
            self.show_window()

if __name__ == "__main__":
    new_ver = check_for_update()
    if new_ver:
        reply = QMessageBox.information(
            None, "更新提示",
            f"发现新版本 {new_ver}！是否前往下载？",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            QDesktopServices.openUrl(QUrl("https://.../download"))
    if proxy_settings != None:
        app = QApplication(sys.argv)
        app.setQuitOnLastWindowClosed(False)  # 关闭所有窗口后不自动退出（因为有托盘）

        window = MainWindow()
        window.show()

        sys.exit(app.exec_())








