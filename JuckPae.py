CommentDict={
    '기사단장':[],
    '버서커':[],
    '아크메이지':[],
    '배틀메이지':[],
    '스나이퍼':[],
    '트랩퍼':[],
    '클레릭':[],
    '프리스트':[],
    '레인저':[],
    '런처':[],
    '닌자':[],
    '어쌔신':[],
    '발로그':[],
    '디아블로':[],
    '메카니즘마스터':[],
    '폭발물제조사':[],
    '소울브레이커':[],
    '대지도자':[],
    '버프빌더':[],
    '모스트빌더':[],
    '네크로맨서':[],
    '신앙자':[],
    '검신':[],
    '자객':[],
    '크루세이더':[],
    '샤이닝엠페러스':[],
    '갓핸드':[],
    '파일럿':[],
    '광기의살육자':[],
    '의문의사나이':[],
}
class Comment():
    def __init__(self, author, content):
        self.author = author
        self.content = content

def getCharNames():
    res = ''
    for charname in list(CommentDict.keys()):
        res += charname+'\n'
    return res
def isCharacter(name):
    return name in CommentDict

def addComment(name,comment):
    CommentDict[name].append(comment)
    print('추가됨')
    saveComment(name)

def getComments(name):
    res = ''
    for comment in CommentDict[name]:
        res += f'[{comment.author}] : {comment.content}\n'
    return res

def saveComment(name):
    with open('TeampleRPG Data\\'+name+'.dat','wt',encoding="utf-8") as f:
        for comment in CommentDict[name]:
            f.writelines(comment.author + '\n')
            f.writelines(comment.content + '\n')

def loadAllComment():
    for key in list(CommentDict.keys()):
        loadComment(key)

def loadComment(name):
    try:
        with open('TeampleRPG Data\\'+name+'.dat','rt',encoding="utf-8") as f:
            data = f.readlines()
            print(data,data.__len__())
            i = 0
            while  i < data.__len__():
                addComment(name, Comment(data[i].strip(),data[i+1].strip()))
                i+=2
    except FileNotFoundError:
        pass
    except:
        import traceback
        traceback.print_exc()