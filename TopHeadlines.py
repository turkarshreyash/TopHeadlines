#!topheadlines/bin/python
from requests import get
from json import loads,dumps
import sqlite3
from time import time,sleep

class TopHeadlines:
   
    @staticmethod
    def api_call(country, category):
        api_key = "13b10238f15a4da8a43aedada799b8e6"
        url = 'https://newsapi.org/v2/top-headlines?country='+country+'&category='+category+'&apiKey='+api_key
        try:
            response = get(url)
            if response.status_code == 200:
                return response.json()
            raise Exception(str(response.status_code))
        except Exception as e:
            errors = {"400":"Bad Request","401":"Unauthorized Request","429":"Too many requests","500":"Server Error"}
            response = {'status': 'error','code': e}
            if errors.get(str(e)):
                response["message"] = errors[str(e)]
            else:
                response["message"] = "No more Info Available"
            return response
                
    @staticmethod
    def filter_response(country,category,q,response):
        filtered_response = {"status" : "ok", "country":country,"filter":q,"category":category}
        relevant_news = list()
        for i in response["articles"]:
            try:
                if q in str(i["title"]).lower() or q in str(i["url"]).lower() or q in str(i["description"]).lower() or q in str(i["content"]).lower():
                    #print(f"{i['title']} {i['url']} {i['description'][:10]}")
                    relevant_news.append({"title" : i['title'],"url":i['url'],"description":i['description'][:100]})
            except:
                pass
        filtered_response["articles"] = relevant_news
        return filtered_response
                       
    @staticmethod
    def query(*argv):
        try:
            if len(argv) != 3 or (not argv[0].isalnum()) or (not argv[1].isalnum()) or (not len(argv[0]) == 2):
                raise Exception
            country = argv[0]
            category = argv[1]
            q = argv[2]
            country = country.lower()
            category = category.lower()
            q = q.lower()
            q = " ".join(q.split())
        except:
            response = {"status":"error","message":"Bad Request","code":"400"}
            return response
        conn = sqlite3.connect("cache.db")
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Query(Country TEXT, Category TEXT,q TEXT,Description TEXT, ADDED_AT REAL)''')
        cursor.execute('''DELETE FROM Query WHERE ((?-ADDED_AT) >= ?)''',(time(),600,))
        conn.commit()
        cursor.execute('''SELECT Description FROM Query WHERE (Country = ?) AND (Category = ?) AND (q = ?)''',(country,category,q,))
        cached = cursor.fetchone()
        if not cached == None:
            #print("cache hit")
            conn.close()
            return loads(cached[0])
        else:
            #print("cache miss")
            response = TopHeadlines.api_call(country,category)
            if response["status"] == "ok":
                response = TopHeadlines.filter_response(country,category,q,response)
                cursor.execute('''INSERT INTO Query VALUES(?,?,?,?,?)''',(country,category,q,dumps(response),time()))
                conn.commit()
            conn.close()
            return response

if __name__ == "__main__":
    #your queries goes here
    #example:
        #my_query = TopHeadlines.query("country ISO 3166 Code","category","keyword")
        #print(my_query)


    #TEST_CASES:

    test_case1 = TopHeadlines.query("us","technology","apple")
    print(test_case1)
    #explaination:
    #            Simple test to search for country : us, category : technology and keyword : apple 


    test_case2 = TopHeadlines.query("US","TECHnology","aPPle")
    print(test_case2)
    #explaination:
    #            This test case will return cached result for the test_case1 query as both this querires are same and what differs is the case of alphabets.

    test_case3 = TopHeadlines.query("india","business","amazon")
    print(test_case3)
    #explaination:
    #            This test case will return error as "Bad Request" and code as "400" because country is not given in ISO 3166 standards

    test_case4 = TopHeadlines.query("ae","business","شبكة")
    print(test_case4)
    #explaination:
    #            Simple test to search for country : united arab emirates, category : business and keyword :  شبكة 

    test_case5 = TopHeadlines.query("ru","health")
    print(test_case5)
    #explaination:
    #            This test case will return error as "Bad Request" and code as "400" because keyword isn't supplied



    test_case6 = TopHeadlines.query("ca","general","price")
    print(test_case6)
    #explaination:
    #            Simple test to search for country : canada, category : general and keyword : price 

    #adding delay for 5 mins
    sleep(300)

    test_case7 = TopHeadlines.query("ca","general","price")
    print(test_case7)
    #explaination:
    #            This test case will return cached data of test_case6 as parameters are same this cached data is stored in sqllite database.

    #adding delay for another 6 mins
    sleep(360)

    test_case8 = TopHeadlines.query("ca","general","price")
    print(test_case8)
    #explaination:
    #            This test case will not return cached data of test_case6 and will make api call as time_elapsed_since_test_case6 > 10mins
