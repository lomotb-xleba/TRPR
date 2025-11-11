import sqlite3
conn = sqlite3.connect('company_data.db')
cursor = conn.cursor()


cursor.execute("SELECT * FROM project_finance_status WHERE status = 'Рисковые';")
risky_projects = cursor.fetchall()
        
if risky_projects:
    print("РИСКОВЫЕ ПРОЕКТЫ:")
    print(f"{'ID':<4} {'Название проекта':<20} {'Бюджет':<12} {'Потрачено':<12} {'% освоения':<12} {'Статус':<10}")
    print("-"*80)
    
    for project in risky_projects:
        project_id, project_name, budget, spent, utilization_percent, status = project
        print(f"{project_id:<4} {project_name:<20} {budget:<12.2f} {spent:<12.2f} {utilization_percent:<12} {status:<10}")
else:
    print("Рисковые проекты не найдены")