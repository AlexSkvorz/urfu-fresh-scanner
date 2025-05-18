import ollama
import os
import subprocess
from pathlib import Path
from time import sleep

def get_code_from_project(project_path, extensions=(".py", ".txt", ".md", ".yaml", ".yml", "Dockerfile", "docker-compose.yml")):
    """Собирает код из всех файлов проекта, включая Docker-конфиги."""
    code_content = []
    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith(extensions):
                file_path = Path(root) / file
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        code_content.append(f"=== Файл: {file} ===\n{content}\n")
                except Exception as e:
                    print(f"Ошибка чтения {file_path}: {e}")
    return "\n".join(code_content)

def analyze_with_ollama(prompt, model="llama3"):
    """Отправляет запрос в Ollama и получает ответ."""
    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return response["message"]["content"]

def deploy_with_docker():
    """Запускает сборку и деплой через docker-compose."""
    try:
        # Сборка образов
        subprocess.run(["docker-compose", "build"], check=True)
        # Запуск контейнеров
        subprocess.run(["docker-compose", "up", "-d"], check=True)
        print("✅ Деплой через Docker Compose завершён.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка деплоя: {e}")
        return False

def check_container_health():
    """Проверяет здоровье контейнера через docker inspect."""
    try:
        result = subprocess.run(
            ["docker", "inspect", "--format='{{.State.Health.Status}}'", "urfu-fresh-scanner-FreshScannerBot-1"],
            capture_output=True, text=True
        )
        status = result.stdout.strip("'\n")
        return status == "healthy"
    except Exception as e:
        print(f"⚠️ Ошибка проверки здоровья: {e}")
        return False

def rollback_docker():
    """Откатывает деплой: останавливает контейнеры и удаляет образы."""
    print("🔄 Откатываю деплой...")
    subprocess.run(["docker-compose", "down", "--rmi", "all"])

if __name__ == "__main__":
    project_path = "C:/Users/matve/PycharmProjects/urfu-fresh-scanner"
    code = get_code_from_project(project_path)

    if not code:
        print("Не найдено файлов для анализа.")
        exit()

    # 1. Анализ проекта
    prompt = f"""
    Вот код проекта (включая Docker-конфиги):
    {code}

    Задачи:
    1. Проверь, что Dockerfile и docker-compose.yml корректны.
    2. Предложи команды для ручного деплоя (docker-compose up -d).
    3. Как можно улучшить конфигурацию для self-healing?
    Отвечай ТОЛЬКО на русском.
    """
    print("Анализирую код...\n")
    analysis_result = analyze_with_ollama(prompt)
    print(analysis_result)

    # 2. Деплой
    if input("Запустить деплой через Docker? (y/n): ").lower() == "y":
        print("🚀 Запускаю деплой...")
        if deploy_with_docker():
            # 3. Self-healing: проверка здоровья
            sleep(10)  # Ждём инициализации контейнеров
            if not check_container_health():
                rollback_docker()
                print("🔴 Self-healing: деплой откачен из-за ошибки.")
            else:
                print("🟢 Self-healing: контейнер работает нормально.")