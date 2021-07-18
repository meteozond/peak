import random

from factory import Factory


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
