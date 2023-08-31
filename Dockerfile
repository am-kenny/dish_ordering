FROM python:latest

EXPOSE 5000

WORKDIR /app
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "app.py" ]

LABEL authors="Andrii"

# to create image use:
# docker build -t dish_ordering-app .

# to create container use:
# docker run -it --rm --name dish_ordering-running-app dish_ordering-app
