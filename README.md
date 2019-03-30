# TopHeadlines

Service to find relevant news for a particular Category and Country. The json output from NEWS API is further filtered for relevant keyword provided to the Micro-service (example Keyword = Tendulkar).
API call isn't made if call using same parameters was made in last 10 minutes, it is cached in sqlite database

Output is json containing:

Country
Category
Filter keyword
News Title
Description (first 100 words)
Source News URL
In case of bad parameters the API should return proper error messages.

API to fetch news data:

https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey={api-key}

API Key:13b10238f15a4da8a43aedada799b8e6
