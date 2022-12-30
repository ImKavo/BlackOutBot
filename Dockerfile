FROM python:3.9
# set work directory
WORKDIR /usr/src/app/
# copy project
COPY . /usr/src/app/
# install dependencies
RUN pip install --user aiogram
# run app
CMD ["python", "function.py"]