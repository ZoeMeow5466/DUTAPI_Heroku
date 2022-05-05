
from click import style
import dutapi
from flask import Flask, redirect, url_for, request, Response
import json

app = Flask(__name__)

# Login
def login(username: str, password: str):
    repText = None
    repCode = 200
    repType = "text/html; charset=utf-8"
    if username != None and password != None:
        dutss = dutapi.Session()
        repText = dutss.Login(username, password)
        repCode = 200
        if repText['loggedin'] == False:
            repCode = 401
        repType = "application/json" 
    else:
        repText = 'Bad request!'
        repCode = 400
    return Response(repText, status=repCode, mimetype=repType)    


# Logout
def logout(sessionid: str):
    repText = None
    repCode = 200
    repType = "text/html; charset=utf-8"
    if sessionid != None:
        dutss = dutapi.Session()
        dutss.SetSessionID(sessionid)
        repText = dutss.Logout()
        if repText['loggedin'] == True:
            repCode = 401
        repText = json.dumps(repText, ensure_ascii=False).encode('UTF-8')
        repType = "application/json"   
    else:
        repText = 'Bad request!'
        repCode = 400
    return Response(repText, status=repCode, mimetype=repType)    


# Subject schedule
def subjectschedule(sessionid: str, year: int, semester: int, insummer: int):
    repText = None
    repCode = 200
    repType = "application/text"
    if sessionid != None and year != None and semester != None and insummer != None:
        dutss = dutapi.Session()
        dutss.SetSessionID(sessionid)
        if dutss.IsLoggedIn()['loggedin'] == True:
            repText = json.dumps(dutss.GetSubjectSchedule(year, semester, True if insummer == 1 else False), ensure_ascii=False).encode('UTF-8')
            repCode = 200
            repType = "application/json"            
        else:
            repText = "Unauthorized"
            repCode = 401
    else:
        repText = 'Bad request!'
        repCode = 400
    return Response(repText, status=repCode, mimetype=repType)


# Subject fee
def subjectfee(sessionid: str, year: int, semester: int, insummer: int):
    repText = None
    repCode = 200
    repType = "text/html; charset=utf-8"
    if sessionid != None and year != None and semester != None and insummer != None:
        dutss = dutapi.Session()
        dutss.SetSessionID(sessionid)
        if dutss.IsLoggedIn()['loggedin'] == True:
            repText = json.dumps(dutss.GetSubjectFee(year, semester, True if insummer == 1 else False), ensure_ascii=False).encode('UTF-8')
            repCode = 200
            repType = "application/json"            
        else:
            repText = "Unauthorized"
            repCode = 401
    else:
        repText = 'Bad request!'
        repCode = 400
    return Response(repText, status=repCode, mimetype=repType)


@app.route('/account', methods=['GET', 'POST'])
def account():
    sType = request.args.get('type')
    try:
        if sType == None:
            return Response('Bad request!', status=400, mimetype='text/html; charset=utf-8')
        elif sType.lower() == 'login':
            if request.method == 'POST':
                return login(request.args.get('user'), request.args.get('pass'))
        elif sType.lower() == 'logout':
            if request.method == 'POST':
                return logout(request.args.get('sid'))
        elif sType.lower() == 'subjectschedule':
            if request.method == 'POST':
                return subjectschedule(request.args.get('sid'), request.args.get('year'), request.args.get('semester'), request.args.get('insummer'))
        elif sType.lower() == 'subjectfee':
            if request.method == 'POST':
                return subjectfee(request.args.get('sid'), request.args.get('year'), request.args.get('semester'), request.args.get('insummer'))
        else:
            return Response('Bad request!', status=400, mimetype='text/html; charset=utf-8')
    # If something went wrong, will return back to homepage.
    except:
        return Response('Internal Server Error!', status=500, mimetype='text/html; charset=utf-8')


# News
def news(type: dutapi.NewsType, page: int):
    repText = None
    repCode = 200
    repType = "application/text"
    try:
        if (type == None) or (type.lower() != "global" and type.lower() == "subjects"):
            repText = "Bad request!"
            repCode = 400
        else:
            if (page == None) or (page.isdigit() == False):
                page = 1
            else:
                page = int(page)
                if page < 1: page = 1
            repText = json.dumps(dutapi.GetNews(dutapi.NewsType.General if type.lower() == "global" else dutapi.NewsType.Subjects, page), ensure_ascii=False).encode('UTF-8')
            repType = "application/json"
    except:
        repText = "Internal Server Error!"
        repCode = 500
    finally:
        return Response(repText, status=repCode, mimetype=repType)    


@app.route('/news', methods=['GET'])
def getNews():
    sType = request.args.get('type')
    page = request.args.get('page')
    if request.method == 'GET':
        return news(sType, page)
        

@app.route('/')
def index():
    return "DUTAPI"

if __name__ == '__main__':
    app.run()
