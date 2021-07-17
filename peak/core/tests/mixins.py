class AddressTestMixin:
    """
    Заполнение тестовой базы адресов небольшими фикстурами.
    """
    fixtures = [
        'fixtures/countries.json',
        'fixtures/regions.json',
        'fixtures/cities.json',
    ]
