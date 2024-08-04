import requests
from bs4 import BeautifulSoup
import re
import mysql.connector 
from sklearn import tree

# Scraping
res = requests.get("https://www.scrapethissite.com/pages/simple/")
soup = BeautifulSoup(res.text, 'html.parser')
values = soup.find('body').text
myList = re.findall(r'.+\s+Capital:.+\s+.+\s+.+\.\d', values)

# database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="@meN9199",
  database ="mydatabase"
)
mycursor = mydb.cursor()

# create table
# mycursor.execute("CREATE TABLE countries (name VARCHAR(255), capital VARCHAR(255), population VARCHAR(255), area VARCHAR(255))")

mycursor.execute("SELECT * FROM countries")
myresult = mycursor.fetchall()

# insert into db
for i in range(len(myList)):
    newItem = re.sub(r'\s+',' ', myList[i]).strip()
    country = newItem.split(' Capital: ')[0]
    capital = newItem.split(' Capital: ')[1].split(' Population')[0]
    pop = newItem.split(' Population: ')[1].split(' Area')[0]
    area = newItem.split(' (km2): ')[1]
    sql = "INSERT INTO countries (name, capital, population, area) VALUES (%s, %s, %s, %s)"
    val = [(f'{country}', f'{capital}', f'{pop}', f'{area}')]
    try:
        if myresult[i][0] == val[0][0]:
            continue
        else:
            mycursor.executemany(sql, val)
            mydb.commit()
    except:
        mycursor.executemany(sql,val)
        mydb.commit()

# Machine Learning and predicting the area measurement of a country based on a given population
mycursor.execute("SELECT * FROM countries")
myresult = mycursor.fetchall()
x = []
y = []
for item in myresult:
    print(item)
    x.append([item[2]])
    y.append([item[3]])
print('########################################################')
clf = tree.DecisionTreeClassifier()
clf = clf.fit(x, y)
new_data = [[f'{input("Please enter the population by full digit format: ")}']]
answer = clf.predict(new_data)
print(f'The predicted area for the inputted population according to the database will be : {answer[0]} km^2')
    
    


        
    


