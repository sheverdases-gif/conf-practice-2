import sys
import os
import unittest
from argparse import Namespace
from unittest.mock import patch

current_dir = os.path.dirname(__file__)
src_path = os.path.abspath(os.path.join(current_dir, '..', 'src'))
sys.path.insert(0, src_path)

from main import validate_arguments


class TestValidateArguments(unittest.TestCase):
    """Тесты для функции validate_arguments."""

    def test_valid_arguments(self):
        """Корректные параметры проходят валидацию."""
        args = Namespace(
            package="express",
            repo="https://registry.npmjs.org/express",
            test_mode=False,
            filter="dev"
        )
        self.assertTrue(validate_arguments(args))

    def test_empty_package(self):
        """Пустое имя пакета — ошибка."""
        args = Namespace(
            package="   ",
            repo="https://registry.npmjs.org/express",
            test_mode=False,
            filter=""
        )
        with patch('builtins.print') as mock_print:
            self.assertFalse(validate_arguments(args))
            mock_print.assert_called_with(
                "Ошибка: Имя пакета не может быть пустым."
            )

    def test_url_in_test_mode(self):
        """URL в режиме тестирования — ошибка."""
        args = Namespace(
            package="express",
            repo="https://registry.npmjs.org/express",
            test_mode=True,
            filter=""
        )
        with patch('builtins.print') as mock_print:
            self.assertFalse(validate_arguments(args))
            mock_print.assert_called_with(
                "Ошибка: В режиме тестирования (--test-mode) "
                "укажите путь к файлу, а не URL."
            )

    def test_no_url_in_normal_mode(self):
        """Локальный путь в обычном режиме — ошибка."""
        args = Namespace(
            package="express",
            repo="./local_file.txt",
            test_mode=False,
            filter=""
        )
        with patch('builtins.print') as mock_print:
            self.assertFalse(validate_arguments(args))
            mock_print.assert_called_with(
                "Ошибка: Укажите корректный URL-адрес репозитория "
                "(начинающийся с http:// или https://)."
            )

    def test_filter_too_long(self):
        """Слишком длинный фильтр — ошибка."""
        args = Namespace(
            package="express",
            repo="https://registry.npmjs.org/express",
            test_mode=False,
            filter="a" * 51
        )
        with patch('builtins.print') as mock_print:
            self.assertFalse(validate_arguments(args))
            mock_print.assert_called_with(
                "Ошибка: Подстрока фильтрации слишком длинная "
                "(максимум 50 символов)."
            )

if __name__ == "__main__":
    unittest.main()