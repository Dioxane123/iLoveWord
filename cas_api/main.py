from getpass import getpass
from getToken import token
from iLoveWord import answerPaper
if __name__ == '__main__':
    username = input('请输入您的学号：')
    password = getpass('请输入您的密码：')
    myToken = token(username, password)
    mode = input('请输入模式-自测(0)/考试(1)：')
    week = input('请输入第几周(数字)：')
    answerPaper(myToken, mode, week)
    