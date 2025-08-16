FROM python:3.13.7-slim-trixie

WORKDIR /app

COPY . . 

RUN python3 -m pip install -r  requirements.txt

EXPOSE 8000

CMD ["fastapi", "run", "main.py"]
