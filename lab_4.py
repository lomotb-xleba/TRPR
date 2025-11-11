import sqlite3

def main():
    try:
        # Подключение к базе данных
        conn = sqlite3.connect('company_data.db')
        cursor = conn.cursor()
        print("Успешное подключение к базе данных")

        # Создание целевой таблицы если не существует
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS project_finance_status (
                project_id INTEGER PRIMARY KEY,
                project_name TEXT NOT NULL,
                budget REAL NOT NULL,
                spent REAL NOT NULL,
                utilization_percent REAL NOT NULL,
                status TEXT NOT NULL
            )
        ''')

        # Извлечение данных из исходной таблицы
        cursor.execute('''
            SELECT project_id, project_name, budget, spent 
            FROM Projects
        ''')
        projects = cursor.fetchall()
        print(f"Обработано записей: {len(projects)}")

        # Обработка данных
        results = []
        for project in projects:
            project_id, project_name, budget, spent = project
            
            # Расчет процента освоения бюджета
            utilization_percent = (spent / budget) * 100 if budget > 0 else 0
            
            # Определение статуса
            status = "Рисковые" if utilization_percent > 90 else "Стабильные"
            
            results.append((
                project_id,
                project_name,
                budget,
                spent,
                round(utilization_percent, 2),
                status
            ))

        # Запись результатов в целевую таблицу
        cursor.executemany('''
            INSERT OR REPLACE INTO project_finance_status
            (project_id, project_name, budget, spent, utilization_percent, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', results)

        conn.commit()
        print("Данные успешно записаны в таблицу project_finance_status")

    except sqlite3.Error as e:
        print(f"Ошибка базы данных: {e}")
    finally:
        if conn:
            conn.close()
            print("Соединение с базой данных закрыто")

if __name__ == "__main__":
    main()