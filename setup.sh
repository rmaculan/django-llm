#!/bin/bash

# Create Django project
django-admin startproject local_llm_chat .

# Create main app
python manage.py startapp chat

# Create necessary directories
mkdir -p static templates
mkdir -p chat/templates/chat
mkdir -p chat/static/chat 