from flask import Flask, jsonify, request
from models.task import Task
app = Flask(__name__)


tasks = []
task_id_control = 1

@app.route('/tasks', methods=['POST'])
def create_task():
    #define acesso global à variável task_id_control para podermos usá-la
    global task_id_control

    # recupera o que o cliente enviou
    data = request.get_json() 

    # cria uma nova tarfa com os dados fornecidos pelo usuário, utilizando o task_id_control para definir o id
    new_task = Task(id=task_id_control, title=data['title'], description=data.get('description', '')) 

    # atualiza o task_id_control
    task_id_control += 1

    # inclui a nova task na lista de tarefas e print no prompt para debug
    tasks.append(new_task)
    print(tasks)

    # retorna um json contendo uma mensagem
    return jsonify({'message':'Nova tarefa criada com sucesso.', 'id':new_task.id })

@app.route('/tasks', methods=['GET'])
def get_tasks():
    # lista com o retorno do método, recebendo o resultado do método to_dict, que converte objeto em dicionário, para cada task dentro de tasks, conforme o for a frente
    task_list = [task.to_dict() for task in tasks ]
    
    # montando o objeto com o task_list para o retorno e o total de objetos na lista
    output = {
        'tasks': task_list,
        'total_tasks': len(task_list)
    }

    # retorna um json contendo a lista de recursos
    return jsonify(output)



@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    ''' é executado um for por toda lista de tarefas, verificando se há algum objeto na lista com o 
    id igual ao id passado na rota. Caso haja, ele retorna o objeto transformado em dicionário. 
    Caso não haja, ele retorna uma mensagem indicando que não encontrou, junto do status code 404 '''
    for t in tasks:
        if t.id == id:
            return jsonify(t.to_dict())

    return jsonify({'message':'Não foi possível encontrar a atividade'}), 404


@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = None
    ''' é executado um for por toda lista de tarefas, verificando se há algum objeto na lista com o 
    id igual ao id passado na rota. Caso haja, ele atribui esse objeto à task que criamos nula. 
    Caso não haja, ele retorna uma mensagem indicando que não encontrou, junto do status code 404 '''
    for t in tasks:
        if t.id == id:
            task = t
    if task == None:
        return jsonify({'message':'não foi possível encontrar a atividade'}), 404
    
    # recupera o objeto enviado pelo usuário
    data = request.get_json()

    #recupera os valores do objeto enviado pelo usuário
    task.title = data['title']
    task.description = data['description']
    task.completed = data['completed']

    #retorna mensagem de sucesso ao usuário
    return jsonify({'message':'tarefa atualizada com sucesso.'})


@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    ''' é executado um for por toda lista de tarefas, verificando se há algum objeto na lista com o 
    id igual ao id passado na rota. Caso haja, ele atribui esse objeto à task que criamos nula. 
    Caso não haja, ele retorna uma mensagem indicando que não encontrou, junto do status code 404 '''
    task = None
    for t in tasks:
        if t.id == id:
            task = t
            
            
    if not task:
        return jsonify({'message':'não foi possível encontrar a atividade'}), 404

    # remove o recurso da lista
    tasks.remove(task)

    #retorna mensagem de sucesso ao usuário
    return jsonify({'message':'Tarefa deletada com sucesso.'})



if __name__ == '__main__':
    app.run(debug=True)