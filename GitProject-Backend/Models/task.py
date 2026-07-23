class Task():
    task_id :int
    task_name :str
    task_condition :str
    task_completion :bool

    def __init__(self, _id :int, name :str, condition :str, dead_line :str):
        self.task_id = _id
        self.task_name = name
        self.task_condition = condition
        self.task_completion :bool = False
        self.dead_line :str = dead_line

