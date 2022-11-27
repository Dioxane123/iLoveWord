import requests
import uuid
import json
import time
import pprint
from ydtrans import translate


# def translate(word):
#     url = 'https://fanyi.baidu.com/sug'
#     data = {'kw': word}
#     return str(json.loads(requests.post(url, data=data).text))


def getData(x_token, mode, week):
    # 获取当前时间戳
    timestamp = int(time.time() * 10000)
    getUrl = f'https://skl.hdu.edu.cn/api/paper/new?type={mode}&week={week}&startTime=' + str(timestamp)
    getHeaders = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Host': 'skl.hdu.edu.cn',
        'Origin': 'https://skl.hduhelp.com',
        'Pragma': 'no-cache',
        'Referer': 'https://skl.hduhelp.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'cross-site',
        # 获取当前uuid（测试发现是uuid1）
        'skl-ticket': str(uuid.uuid1()),
        'User-Agent': 'Mozilla/5.0 (Linux; Android 12; 22081212C Build/SKQ1.220303.001) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/95.0.4638.74 Mobile Safari/537.36',
        # 自己的token
        'X-Auth-Token': x_token
    }
    response = requests.get(getUrl, headers=getHeaders)
    return json.loads(response.text)


def postData(answer, x_token):
    url = 'https://skl.hdu.edu.cn/api/paper/save'

    postHeaders = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Host': 'skl.hdu.edu.cn',
        'Origin': 'https://skl.hduhelp.com',
        'Referer': 'https://skl.hduhelp.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'skl-ticket': str(uuid.uuid1()),
        'User-Agent': 'Mozilla/5.0 (Linux; Android 12; 22081212C Build/SKQ1.220303.001) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/95.0.4638.74 Mobile Safari/537.36',
        'X-Auth-Token': x_token
    }  # 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0'
    requests.post(url, headers=postHeaders, data=answer)


def fail(tit, a, b, c, d, ans):
    print("程序无法识别此题，请手动选择")
    print("题目：" + tit)
    print('A:' + a[:-3])
    print('B:' + b[:-3])
    print('C:' + c[:-3])
    print('D:' + d[:-3])
    print("参考答案：" + ans)
    return input("请输入答案(A/B/C/D):")


def getAnswer(word, man):
    optionList = ['A', 'B', 'C', 'D']
    if '，' in word['title']:  # 处理中文中的  （，）
        zhList = word['title'][:-3].split('，')
        for num in range(0, len(zhList)):
            transResult = ' '.join(translate(zhList[num]))
            for option in optionList:  # 翻译题目匹配选项
                if word[f'answer{option}'][:-3] in transResult:
                    print(f"题目匹配 ans:{option}")
                    return option
            for option in optionList:  # 翻译选项匹配题目
                print(f"{option}:", end='')
                transResult = ' '.join(translate(word[f'answer{option}'][:-3]))
                if zhList[num] in transResult:
                    print(f"选项匹配 ans:{option}")
                    return option
        if man:  # 手动调整
            transResult = ' '.join(translate(zhList[0]))
            return fail(word['title'][:-3], word['answerA'], word['answerB'],
                        word['answerC'], word['answerD'], transResult)
        else:
            print("fuck up")
            return 'C'
    elif '(' in word['title']:  # 处理中文中的()
        zhList = word['title'][:-3].split('(')
        if bool(zhList):
            transResult = ' '.join(translate(zhList[0]))
            for option in optionList:  # 翻译题目匹配选项
                if word[f'answer{option}'][:-3] in transResult:
                    print(f"题目匹配 ans:{option}")
                    return option
            for option in optionList:  # 翻译选项匹配题目
                print(f"{option}:", end='')
                transResult = ' '.join(translate(word[f'answer{option}'][:-3]))
                if zhList[0] in transResult:
                    print(f"选项匹配 ans:{option}")
                    return option
            zhList = word['title'][:-3].split(')')
        transResult = ' '.join(translate(zhList[1]))
        for option in optionList:  # 翻译题目匹配选项
            if word[f'answer{option}'][:-3] in transResult:
                print(f"题目匹配 ans:{option}")
                return option
        for option in optionList:  # 翻译选项匹配题目
            print(f"{option}:", end='')
            transResult = ' '.join(translate(word[f'answer{option}'][:-3]))
            if zhList[1] in transResult:
                print(f"选项匹配 ans:{option}")
                return option
        if man:  # 手动调整
            transResult = ' '.join(translate(word['title'][:-3]))
            return fail(word['title'][:-3], word['answerA'], word['answerB'],
                        word['answerC'], word['answerD'], transResult)
        else:
            print("fuck up")
            return 'C'
    else:  # TODO:处理省略号
        transResult = ' '.join(translate(word['title'][:-3]))
        for option in optionList:  # 翻译题目匹配选项
            if word[f'answer{option}'][:-3] in transResult:
                print(f"题目匹配 ans:{option}")
                return option
        for option in optionList:  # 翻译选项匹配题目
            print(f"{option}:", end='')
            transResult = ' '.join(translate(word[f'answer{option}'][:-3]))
            if word['title'][:-3] in transResult:
                print(f"选项匹配 ans:{option}")
                return option
        if man:  # 手动调整
            transResult = ' '.join(translate(word['title'][:-3]))
            return fail(word['title'][:-3], word['answerA'], word['answerB'],
                        word['answerC'], word['answerD'], transResult)
        else:
            print("fuck up")
            return 'C'


def answerPaper(X_Auth_Token, mode, week):
    with open('answerList', 'r') as f:
        answerSource = f.read()
    answerDic = json.loads(answerSource)
    paper = getData(X_Auth_Token, mode, week)  # mode=0为自测,1为考试。week参数为第几周。
    print("极速模式：全自动，准确率较低(约为80%)")
    print("精确模式：程序不确定时会询问你的意见，准确率较高")
    manu = bool(int(input("请输入模式-极速模式(0)/精确模式(1):")))
    pprint.pprint(paper)
    answerDic['paperId'] = paper['paperId']
    print('********正在答题中********')
    for index in range(0, 100):
        print(f"{index+1}. ")
        answerDic['list'][index]['input'] = getAnswer(paper['list'][index], manu)
        answerDic['list'][index]['paperDetailId'] = paper['list'][index]['paperDetailId']
    print("程序已完成，建议等待一段时间后再提交答卷")
    answerTime = input("你希望在几分钟后提交答卷？(数字)")
    time.sleep(int(answerTime) * 60)  # 测试时可关闭,正式使用时请打开
    postData(json.dumps(answerDic), X_Auth_Token)
    print('答题已结束，任意键退出')
    input()
