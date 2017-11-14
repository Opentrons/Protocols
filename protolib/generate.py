import random
from faker import Factory
from slugify import slugify


fake = Factory.create()


def time_estimate():
    return '{} hours {} minutes'.format(
        random.randint(2, 5),
        random.randint(2, 59)
    )


def generate_deck():
    return {}


schema = {
    'slug': None,
    'source-url': None,
    'github-url': None,
    'author': fake.name,
    'partner': fake.company,
    'deck': generate_deck,
    'categories': (
        [
            'Molecular-Biology',
            'Cell-Biology',
            'Tissue-Culture',
            'DNA-Analysis',
        ], 2),
    'subcategories': ([
        'PCR',
        'FusX',
        'ELISA',
        'Dilutions',
        'DNA-Extraction'],
        2),
    'description': fake.text,
    'time-estimate': time_estimate,
    'robot': (['OT Pro', 'OT Hood'], 2),
    'modules': (['MagDeck', 'Gripper'], 2),
    'reagents': ([
        {
            'name': 'enzymeA',
            'url': 'http://example.com/a'
        },
        {
            'name': 'enzymeB',
            'url': 'http://example.com/b'
        },
        {
            'name': 'enzymeC',
            'url': 'http://example.com/c'
        },
        {
            'name': 'enzymeD',
            'url': 'http://example.com/d'
        }
    ], 2),
    'process': fake.text,
    'notes': fake.text
}


def generate_field(field):
    value = schema[field]
    if isinstance(value, tuple):
        return random.sample(*value)

    if hasattr(value, '__call__'):
        return value()

    return value


def generate(count):
    for _ in range(count):
        title = fake.sentence(nb_words=3)
        slug = slugify(title)
        github = 'https://github.com/opentrons/protocols/{}'.format(
            slug
        )

        head = {
            'title': title,
            'slug': slug,
            'source-url': github + '/protocol.py',
            'github-url': github
        }

        tail = {
            field: generate_field(field)
            for field in schema.keys() - head.keys()
        }

        yield {**head, **tail}
