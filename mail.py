import smtplib
import config

def send_email(subject, mssg, email):
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(config.EMAIL_ADDRESS, config.PASSWORD)
        message = 'Subject: {}\n\n{}'.format(subject, mssg)
        server.sendmail(config.EMAIL_ADDRESS, email, message)
        server.quit()
    except Exception as e:
        print('Error: {}'.format(e))
        print('\nEmail failed to send!')




