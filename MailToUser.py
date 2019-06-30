# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 12:02:47 2018

@author: Dragon
"""
import smtplib

def mail(location):
	

	s=smtplib.SMTP()
	s.connect("email-smtp.us-east-1.amazonaws.com",465) # mailserver , port
	s.starttls()
	s.login("AKIAITKZLBMAEZI4K7DQ","Ap21Iv1m6Ces88k/C4YlfI+LI4ABmOVKhxjOB/aW/Wf1") #login credentials.(<SESSMTPUSERNAME> <SESSMTPPASSWORD>)

	msg="From: smartiotkitchen@gmail.com\nTo: amitthesingh92@gmail.com\nSubject: notification for items\n\n" + location

	s.sendmail("smartiotkitchen@gmail.com","amit.chauhan1702@gmail.com",msg)
#mail sent
