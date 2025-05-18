import ollama
import os
from pathlib import Path


def get_code_from_project(project_path, extensions=(".py", ".txt", ".md")):
    """Собирает код из всех файлов проекта."""
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


if __name__ == "__main__":
    project_path = "C:/Users/matve/PycharmProjects/urfu-fresh-scanner"  # Укажите свой путь
    code = get_code_from_project(project_path)

    if not code:
        print("Не найдено файлов для анализа.")
        exit()

    # Формируем запрос (можно менять под свои нужды)
    prompt = f"""
    Вот код проекта:
    {code}

    Задачи:
    Напиши CI-CD пайплайн.
    Отвечай на русском.
    """

    print("Анализирую код...\n")
    analysis_result = analyze_with_ollama(prompt)
    print(analysis_result)