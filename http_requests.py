import requests

# r = requests.get('https://jsonplaceholder.typicode.com/posts')

# print(r.status_code)
# print(r.json())
#
# r = requests.post('https://jsonplaceholder.typicode.com/posts', json={'title': 'foo', 'body': 'bar', 'userId': 1})
# print(r.status_code)
# print(r.json())
#
# r = requests.put('https://jsonplaceholder.typicode.com/posts/1', json={'title': 'foo', 'body': 'bar', 'userId': 1})
# print(r.status_code)
# print(r.json())
#
# r = requests.delete('https://jsonplaceholder.typicode.com/posts/1')
# print(r.status_code)
# print(r.json())

r = requests.get('http://localhost:8000/')
print(r.status_code)
print(r.text)
print(r.headers)