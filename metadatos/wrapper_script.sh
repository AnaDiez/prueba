#!/bin/bash
set -m
./servidorMetadatos 3005 & 
python new_receive.py 
fg %1