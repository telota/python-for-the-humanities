#!/usr/bin/env python3

from collections import defaultdict, OrderedDict
from operator import itemgetter
from pathlib import Path
from typing import Dict, List

from markdown import Markdown


PROJECT_DIR = Path(__file__).parent
ITEMS_DIR = PROJECT_DIR / 'items'
TARGET_FILE = PROJECT_DIR / 'docs' / 'index.md'

PROLOGUE = """
# Python for the Humanities

Lorem ipsum motivationales

For a list of general recommendations on Python libraries check out
[Awesome Python](https://awesome-python.com/).

""".lstrip()

ITEM_HEADING_AND_SHIELDS = """
#### {name}

![license](https://img.shields.io/pypi/l/{name}.svg)
![version](https://img.shields.io/pypi/v/{name}.svg)
![pyversions](https://img.shields.io/pypi/pyversions/{name}.svg)
![maturity](https://img.shields.io/pypi/status/{name}.svg)
""".lstrip()

ITEM_GITHUB_SHIELDS = """
![stars](https://img.shields.io/github/stars/{github_repo}.svg)
![contributors](https://img.shields.io/github/contributors/{github_repo}.svg)
![forks](https://img.shields.io/github/forks/{github_repo}.svg)
""".lstrip()


markdown_parser = Markdown(extensions=['markdown.extensions.meta'])


def read_sections() -> OrderedDict:
    sections = {}
    for section in ITEMS_DIR.iterdir():
        sections[section.name] = read_subsections(section)
    return OrderedDict(sorted(sections.items(), key=itemgetter(0)))


def read_subsections(section: Path) -> OrderedDict:
    subsections = {}
    for subsection in section.iterdir():
        subsections[subsection.name] = read_items(subsection)
    return OrderedDict(sorted(subsections.items(), key=itemgetter(0)))


def read_items(subsection: Path) -> List[Dict]:
    items = []
    for item_file in subsection.glob('*.md'):
        with open(item_file, 'rt') as f:
            text = f.read()
        item = {k: None for k in ('github_repo', 'docs_url')}
        markdown_parser.convert(text)
        item.update({k: '\n'.join(v) for k, v in markdown_parser.Meta.items()})
        item['name'] = item_file.stem
        item['description'] = text.split('\n\n', 1)[1]
        items.append(item)
    return sorted(items, key=itemgetter('name'))


def generate_catalogue_md(sections: OrderedDict) -> None:
    result = PROLOGUE
    for section_name, subsections in sections.items():
        assert all(x[0].isupper() for x in section_name.split()), \
            'All words in a section name must start with an uppercase character.'
        result += f'## {section_name}\n\n'
        for subsection_name, items in subsections.items():
            assert all(x[0].isupper() for x in subsection_name.split()), \
                'All words in a section name must start with an uppercase character.'
            result += f'### {subsection_name}\n\n'
            for item in items:
                result += format_item(item) + '\n'
    return result


def format_item(item: Dict[str, str]) -> str:
    name = item['name']
    result = ITEM_HEADING_AND_SHIELDS.format(name=name)

    github_repo = item.get('github_repo')
    if github_repo is not None:
        assert github_repo.count('/') == 1
        result += ITEM_GITHUB_SHIELDS.format(github_repo=github_repo)

    result += '\n'

    description = item['description']
    assert name in description
    result += description.replace(
        name, f'[{name}](https://pypi.python.org/pypi/{name})', 1)

    footer = []
    docs_url = item.get('docs_url')
    if docs_url is not None:
        footer.append(f'[documentation]({docs_url})')
    if github_repo is not None:
        footer.append(f'[code repository](https://github.com/{github_repo})')
    if footer:
        result += '\n' + ' &ndash; '.join(footer)

    return result + '\n'


def main(contents, page) -> None:
    if page.title != 'Catalogue':
        return None
    else:
        return generate_catalogue_md(read_sections())


if __name__ == '__main__':
    from types import SimpleNamespace
    print(main(None, SimpleNamespace(title='Catalogue')))
