from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, Date
from datetime import datetime, timedelta


Base = declarative_base()


class ToDoTask(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, nullable=False)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.string_field


engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def print_tasks(date, weekday=False):
    first_word = "Today"
    if weekday:
        first_word = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][date.weekday()]
    print(f"{first_word} {date.day} {date.strftime('%b')}:")
    rows = session.query(ToDoTask) \
        .filter(ToDoTask.deadline == date) \
        .order_by(ToDoTask.deadline) \
        .all()
    if len(rows) > 0:
        row_number = 1
        for row in rows:
            print(f'{row_number}. {row.task}')
            row_number += 1
    else:
        print('Nothing to do!')


while True:
    print("1) Today's tasks")
    print("2) Week's tasks")
    print('3) All tasks')
    print('4) Missed tasks')
    print('5) Add task')
    print('6) Delete task')
    print('0) Exit')

    command = input('> ')
    print()

    if command == '1':
        print_tasks(datetime.now().date())
    elif command == '2':
        current_date = datetime.now().date()
        current_day_of_week = current_date.weekday()
        for it in range(7):
            day = current_date + timedelta(days=it)
            print_tasks(day, weekday=True)
            print()
    elif command == '3':
        print('All tasks:')
        rows = session.query(ToDoTask) \
            .order_by(ToDoTask.deadline) \
            .all()
        if len(rows) > 0:
            row_number = 1
            for row in rows:
                print(f"{row_number}. {row.task}. {row.deadline.day} {row.deadline.strftime('%b')}")
                row_number += 1
        else:
            print('Nothing to do!')
    elif command == '4':
        print('Missed tasks:')
        rows = session.query(ToDoTask) \
            .filter(ToDoTask.deadline < datetime.now().date()) \
            .order_by(ToDoTask.deadline) \
            .all()
        if len(rows) > 0:
            row_number = 1
            for row in rows:
                print(f"{row_number}. {row.task}. {row.deadline.day} {row.deadline.strftime('%b')}")
                row_number += 1
        else:
            print('Nothing is missed!')
    elif command == '5':
        print('Enter task')
        new_task = input('> ')
        print('Enter deadline')
        new_deadline = input('> ')
        new_task = ToDoTask(task=new_task, deadline=datetime.fromisoformat(new_deadline))
        session.add(new_task)
        session.commit()
        print('The task has been added!')
    elif command == '6':
        print('Choose the number of the task you want to delete:')
        rows = session.query(ToDoTask) \
            .order_by(ToDoTask.deadline) \
            .all()
        if len(rows) > 0:
            row_number = 1
            for row in rows:
                print(f"{row_number}. {row.task}. {row.deadline.day} {row.deadline.strftime('%b')}")
                row_number += 1
            to_delete = int(input('> '))
            session.query(ToDoTask).filter(ToDoTask.id == rows[to_delete - 1].id).delete()
            session.commit()
        else:
            print('Nothing to delete!')
    elif command == '0':
        print('Bye!')
        break

    print()
