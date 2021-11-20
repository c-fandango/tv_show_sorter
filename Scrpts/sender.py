import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ast
import datetime
print('sender')
print(datetime.datetime.now())

with open("/home/pi/Comedy_proj/records/master1.txt","r") as file:
    master=ast.literal_eval(file.read())

with open("/home/pi/Comedy_proj/records/master2.txt","r") as file:
    master2=ast.literal_eval(file.read())

count_old=master2[0]    
count=master[0]
olen=master[1]
mrg = master[2]


if count_old != count -1:
        print("count error")
        quit()

smtp_server=""
sender_email=""
receiver_email=""
context=ssl.create_default_context()
password= ''

def tup(x):
        tup_flag=False
        lst_flag=False
        for i in x: 
            if type(i) ==tuple:
                tup_flag=True
                break
        for i in x:
            if type(i) == list:
                lst_flag=True
                break

        if tup_flag and not lst_flag:
            x.append([])    
        if lst_flag and not tup_flag:
            lst=[]
            if len(x)%2==0:    
                for i in range(0,len(x),2):
                    lst.append((x[i],x[i+1]))
            if len(x)%2 != 0:
                a=x[-1]
                for i in range(0,len(x)-1,2):
                    lst.append((x[i],x[i+1]))
                lst.append((a,[]))
            x=lst
            x.append([])
        if ([],[]) in x:
                x.remove(([],[]))
            
        return(x)

def checker(x,l,c):
        y=[]
        for i in x:
                if type(i)==list:
                        y.append(i)
        if max(y, key=len) == l:
                    smtp_server=""
                    sender_email=""
                    receiver_email=""
                    context=ssl.create_default_context()
                    password= ''    
                    message = MIMEMultipart("alternative")
                    message["Subject"] = f"Sorting Finished"
                    message["From"] = sender_email
                    message["To"] = receiver_email
                    flist=''
                    for j in y:
                            if len(j)==max(y,key=len):
                                    mx=j
                
                    for k in range(len(mx)):
                            flist=flist + f"\n {k} - {mx[k]}"
                            
                    text= f"Congratulations, the ordered list is complete - it took {c} steps. \n Here is the list:" + flist
                    
                    body=MIMEText(text,'plain')
                    message.attach(body)

                    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                        server.login(sender_email, password)
                        server.sendmail(sender_email, receiver_email, message.as_string())
                    quit()    
                    return()
                        
                
        else:
                return()
        

def send(mrg,olen,count):
        
            checker(mrg,olen,count)                
            #if len(mrg[-2])==olen:            
                #return("done",mrg[-2])
                #break
            mrg=tup(mrg)
     
            if len(mrg[0][0]) ==0 or len(mrg[0][1]) ==0:                 
                if len(mrg[0][0])==0:
                    mrg[-1]=mrg[-1]+mrg[0][1]
                    mrg.pop(0)
                    mrg.append([])
                elif len(mrg[0][1])==0:
                    mrg[-1]=mrg[-1]+mrg[0][0]
                    mrg.pop(0)
                    mrg.append([])
                    
            mrg=tup(mrg)

            rcd=[count,olen,mrg]
            with open(f"/home/pi/Comedy_proj/records/record_step_{count}.txt","w+") as file:
                file.write(str(rcd))

            with open(f"/home/pi/Comedy_proj/records/master2.txt","w+") as file:
                file.write(str(rcd))
            
            if len(mrg[0][0]) !=0 and len(mrg[0][1]) !=0:
                    optionA = mrg[0][0][0]
                    optionB = mrg[0][1][0]
                    
                    message = MIMEMultipart("alternative")
                    message["Subject"] = f"Choice To Make ({count+1})"
                    message["From"] = sender_email
                    message["To"] = receiver_email
    
                    text= f"Which Comedy Is Better?:  \n  \n {optionA}[A] or {optionB}[B]"
                    body=MIMEText(text,'plain')
                    message.attach(body)

                    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                        server.login(sender_email, password)
                        server.sendmail(sender_email, receiver_email, message.as_string())
                    print("All is well")
            return()
            #email stuff

print(send(mrg,olen,count))
quit()
