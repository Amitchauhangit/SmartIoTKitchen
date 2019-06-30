#!/usr/bin/env python3
from subprocess import run, PIPE

def main():
        
    p = run(['aws','configure'], stdout=PIPE, input='AKIAJNVX2MRBHIBSXOMQ\r\nsmXgfQ2b4Lw8O51RmDLh+wYepWg1oaYWhfQpa8PB\r\nus-east-2\n\n', encoding='ascii')

    print(p.returncode)
