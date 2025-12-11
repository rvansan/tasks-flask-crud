import pytest
import requests

BASE_URL = 'http://127.0.0.1:5000'
tasks = []


def test_create_task():
    # objeto que será enviado para o endpoint de criação de nova task.
    new_task_data = {
        'title': 'nova tarefa',
        'description':'descrição da nova tarefa'
    }

    # chamada no endpoint de criação de nova task, passando a task criada no passo anterior.
    response = requests.post(f"{BASE_URL}/tasks", json=new_task_data)
    
    # verificação do status code retornado, e se for 200, teste passa com sucesso. 
    assert response.status_code == 200

    # recupera os dados retornados pela chamada
    response_json = response.json()

    # verifica se os campos message e id estão no corpo da resposta. Para cada um deles, um teste é retornado
    assert 'message' in response_json
    assert 'id' in response_json

    # inclui o id da task criada na lista de tasks para usá-la em outros testes
    tasks.append(response_json['id'])

def test_get_tasks():
    # chamada para listar tasks da API
    response = requests.get(f"{BASE_URL}/tasks")

    # verificação do status code retornado, e se for 200, teste passa com sucesso.
    assert response.status_code == 200

    # recupera os dados retornados pela chamada
    response_json = response.json()
    
    # verifica se os campos tasks e total_tasks estão no corpo da resposta. Para cada um deles, um teste é retornado
    assert 'tasks' in response_json
    assert 'total_tasks' in response_json


def test_get_test():
    # caso haja algo na lista
    if tasks:

        # recupera o id da primeira task na lista
        task_id = tasks[0]

        # chamada para retornar a task
        response = requests.get(f'{BASE_URL}/tasks/{task_id}')
        
        # verificação do status code retornado, e se for 200, teste passa com sucesso.
        assert response.status_code == 200

        # recupera os dados retornados pela chamada
        response_json = response.json()

        # verifica se o campo id retornado é o mesmo que enviamos. Caso seja, teste passa com sucesso
        assert task_id == response_json['id']

def test_update_task():
    if tasks:
        task_id = tasks[0]
        payload = {
            'completed':True,
            'description':'descrição atualizada',
            'title':'título atualizado'
        }
        response = requests.put(f'{BASE_URL}/tasks/{task_id}', json=payload)
        assert response.status_code == 200
        response_json = response.json()
        assert 'message' in response_json

        response = requests.get(f'{BASE_URL}/tasks/{task_id}')
        assert response.status_code == 200
        response_json = response.json()
        assert payload['completed'] == response_json['completed']
        assert payload['description'] == response_json['description']
        assert payload['title'] == response_json['title']

def test_delete_task():
    if tasks:
        task_id = tasks[0]
        response = requests.delete(f'{BASE_URL}/tasks/{task_id}')
        assert response.status_code == 200
        response = requests.get(f'{BASE_URL}/tasks/{task_id}')
        assert response.status_code == 404