# Import modules
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import ssl
from string import Template
import getpass

# To form a contact list
def contacts(filename):
    names=[]
    mail_id=[]
    
    with open(filename,mode='r',encoding='utf-8') as fname:
        for contact in fname:
            names.append(contact.split()[0])
            mail_id.append(contact.split()[1])
    return names, mail_id


# To form a mailing template
def template(filename):
    with open(filename,encoding='utf-8') as fname:
        temp = fname.read()
        
    return Template(temp)

def mailer():
    names,mail_id=contacts('msg_list.txt')
    
    #userid = getpass.getuser() # did not use  since it takes the os user id
    sender_email = 'yashlaboratoire@gmail.com'
    password = getpass.getpass('Enter your password')

    context = ssl.create_default_context()
    mail_template = template('message.txt')

    # set up mail server:
    with smtplib.SMTP_SSL(host="smtp.gmail.com",port = 465,context=context) as server:    
        # login to the server
        server.login(sender_email,password)

        for name,email in zip(names,mail_id):
            msg = MIMEMultipart() # create message

            message = mail_template.substitute(name = name.title())
            print(message)
            msg['From'] = sender_email
            msg['To']=email
            msg['Subject']= "Python_Mailer"

            msg.attach(MIMEText((message),'plain'))

            html = """\
            <html>
              <body>
                <p>Hi,<br>
                   How are you?<br>
                   <a href="http://www.realpython.com">Real Python</a> 
                   has many great tutorials.
                </p>
              </body>
            </html>
            """

    #         part1 = MIMEText(message, "plain")
            part2 = MIMEText(html, "html")

    #         msg.attach(part1)
            msg.attach(part2)


            #server.send_message(msg)
            server.sendmail(sender_email,email,msg.as_string())

            #del msg
            print(msg.as_string())

        server.quit()