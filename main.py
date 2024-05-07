from search import Search
from translate import gel_to_eng,eng_to_gel


es = Search()
query = "ტანის და სახის დასაბანი გელი"
georgian_to_english = gel_to_eng(query)

results = es.search_documents(georgian_to_english)

for result in results:
    print(f"SKU: {result['sku']}")
    print(f"Name: {result['name']}")
    print(f"Description: {result['description'][:200]}...")  # Print truncated description
    print(f"Short Description: {result['short_description']}")
    print(f"Price: {result['price']}")
    print(f"Price: {result['country_of_manufacture']}")
    print(f"Special Price: {result['special_price']}")
    print(f"Categories: {result['categories']}")
    print(f"Score: {result['score']}")
    print("-" * 40)