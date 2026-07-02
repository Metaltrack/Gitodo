class Task():
    task_id :int
    task_name :str
    task_condition :str
    task_completion :bool

    def __init__(self, _id :int, name :str, condition :str):
        self.task_id = _id
        self.task_name = name
        self.task_condition = condition
        self.task_completion :bool

    def set_completion(self, state :bool):
        self.task_completion = state

    def set_name(self, name :str):
        self.task_name = name

    def set_condition(self, condition :str):
        self.task_condition = condition
