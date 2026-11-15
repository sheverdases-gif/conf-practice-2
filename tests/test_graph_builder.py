import sys
import os
import unittest

current_dir = os.path.dirname(__file__)
src_path = os.path.abspath(os.path.join(current_dir, '..', 'src'))
sys.path.insert(0, src_path)

from graph_builder import build_dependency_graph


def mock_fetch(pkg: str) -> list:
    """Фейковая функция получения зависимостей для тестов."""
    data = {
        "A": ["B", "C"],
        "B": ["D"],
        "C": ["A", "E"],
        "D": ["B"],
        "E": []
    }
    return data.get(pkg, [])


class TestGraphBuilder(unittest.TestCase):
    """Тесты для алгоритма DFS."""

    def test_cycle_handling(self):
        """Тест: алгоритм не зависает на цикле A -> C -> A."""
        graph = {}
        current_path = set()
        build_dependency_graph(
            "A", mock_fetch, "", current_path, graph
        )
        self.assertIn("A", graph)
        self.assertIn("C", graph)
        self.assertIn("E", graph)

    def test_filter_ignore(self):
        """Тест: пакеты с подстрокой 'D' игнорируются."""
        graph = {}
        current_path = set()
        build_dependency_graph(
            "A", mock_fetch, "D", current_path, graph
        )
        self.assertNotIn("D", graph)
        self.assertIn("B", graph)
        self.assertIn("C", graph)


if __name__ == "__main__":
    unittest.main()