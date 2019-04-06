import requests
import math
from bs4 import BeautifulSoup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import datetime


def start(bot, update):
    print("InsideStart!")

    texxt = "Hey <strong>" + update.message.chat.first_name + "</strong>\n" + \
        "Thanks for trying AttendanceBot!\nWe can help you maintain that sweet 75%\n Enter '/login username: password' to see results "

    bot.send_message(chat_id=update.message.chat_id, text=texxt,
                     parse_mode='HTML', disable_web_page_preview=True)


def attendance_fetcher(bot, update, args):

    if(args == []):
        bot.send_message(chat_id=update.message.chat_id,
                         text="enter login details like below: \n/login < username > : < password >")

    print("inside fetcher!")
    now = datetime.datetime.now()
    date2 = now.strftime("%Y-%m-%d")
    date1 = "2019-01-28"
    print(date2)

    subject_name = {
        "DESIGN AND ANALYSIS OF ALGORITHMS CS302": "DAA      ",
        "COMPILER DESIGN CS304": "CD        ",
        "COMPUTER NETWORKS CS306": "CN        ",
        "SOFTWARE ENGINEERING AND PROJECT MANAGEMENT CS308": "SEPM    ",
        "MICROPROCESSOR LAB CS332": "MP_LAB  ",
        "NETWORK PROGRAMMING LAB CS334": "NP_LAB  ",
        "COMPREHENSIVE EXAM CS352": "COMPR_EX",
        "WEB TECHNOLOGIES CS368": "WT       ",
        "PRINCIPLES OF MANAGEMENT HS300": "POM       ",
        "NATURAL LANGUAGE PROCESSING CS366": "NLP"



    }

    username = str(args[0].split(":")[0])
    password = str(args[0].split(":")[1])
    # username=args[0].split(":")[0]
    # password=args[0]
    print(username, password)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0',
        'Referer': 'http://mca.rit.ac.in/ritsoftv3/login.php',
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    response = requests.post(
        'http://mca.rit.ac.in/ritsoftv3/login.php', headers=headers)
    cookie = (response.headers['Set-Cookie'].split()[0])

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0',
        'Referer': 'http://mca.rit.ac.in/ritsoftv3/login.php',
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = 'username='+username+'&password='+password+'&login=Login'
    cookies = {
        'PHPSESSID': cookie.split('=')[1].strip(';')
    }
    print(cookies)

    response = requests.post('http://mca.rit.ac.in/ritsoftv3/login.php',
                             headers=headers, cookies=cookies, data=data, verify=False)

    headers2 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0',
        'Referer': 'http://mca.rit.ac.in/ritsoftv3/login.php',
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'multipart/form-data; boundary=---------------------------17760220484614',
    }
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-GB,en;q=0.5",
               "Referer": "http://mca.rit.ac.in/ritsoftv3/student/login.php", "Connection": "close", "Upgrade-Insecure-Requests": "1", "Content-Type": "multipart/form-data; boundary=---------------------------17760220484614"}
    cookies = {
        'PHPSESSID': cookie.split('=')[1].strip(';')
    }
    data = "-----------------------------17760220484614\r\nContent-Disposition: form-data; name=\"date1\"\r\n\r\n"+date1+"\r\n-----------------------------17760220484614\r\nContent-Disposition: form-data; name=\"date2\"\r\n\r\n" + \
        date2+"\r\n-----------------------------17760220484614\r\nContent-Disposition: form-data; name=\"btnshow-new\"\r\n\r\n\r\n-----------------------------17760220484614--\r\n"
    files = {'file': ''}
    proxies = {"http": "http://127.0.0.1:8080",
               "https": "http://127.0.0.1:8080"}
    response = requests.post('http://mca.rit.ac.in/ritsoftv3/student/parent_monthly.php',
                             headers=headers2, cookies=cookies, data=data)
    f = open("res.html", "w")
    f.write(response.text)
    f.close()
    soup = BeautifulSoup(response.text, "html.parser")
    i = 0
    sname = []
    total = []
    attended = []
    perc = []
    count = 1
    name = soup.find("td").text
    print(name)

    all_details = ""
    all_details_list = []

    table2 = soup.find_all('tbody')[0]
    for i in table2.find_all("tr"):
        all_details_list.append(i.text)
        # print(i.text)

    all_details_list = list(dict.fromkeys(all_details_list))
    # print(all_details_list)

    sub_tot_att_perc = []
    for i in all_details_list:
        l = i.split("\n")[1:]
        # print("".join(l)+"\n")
        print(l[0])
        if("".join(l).find("TOTAL") == -1 and l[0] != "PRINCIPLES OF MANAGEMENT HS300 "):
            sub_tot_att_perc.append(l)

    print(sub_tot_att_perc)
    for i in sub_tot_att_perc:
        try:
            sname.append(subject_name[i[0]])
        except:
            print(i[0])
            sname.append(i[0])

        total.append(i[1])
        attended.append(i[2])
        perc.append(i[3].replace(" ", ""))

    classcut = []

    for i in range(0, len(sname)):
        #print(attended[i],"   ",total[i],"   ",int(math.floor(float(attended[i])*(4/3))))
        a = int(math.floor((float(attended[i])*4)/3))
        b = int(total[i])
        classcut.append(a-b)

    final_text = ""
    print(sname)

    for i in range(len(sname)):
        # print(sname[i]+": " + attended[i] + "/"+total[i]+"  " +
        #       perc[i] + "  cuttable:"+str(classcut[i])+"\n")
        a = sname[i]+": " + attended[i] + "/"+total[i]+"  " + \
            perc[i] + "  cuttable:"+str(classcut[i])+"\n"
        final_text = final_text+a
    final_text = "<strong>ATTENDANCE: "+name + \
        "</strong>\nTill : "+date2+"\n\n"+final_text
    bot.send_message(chat_id=update.message.chat_id,
                     text=final_text, parse_mode="HTML")
    print(final_text)


def main():
    print("started!")

    f1 = open("token.txt", "r")
    token = f1.read().strip()
    updater = Updater(token)
    f1.close()

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("login", attendance_fetcher, pass_args=True))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
