import sqlite3
from datetime import date, timedelta
import random

def create_database():
    conn = sqlite3.connect('company_data.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Projects (
            project_id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_name TEXT NOT NULL,
            manager TEXT NOT NULL,
            budget REAL NOT NULL,
            spent REAL NOT NULL,
            deadline DATE NOT NULL
        )
    ''')
    
    # Генерация тестовых данных
    projects = []
    managers = ['Иван Петров', 'Мария Сидорова', 'Алексей Козлов', 
                'Елена Новикова', 'Дмитрий Воробьев', 'Ольга Соколова']
    
    start_date = date(2024, 1, 1)
    for i in range(1, 101):
        project_name = f"Проект {i}"
        manager = random.choice(managers)
        budget = round(random.uniform(50000, 500000), 2)
        spent = round(random.uniform(0, budget * 1.2), 2)  # Иногда превышаем бюджет
        deadline = start_date + timedelta(days=random.randint(30, 365))
        
        projects.append((project_name, manager, budget, spent, deadline))
    
    cursor.executemany('''
        INSERT INTO Projects (project_name, manager, budget, spent, deadline)
        VALUES (?, ?, ?, ?, ?)
    ''', projects)
    
    conn.commit()
    conn.close()
    print("База данных company_data.db и таблица Projects успешно созданы!")

if __name__ == "__main__":
    create_database()