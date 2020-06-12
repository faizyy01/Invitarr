FROM python
COPY . /app
WORKDIR /app
RUN pip install discord.py
RUN pip install plex.py
RUN pip install plexapi
CMD python -u ./Invitarr-docker.py
