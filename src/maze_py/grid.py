"""
Основные доменные модели для генерации и решения лабиринтов.
Содержит фундаментальные структуры данных для представления лабиринта.
"""

from __future__ import annotations  # Для отложенных аннотаций типов

from dataclasses import dataclass, field
from typing import Iterable, Iterator, List, Sequence, Tuple


# Тип для представления смещений к соседям
Neighbors = Tuple[int, int]


@dataclass(slots=True)  # Используем slots для оптимизации памяти
class Cell:
    """
    Представляет одну клетку лабиринта.
    
    Клетка может иметь связи (проходы) с ортогональными соседями.
    Также поддерживает структуру дерева для хранения путей.
    
    Атрибуты:
        x, y: Координаты клетки в сетке
        links: Словарь связанных соседей и весов связей
        parent: Родительская клетка в дереве обхода
        children: Дочерние клетки в дереве обхода
        _depth_cache: Кэшированная глубина в дереве
    """

    x: int
    y: int
    links: dict["Cell", int] = field(default_factory=dict)  # Граф связей
    parent: "Cell | None" = None  # Для построения деревьев
    children: List["Cell"] = field(default_factory=list)  # Для иерархии
    _depth_cache: int | None = field(default=None, init=False, repr=False)  # Оптимизация

    @property
    def coords(self) -> Tuple[int, int]:
        """Возвращает координаты клетки в виде кортежа (x, y)."""
        return self.x, self.y

    def depth(self) -> int:
        """
        Вычисляет глубину клетки в дереве (расстояние от корня).
        
        Использует мемоизацию для оптимизации повторных вычислений.
        """
        if self._depth_cache is not None:
            return self._depth_cache
        
        # Если нет родителя, это корневая клетка (глубина 0)
        if not self.parent:
            self._depth_cache = 0
        else:
            # Глубина = глубина родителя + 1
            self._depth_cache = self.parent.depth() + 1
        
        return self._depth_cache

    def link(self, other: "Cell", weight: int = 1) -> None:
        """
        Создает двустороннюю связь между текущей клеткой и соседом.
        
        Args:
            other: Клетка для связи
            weight: Вес связи (может использоваться для взвешенных графов)
        """
        self.links[other] = weight
        other.links[self] = weight

    def unlink(self, other: "Cell") -> None:
        """Удаляет связь между двумя клетками."""
        self.links.pop(other, None)
        other.links.pop(self, None)

    def reset_links(self) -> None:
        """
        Полностью сбрасывает все связи и информацию о дереве.
        
        Используется при перегенерации лабиринта.
        """
        # Удаляем ссылки на текущую клетку у всех соседей
        for neighbor in list(self.links.keys()):
            neighbor.links.pop(self, None)
        
        # Очищаем все атрибуты
        self.links.clear()
        self.parent = None
        self.children.clear()
        self._depth_cache = None

    def __hash__(self) -> int:
        """
        Определяет хэш-функцию для использования Cell как ключа словаря.
        
        Хэшируем по координатам, так как они уникальны для каждой клетки.
        """
        return hash((self.x, self.y))

    def __eq__(self, other: object) -> bool:
        """Сравнивает две клетки по координатам."""
        if not isinstance(other, Cell):
            return NotImplemented
        return (self.x, self.y) == (other.x, other.y)


class MazeGrid:
    """
    2D сетка клеток, представляющая лабиринт.
    
    Реализует логику работы с сеткой: доступ к клеткам,
    поиск соседей, управление связями.
    """

    def __init__(self, width: int, height: int):
        """Инициализирует сетку заданного размера."""
        if width <= 0 or height <= 0:
            raise ValueError("Размеры лабиринта должны быть положительными целыми числами.")
        
        self.width = int(width)
        self.height = int(height)
        
        # Создаем двумерный список клеток
        # Обратите внимание: первый индекс - x (столбец), второй - y (строка)
        self._cells: List[List[Cell]] = [
            [Cell(x, y) for y in range(self.height)]
            for x in range(self.width)
        ]

    def __iter__(self) -> Iterator[Cell]:
        """
        Итератор по всем клеткам сетки.
        
        Позволяет использовать: for cell in grid: ...
        """
        for column in self._cells:
            yield from column  # Генератор для эффективности

    def contains(self, x: int, y: int) -> bool:
        """Проверяет, находятся ли координаты в пределах сетки."""
        return 0 <= x < self.width and 0 <= y < self.height

    def cell(self, x: int, y: int) -> Cell:
        """
        Возвращает клетку по координатам.
        
        Raises:
            IndexError: Если координаты вне границ сетки.
        """
        if not self.contains(x, y):
            raise IndexError(f"Клетка ({x}, {y}) выходит за границы лабиринта.")
        return self._cells[x][y]

    def neighbor_coords(self, cell: Cell) -> Iterable[Tuple[int, int]]:
        """
        Генерирует координаты всех ортогональных соседей клетки.
        
        Ортогональные соседи: вверх, вниз, влево, вправо.
        Диагональные соседи не учитываются в стандартном лабиринте.
        """
        # Смещения для ортогональных соседей
        offsets: Sequence[Neighbors] = ((1, 0), (-1, 0), (0, 1), (0, -1))
        
        for dx, dy in offsets:
            nx, ny = cell.x + dx, cell.y + dy
            if self.contains(nx, ny):
                yield nx, ny

    def neighbors(self, cell: Cell) -> Iterable[Cell]:
        """Генерирует объекты всех ортогональных соседей клетки."""
        for x, y in self.neighbor_coords(cell):
            yield self.cell(x, y)

    def link(self, a: Cell, b: Cell, weight: int = 1) -> None:
        """Создает связь между двумя клетками (прокладывает проход)."""
        a.link(b, weight)

    def reset(self) -> None:
        """Сбрасывает все связи в лабиринте."""
        for cell in self:
            cell.reset_links()


@dataclass(slots=True)
class MazeTree:
    """
    Результат генерации остовного дерева над сеткой.
    
    Представляет лабиринт как дерево с корнем и порядком посещения.
    Это эффективная структура для хранения сгенерированных лабиринтов.
    """

    grid: MazeGrid  # Исходная сетка
    root: Cell  # Корневая клетка (вход в лабиринт)
    visit_order: List[Cell]  # Порядок, в котором клетки были посещены при генерации

    def path_to(self, target: Cell) -> List[Cell]:
        """
        Восстанавливает путь от корня к целевой клетке.
        
        Использует цепочку родительских ссылок, установленных при генерации.
        
        Returns:
            Список клеток от корня к цели (включительно).
        """
        path: List[Cell] = []
        cursor: Cell | None = target
        
        # Идем от цели к корню по родительским ссылкам
        while cursor:
            path.append(cursor)
            cursor = cursor.parent
        
        # Переворачиваем, чтобы получить путь от корня к цели
        return list(reversed(path))

