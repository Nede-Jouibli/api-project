FROM python:3.10
WORKDIR /usr/scr/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

#copy all source code to the current directory
COPY . .  

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]