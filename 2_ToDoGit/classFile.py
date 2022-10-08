from datetime import datetime

class TaskList:
    def __init__(self, tasks=[]):
        self.tasks = tasks

    def __repr__(self):
        str = "[\n"
        for task in self.tasks:
            str = str +  repr(task) +',\n'
        str += ']'
        return str

    def addTask(self, task):
        self.tasks.append(task)

class Task:
    def __init__(self, date=datetime.today(), course='', description=''):
        self.date = datetime.date(date)
        self.course = course
        self.description = description

    def __repr__(self):
        return f'{self.date}\t{self.course}\t{self.description}'


def main():
    tl = TaskList()
    T = Task(datetime.today(), "AAR", "oefenen")
    tl.addTask(T)
    print(T)
    print(tl)

if __name__ == "__main__":
    main()

