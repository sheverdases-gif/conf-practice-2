"""Модуль для построения графа зависимостей с помощью DFS."""

import json


def load_test_graph(file_path: str) -> dict:
    """Загружает граф из локального JSON-файла."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise ValueError(
            f"Файл тестового репозитория не найден: {file_path}"
        )
    except json.JSONDecodeError:
        raise ValueError(
            "Ошибка: тестовый файл содержит некорректный JSON."
        )


def get_mock_dependencies(package_name: str, mock_data: dict) -> list:
    """Возвращает прямые зависимости из тестового словаря."""
    return mock_data.get(package_name, [])


def build_dependency_graph(
    package_name: str,
    fetch_deps_func,
    filter_str: str,
    current_path: set,
    result_graph: dict
) -> None:
    """
    Рекурсивно обходит граф зависимостей (DFS).
    Записывает результат в result_graph.
    Обрабатывает циклы с помощью current_path.
    Учитывает фильтр при формировании списка зависимостей.
    """
    if package_name in current_path:
        return
        
    if filter_str and filter_str in package_name:
        return

    current_path.add(package_name)

    try:
        deps = fetch_deps_func(package_name)
    except ValueError:
        deps = []

    if package_name not in result_graph:
        filtered_deps = []
        for dep in deps:
            if dep not in current_path:
                if not (filter_str and filter_str in dep):
                    filtered_deps.append(dep)
        result_graph[package_name] = filtered_deps

    for dep in deps:
        build_dependency_graph(
            dep,
            fetch_deps_func,
            filter_str,
            current_path,
            result_graph
        )

    current_path.remove(package_name)