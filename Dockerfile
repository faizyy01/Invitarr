FROM gorialis/discord.py
WORKDIR /app
COPY . .
RUN pip install -Ur requirements.txt
CMD ["python", "-u", "run.py"]
