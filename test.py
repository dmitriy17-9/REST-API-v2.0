from requests import get, post, delete

print(get('http://localhost:8080/api/v2/users').json())

print(post('http://localhost:8080/api/v2/users', json={'surname': 'API',
                                                        'name': 'User',
                                                        'age': 99,
                                                        'position': 'ROOT',
                                                        'speciality': 'worker',
                                                        'address': 'module_1',
                                                        'email': 'a@a.a',
                                                        'hashed_password': '1'}))

print(get('http://localhost:8080/api/v2/users/7').json())

print(get('http://localhost:8080/api/v2/users/999').json())

print(delete('http://localhost:8080/api/v2/users/7').json())

print(delete('http://localhost:8080/api/v2/users/999').json())
