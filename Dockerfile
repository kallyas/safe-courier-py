# Docker file for the flask api
# depends on mysql database


FROM python:3.9.0-alpine3.11


# create working directory
WORKDIR /app

# copy the flask app except venv
COPY . .

# create venv
RUN pip install --upgrade pip
RUN pip install virtualenv
RUN virtualenv -p python3 venv

# activate venv
ENV PATH /app/venv/bin:$PATH
ENV VIRTUAL_ENV /app/venv

# install requirements
RUN /app/venv/bin/pip install -r requirements.txt


# run the flask app using gunicorn
CMD ["/app/venv/bin/gunicorn", "app:app", "-w", "4", "-b", ":5000"]


