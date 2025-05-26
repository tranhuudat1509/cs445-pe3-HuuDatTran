from flask import Flask, jsonify, request
from flask_restx import Api, Resource, fields

app = Flask(__name__)
api = Api(app)

# Sample in-memory data store
# Each task has an ID, title, and completion status
tasks = {
    1: {"title": "Buy groceries", "done": False},
    2: {"title": "Do laundry", "done": True},
}

# Request model for input validation
task_model = api.model('Task', {
    'title': fields.String(required=True, description='Title of the task'),
    'done': fields.Boolean(required=True, description='Task completion status')
})

@api.route('/tasks')
class TaskList(Resource):
    def get(self):
        """Get the list of all tasks"""
        return jsonify(tasks)

    @api.expect(task_model)
    def post(self):
        """Add a new task"""
        new_id = max(tasks.keys(), default=0) + 1
        tasks[new_id] = request.json
        return {"message": "Task added", "task_id": new_id}, 201

@api.route('/tasks/<int:task_id>')
class Task(Resource):
    def get(self, task_id):
        """Retrieve a specific task by ID"""
        task = tasks.get(task_id)
        if task:
            return task
        return {"error": "Task not found"}, 404

    @api.expect(task_model)
    def put(self, task_id):
        """Update an existing task"""
        if task_id not in tasks:
            return {"error": "Task not found"}, 404
        tasks[task_id] = request.json
        return {"message": "Task updated"}

    def delete(self, task_id):
        """Delete a task by ID"""
        if task_id in tasks:
            del tasks[task_id]
            return {"message": "Task deleted"}
        return {"error": "Task not found"}, 404

if __name__ == '__main__':
    app.run(debug=True)
    