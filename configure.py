# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 01:28:57 2018

@author: Dragon
"""

from subprocess import Popen,PIPE
p=Popen(["aws","configure"],stdin=PIPE)
p.communicate("AKIAJNVX2MRBHIBSXOMQ")
p.communicate("#\n")
p.communicate("smXgfQ2b4Lw8O51RmDLh+wYepWg1oaYWhfQpa8PB")
p.communicate("#\n")
p.communicate("us-east-2")
p.communicate("#\n")

