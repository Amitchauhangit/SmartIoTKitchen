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
	s.login("AKIAI*****7DQ","Ap21Iv1m6Ces88k/C4****OB/aW/Wf1") #login credentials.(<SESSMTPUSERNAME> <SESSMTPPASSWORD>)

	msg="From: smartiotkitchen@gmail.com\nTo: amitthesingh92@gmail.com\nSubject: notification for items\n\n" + location
	if(!mailcontentcheck(msg)):
		s.sendmail("smartiotkitchen@gmail.com","amit.chauhan1702@gmail.com",msg)
	else:
		print("No Special Char allowed")
#mail sent

def mailcontentcheck(mailbody):
	special_characters = ""!@#$%^&*()-+?_=,<>/""
	if any(c in special_characters for c in s):
		return true
	else:
		return false
	
