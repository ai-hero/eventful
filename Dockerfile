FROM python:3.10-slim-bullseye

RUN apt-get -y update && apt-get install -y --no-install-recommends build-essential  \
    wget nginx ca-certificates \
    && pip install --upgrade pip setuptools \ 
    && rm -rf /var/lib/apt/lists/*

# Set some environment variables. PYTHONUNBUFFERED keeps Python from buffering our standard
# output stream, which means that logs can be delivered to the user quickly. PYTHONDONTWRITEBYTECODE
# keeps Python from writing the .pyc files which are unnecessary in this case. We also update
# PATH so that the train and serve programs are found when the container is invoked.
ENV PYTHONUNBUFFERED=TRUE PYTHONDONTWRITEBYTECODE=TRUE PATH="/home/user/app:${PATH}" PYTHONPATH="/home/user/app:${PYTHONPATH}"

# Add non-root user
RUN groupadd -r user && useradd -r -g user user
RUN chown -R user /var/log/nginx /var/lib/nginx /tmp

# Install dependencies
COPY app/requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Set up the program in the image
COPY app /home/user/app
WORKDIR /home/user/app

# Add app folder and chown
RUN chown -R user /home/user/app

RUN pylint --disable=R,C ./**/*.py

# Finishing loose ends
EXPOSE 8080
ENTRYPOINT [ "sh", "./entrypoint" ]
USER user