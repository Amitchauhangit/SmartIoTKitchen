# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 01:28:57 2018

@author: Dragon
"""

from subprocess import Popen,PIPE

def config():
      p=Popen(["aws","configure"],stdin=PIPE)
      p.communicate("AWS Access Key ID")
      p.communicate("#\n")
      p.communicate("AWS Secret Access Key")
      p.communicate("#\n")
      p.communicate("us-east-2") #region name
      p.communicate("#\n")

