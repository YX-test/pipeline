FROM wcfdehao/python3.9_java_822
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python3", "-m", "pytest", "--alluredir=reports"]