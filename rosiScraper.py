import requests
from bs4 import BeautifulSoup
import json
import sys

def login(url, username, password):
    with requests.Session() as s:
        payload = {'personId': username, 'pin': password, 'verify.dispatch': '1'}
        p = s.post(login_url, data=payload)
        return s

if __name__ == "rosiScraper__main__":

    username = ""
    password = ""
    if len(sys.argv) != 3:
        username = input("Enter UTORID: ")
        password = input("Enter PIN: ")
    else:
        username = sys.argv[1]
        password = sys.argv[2]

    # log-in to rosi
    login_url = 'https://sws.rosi.utoronto.ca/sws/auth/login/verify.do'
    session = login(login_url, username, password)

    # move to transcript url
    transcript_url = 'https://sws.rosi.utoronto.ca/sws/transcript/academic/view.do?view.dispatch&mode=complete&displayName='
    transcript = session.get(transcript_url)

    # make a soup and find courses block
    soup = BeautifulSoup(transcript.text, "html.parser")
    tables = soup.findAll("div", { "class" : "courses" })

    # grab da grades
    new_grades = []
    for table in tables:
        courses = str(table.text).split("\n")
        for course in courses:
            c = course.split("  ")
            c = [comp for comp in c if comp != ""]
            if len(c) >= 4:
                code = c[0]
                mark = c[3]
                if mark != 'IPR':
                    new_grades.append((code, mark))

    # write to json, comparing with previous marks
    try:
        f = open("marks.json", "r")
        old_grades = json.loads(f.read())
        diff = len(new_grades) - len(old_grades)
        # new marks
        print "checking for new marks..."
        if diff > 0:
            print "new marks!"
            for i in range(1,diff+1):
                print (str(new_grades[-1*i][0]), str(new_grades[-1*i][1]))
        else:
            print "no new marks </3"
    except IOError:
        print "first time running, no previous marks to check against"
        # if first time, write
        with open("marks.json", "w") as f:
            json.dump(new_grades, f)

    #logout
    session.post("https://sws.rosi.utoronto.ca/sws/auth/logout.do?logout.dispatch")
