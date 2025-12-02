"""
Модуль BFS-решателя лабиринтов.
Алгоритм поиска в ширину (Breadth-First Search) для нахождения кратчайшего пути в лабиринте.
"""

from __future__ import annotations  # Для отложенных аннотаций типов

from collections import deque  # Используем deque для эффективной работы с очередью
from typing import Deque, Dict, List, Tuple

from ..animation import AnimationRecorder
from ..grid import Cell, MazeTree
from .base import MazeSolver


class BreadthFirstSolver(MazeSolver):
    """
    Реализация алгоритма поиска в ширину (BFS) для решения лабиринтов.
    
    Ключевые особенности BFS:
    1. Находит кратчайший путь (по количеству шагов) в невзвешенном графе
    2. Использует очередь (FIFO - First In, First Out)
    3. Идеально подходит для лабиринтов с одинаковой стоимостью перемещения
    """
    
    name = "bfs"  # Идентификатор алгоритма

    def _traverse(
        self,
        tree: MazeTree,
        target: Tuple[int, int],
        *,
        recorder: AnimationRecorder | None = None,
    ) -> Tuple[List[Cell], List[Cell]]:
        """
        Основной метод обхода лабиринта с использованием BFS.
        
        Args:
            tree: Дерево лабиринта с корневой клеткой
            target: Координаты целевой клетки (x, y)
            recorder: Опциональный рекордер для анимации процесса
            
        Returns:
            Кортеж из (путь к цели, список всех исследованных клеток)
        """
        
        # 1. ИНИЦИАЛИЗАЦИЯ
        # Получаем объект целевой клетки по координатам
        target_cell = tree.grid.cell(*target)
        
        # Создаем очередь для BFS. Используем deque для эффективных операций popleft()
        # Начинаем с корневой клетки (входа в лабиринт)
        queue: Deque[Cell] = deque([tree.root])
        
        # Словарь для хранения родительских связей: клетка → её родитель
        # Это позволяет восстановить путь от цели к старту
        parents: Dict[Cell, Cell | None] = {tree.root: None}
        
        # Список для отслеживания порядка исследования клеток (для визуализации)
        explored: List[Cell] = []

        # 2. ОСНОВНОЙ ЦИКЛ BFS
        # Продолжаем, пока есть клетки для исследования
        while queue:
            # Извлекаем первую клетку из очереди (FIFO)
            # Это ключевое отличие BFS от DFS (который использует стек)
            cell = queue.popleft()
            
            # Добавляем клетку в список исследованных
            explored.append(cell)
            
            # Если включена запись анимации, фиксируем текущее состояние
            if recorder:
                recorder.record(
                    "solve",
                    "explore",
                    cell=list(cell.coords),
                    parent=list(parents[cell].coords) if parents[cell] else None,
                )
            
            # 3. ПРОВЕРКА ЦЕЛИ
            # Если достигли целевой клетки, завершаем поиск
            # В BFS это гарантированно будет кратчайший путь
            if cell is target_cell:
                break
            
            # 4. ИССЛЕДОВАНИЕ СОСЕДЕЙ
            # Проходим по всем связанным соседям текущей клетки
            # В контексте лабиринта - это проходы без стен
            for neighbor in cell.links:
                # Пропускаем уже посещенных соседей (они уже есть в словаре parents)
                if neighbor in parents:
                    continue
                
                # Запоминаем родителя для соседа (текущую клетку)
                parents[neighbor] = cell
                
                # Добавляем соседа в конец очереди для дальнейшего исследования
                queue.append(neighbor)

        # 5. ВОССТАНОВЛЕНИЕ ПУТИ
        # Строим путь от цели к старту, используя словарь родителей
        path = self._build_path(parents, target_cell)
        
        # Записываем финальный путь для анимации
        if path and recorder:
            recorder.record(
                "solve",
                "path",
                cells=[list(step.coords) for step in path],
            )
        
        return path, explored