import json
import imaplib
import email
from bs4 import BeautifulSoup
import ast
import datetime
print('receiver')
print(datetime.datetime.now())

with open("/home/pi/Comedy_proj/records/master2.txt","r") as file:
    mstr=ast.literal_eval(file.read())

count=mstr[0]
olen=mstr[1]
mrg=mstr[2]
print(count)
def get_response(count):
    
    username = ""
    receiver_email = ""
    password = ''

    imap=imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(username,password)
    messages = imap.select("Cmdy")

    typ,data=imap.search(None,'All')
    mail_ids=data[0]
    id_list=mail_ids.split()
    lst=data[0].split()
    lst.reverse()
    for num in lst:
            typ,data = imap.fetch(num,'(RFC822)')
            raw_email=data[0][1]
            raw_string=raw_email.decode('UTF-8')
            email_message=email.message_from_string(raw_string)
            print(1)
            for response_part in data:
                    if isinstance(response_part, tuple):
                        '''msg = email.message_from_string(response_part[1].decode('utf-8'))
                        email_subject = msg['subject']
                        email_from = msg['from']
                        print ('From : ' + email_from + '\n')
                        print(str(count+1))
                        print ('Subject : ' + email_subject + '\n')
                        if str(count+1) in email_subject:
                            html_doc = str(msg.get_payload(decode=True))
                            soup= BeautifulSoup(html_doc,'html.parser')
                            
                            choice=soup.get_text()[2]
                            break
                        else:
                                continue
                        print("No Email Recieved")
                        quit()'''
                        msg = email.message_from_string(response_part[1].decode('utf-8'))
                        email_subject = msg['subject']
                        b = email.message_from_string(raw_string)
                        body = ""
                        print(email_subject)
                        if str(count) in email_subject:
                                if b.is_multipart():
                                  print(3)
                                  for part in b.walk():
                                    ctype = part.get_content_type()
                                    cdispo = str(part.get('Content-Disposition'))
                                    # skip any text/plain (txt) attachments
                                    if ctype == 'text/plain' and 'attachment' not in cdispo:
                                        body = part.get_payload(decode=True)  # decode
                                        choice=str(body)[2]    
                                        return(choice)
                            # not multipart - i.e. plain text, no attachments, keeping fingers crossed
                                else:
                                  print(4)
                                  html_doc = str(msg.get_payload(decode=True))
                                  soup= BeautifulSoup(html_doc,'html.parser')
                                  choice=soup.get_text()[2]
                                  return(choice)
                                  
                                  
                        else:
                            print(5)
                    
                            continue
                 
choice=get_response(count)
print("choice =",choice)
choice=choice.capitalize()
optionA = mrg[0][0][0]
optionB = mrg[0][1][0]


if choice == "A" or choice == "B":
        
        if choice == "A":
                            mrg[0]=list(mrg[0])
                            mrg[0][1].pop(0)
                            mrg[0]=tuple(mrg[0])
                            mrg[-1].append(optionB)
        if choice == "B":
                            mrg[0]=list(mrg[0])
                            mrg[0][0].pop(0)
                            mrg[0]=tuple(mrg[0])
                            mrg[-1].append(optionA)


        if len(mrg[0][0]) ==0 or len(mrg[0][1]) ==0:                    
                    if len(mrg[0][0])==0:
                        mrg[-1]=mrg[-1]+mrg[0][1]
                        mrg.pop(0)
                        mrg.append([])
                    elif len(mrg[0][1])==0:
                        mrg[-1]=mrg[-1]+mrg[0][0]
                        mrg.pop(0)
                        mrg.append([])
        

        count+=1
        mstr1=[count,olen,mrg]
        with open("/home/pi/Comedy_proj/records/master1.txt","w") as file:
            file.write(str(mstr1))
        print("All is well")
        quit()

print("Invalid Choice")
quit()
