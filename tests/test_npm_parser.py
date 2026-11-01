import sys
import os
import unittest

current_dir = os.path.dirname(__file__)
src_path = os.path.abspath(os.path.join(current_dir, '..', 'src'))
sys.path.insert(0, src_path)

from npm_parser import extract_dependencies


class TestExtractDependencies(unittest.TestCase):
    """Тесты для функции извлечения зависимостей."""

    def test_empty_dependencies(self):
        """Если поля dependencies нет, возвращается пустой список."""
        package_info = {"name": "test-package"}
        self.assertEqual(extract_dependencies(package_info), [])

    def test_sorted_dependencies(self):
        """Зависимости возвращаются отсортированными по алфавиту."""
        package_info = {
            "dependencies": {
                "zlib": "^1.0.0",
                "axios": "^0.21.0",
                "express": "^4.17.1"
            }
        }
        expected = ["axios", "express", "zlib"]
        self.assertEqual(extract_dependencies(package_info), expected)

    def test_wrong_type(self):
        """Если dependencies не словарь, возвращается пустой список."""
        package_info = {"dependencies": ["not", "a", "dict"]}
        self.assertEqual(extract_dependencies(package_info), [])


if __name__ == "__main__":
    unittest.main()