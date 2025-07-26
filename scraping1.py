import requests
from bs4 import BeautifulSoup
from collections import Counter
import re
import matplotlib.pyplot as plt
import pandas as pd 
url='https://news.ycombinator.com/item?id=43858554'
response=requests.get(url)
# print(response)
# print(response.content)

soup=BeautifulSoup(response.content,'html.parser')
# print(soup)

elements=soup.find_all(class_='ind',indent=0)
comments=[e.find_next(class_='comment') for e  in elements]
# print(comments)

keyword_map = {
    "languages": ["python", "javascript", "java", "php", "go", "ruby"],
    "frontend": ["react", "angular", "vue", "svelte", "next.js", "tailwind"],
    "backend": ["node.js", "django", "flask", "spring", "rails"],
    "data": ["ai", "ml", "nlp", "pandas", "tensorflow", "pytorch"],
    "devops": ["docker", "kubernetes", "aws", "cloud", "terraform"],
}

#flatten the keyword_map and make it one array 
keywords=[]
for category in keyword_map.keys():
    keywords.extend(keyword_map[category])


counter=Counter() 
for comment in comments:   #for each comment
    
    comment_text=comment.get_text().lower()                 #make that comment a lowercase
    cleaned_comment = re.sub(r'[^\w\s]', '', comment_text)   #remove anything that is not a letter 
    words = set(cleaned_comment.split())                     #split the text into words and remove duplicates
    
    for word in words:                            #for each word in the unique words
        if word in keywords:                   #check if that word in the key_map 
            counter[word]+=1                  #if true increase the count of it 

print(counter)
plt.figure(figsize=(12, 6))
plt.bar(counter.keys(), counter.values())
plt.ylabel("number of Mentions")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()



category_counts={category:0 for category in keyword_map}

for word,count in counter.items():
    for category, keywords in keyword_map.items():
        if word in keywords:
            category_counts[category]+=count


plt.figure(figsize=(10, 10))
plt.pie(category_counts.values(),labels=category_counts.keys(),autopct='%1.1f%%',startangle=90)
plt.title('Tech by Category')
plt.show()

df_keywords=pd.DataFrame(counter.items(),columns=[['technology','Count']])
df_keywords.to_csv("tech_trends.csv",index=False)

df_categories = pd.DataFrame(category_counts.items(), columns=['Category', 'Count'])
df_categories.to_csv('category_counts.csv', index=False)

