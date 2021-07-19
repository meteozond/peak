import random

from factory import Factory

from django.contrib.gis.geos import Polygon


def get_factory_data(factory: Factory) -> dict:
    """
    Возвращает словарь со сгенерированными значениями полей из Factory не сохраняя в БД.
    """
    data = factory.build().__dict__
    for key in list(data.keys()):
        if 'id' in key or key.startswith('_'):
            del data[key]
    return data


def generate_phone_number() -> str:
    """
    Возвращает номер в международном формате.
    """
    return '+' + str(random.randrange(7_981_000_00_00, 7_981_999_99_99))


def generate_polygon(size: int = 5) -> Polygon:
    """
    Генерирует полигон.

    :param size: количество координат
    """
    poly = [
        [random.randrange(1, 100), random.randrange(1, 100)] for _ in range(1, size)
    ]
    poly.append(poly[0])
    return Polygon(poly)
