import json
import urllib.request
import urllib.error

DEFAULT_TIMEOUT = 10
HTTP_OK = 200
HTTP_NOT_FOUND = 404


def _fetch_url(full_url: str) -> str:
    """Выполняет GET-запрос и возвращает декодированный
      текст ответа."""
    with urllib.request.urlopen(
        full_url, timeout=DEFAULT_TIMEOUT
    ) as response:
        if response.status != HTTP_OK:
            raise ValueError(
                f"Ошибка сервера: код {response.status}"
            )
        return response.read().decode('utf-8')


def get_package_info(package_name: str, repo_url: str) -> dict:
    """
    Получает информацию о пакете из npm-реестра.
    
    :param package_name: Имя пакета (например, 'express').
    :param repo_url: Базовый URL репозитория.
    :return: Словарь с данными о пакете.
    :raises ValueError: Если пакет не найден или произошла ошибка.
    """
    base_url = repo_url.rstrip('/')
    full_url = f"{base_url}/{package_name}/latest"
    
    try:
    
        data = _fetch_url(full_url)
        return json.loads(data)

    except urllib.error.HTTPError as e:
        if e.code == HTTP_NOT_FOUND:
            raise ValueError(
                f"Пакет '{package_name}' не найден в репозитории."
            )
        raise ValueError(f"Ошибка HTTP: {e.code} - {e.reason}")
    except urllib.error.URLError as e:
        raise ValueError(
            f"Ошибка сети: не удалось подключиться к {full_url}. "
            f"({e.reason})"
        )
    except json.JSONDecodeError:
        raise ValueError(
            "Ошибка: полученный ответ не является корректным JSON."
        )


def extract_dependencies(package_info: dict) -> list:
    """
    Извлекает список прямых зависимостей из информации о пакете.
    
    :param package_info: Словарь с данными о пакете.
    :return: Отсортированный список имен зависимостей.
    """
    deps = package_info.get("dependencies", {})
    
    if not isinstance(deps, dict):
        return []
        
    return sorted(deps.keys())