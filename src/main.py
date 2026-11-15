import argparse
import sys
from npm_parser import get_package_info, extract_dependencies
from graph_builder import (
    load_test_graph,
    get_mock_dependencies,
    build_dependency_graph,
)

MAX_FILTER_LEN = 50


def _add_arguments(parser: argparse.ArgumentParser) -> None:
    """Добавляет все аргументы в парсер."""
    parser.add_argument(
        "--package", "-p", type=str, required=True,
        help="Имя анализируемого пакета (например: express)."
    )
    parser.add_argument(
        "--repo", "-r", type=str, required=True,
        help="URL-адрес репозитория или путь к файлу "
             "тестового репозитория."
    )
    parser.add_argument(
        "--test-mode", "-t", action="store_true",
        help="Включить режим тестирования (локальный файл вместо URL)."
    )
    parser.add_argument(
        "--filter", "-f", type=str, default="",
        help="Подстрока для фильтрации пакетов (например, 'dev')."
    )


def parse_arguments() -> argparse.Namespace:
    """Парсит аргументы командной строки."""
    parser = argparse.ArgumentParser(
        description="Инструмент визуализации графа зависимостей "
                    "(Этап 3).",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    _add_arguments(parser)
    return parser.parse_args()


def validate_arguments(args: argparse.Namespace) -> bool:
    """Проверяет корректность введенных параметров."""
    is_valid = True
    if not args.package.strip():
        print("Ошибка: Имя пакета не может быть пустым.")
        is_valid = False

    if args.test_mode:
        if args.repo.startswith("http"):
            print("Ошибка: В режиме тестирования (--test-mode) "
                  "укажите путь к файлу, а не URL.")
            is_valid = False
    else:
        if not args.repo.startswith("http"):
            print("Ошибка: Укажите корректный URL-адрес репозитория "
                  "(начинающийся с http:// или https://).")
            is_valid = False

    if len(args.filter) > MAX_FILTER_LEN:
        print(f"Ошибка: Подстрока фильтрации слишком длинная "
              f"(максимум {MAX_FILTER_LEN} символов).")
        is_valid = False
    return is_valid


def print_configuration(args: argparse.Namespace) -> None:
    """Выводит все параметры в формате ключ: значение."""
    print("--- Конфигурация эмулятора ---")
    print(f"package: {args.package}")
    print(f"repo: {args.repo}")
    print(f"test_mode: {args.test_mode}")
    print(f"filter: {args.filter}")


def get_real_deps_wrapper(pkg_name: str, repo_url: str) -> callable:
    """Создает функцию для получения реальных зависимостей (npm)."""
    def fetch(pkg: str) -> list:
        info = get_package_info(pkg, repo_url)
        return extract_dependencies(info)
    return fetch


def main() -> None:
    """Главная функция приложения."""
    print("Запуск инструмента визуализации графа зависимостей "
          "(Этап 3)...")

    args = parse_arguments()
    if not validate_arguments(args):
        sys.exit(1)

    print_configuration(args)
    print()

    result_graph = {}
    current_path = set()

    try:
        if args.test_mode:
            print(f"Загрузка тестового графа из {args.repo}...")
            mock_data = load_test_graph(args.repo)
            
            def fetch_mock(pkg: str) -> list:
                return get_mock_dependencies(pkg, mock_data)
                
            build_dependency_graph(
                args.package, fetch_mock, args.filter,
                current_path, result_graph
            )
        else:
            print(f"Построение графа для пакета '{args.package}'...")
            fetch_real = get_real_deps_wrapper(args.package, args.repo)
            build_dependency_graph(
                args.package, fetch_real, args.filter,
                current_path, result_graph
            )

        print("\n--- Построенный граф зависимостей ---")
        for pkg, deps in result_graph.items():
            deps_str = ", ".join(deps) if deps else "нет"
            print(f"{pkg} -> {deps_str}")

    except ValueError as e:
        print(f"\nОшибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()