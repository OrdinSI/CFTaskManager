from tortoise import Tortoise, run_async

from src.db.models.task import Subject
from src.settings import TORTOISE_ORM


async def init():
    """ Initialize collection of model Subject. """
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas(safe=True)

    subject = [
        Subject(tag="math", name="Математика"),
        Subject(tag="greedy", name="Жадные алгоритмы"),
        Subject(tag="implementation", name="Реализация"),
        Subject(tag="dp", name="Динамическое программирование"),
        Subject(tag="constructive algorithms", name="Конструктивные алгоритмы"),
        Subject(tag="data structures", name="Структуры данных"),
        Subject(tag="brute force", name="Перебор"),
        Subject(tag="sortings", name="Сортировка"),
        Subject(tag="graphs", name="Графы"),
        Subject(tag="binary search", name="Бинарный поиск"),
        Subject(tag="dfs and similar", name="Глубокий поисковый обход (DFS) и подобные"),
        Subject(tag="trees", name="Деревья"),
        Subject(tag="number theory", name="Теория чисел"),
        Subject(tag="strings", name="Строки"),
        Subject(tag="combinatorics", name="Комбинаторика"),
        Subject(tag="bitmasks", name="Битовые маски"),
        Subject(tag="two pointers", name="Два указателя"),
        Subject(tag="special", name="Специальные задачи"),
        Subject(tag="geometry", name="Геометрия"),
        Subject(tag="dsu", name="Система непересекающихся множеств (DSU)"),
        Subject(tag="divide and conquer", name="Разделяй и властвуй"),
        Subject(tag="shortest paths", name="Кратчайшие пути"),
        Subject(tag="probabilities", name="Вероятности"),
        Subject(tag="interactive", name="Интерактивные задачи"),
        Subject(tag="games", name="Игры"),
        Subject(tag="hashing", name="Хэши"),
        Subject(tag="flows", name="Потоки"),
        Subject(tag="matrices", name="Матрицы"),
        Subject(tag="fft", name="Быстрое преобразование Фурье (FFT)"),
        Subject(tag="string suffix structures", name="Суффиксные структуры строк"),
        Subject(tag="graph matchings", name="Сопоставления в графах"),
        Subject(tag="ternary search", name="Тернарный поиск"),
        Subject(tag="meet-in-the-middle", name="Встреча в середине (Meet-in-the-Middle)"),
        Subject(tag="expression parsing", name="Разбор выражений"),
        Subject(tag="2-sat", name="2-SAT задача"),
        Subject(tag="chinese remainder theorem", name="Китайская теорема об остатках (CRT)"),
        Subject(tag="schedules", name="Расписания")
    ]

    await Subject.bulk_create(subject)

    await Tortoise.close_connections()


if __name__ == "__main__":
    run_async(init())
