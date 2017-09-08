#!/usr/bin/env python3

from collections import defaultdict, OrderedDict
from operator import itemgetter
from pathlib import Path
from typing import Dict, List

from yaml import load as load_yaml


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
    for item_file in subsection.glob('*.yml'):
        with open(item_file, 'rt') as f:
            items.append(load_yaml(f))
    return sorted(items, key=itemgetter('name'))


def write_index_md(sections: OrderedDict) -> None:
    with open(TARGET_FILE, 'wt') as f:
        print(PROLOGUE, file=f)
        for section_name, subsections in sections.items():
            print(f'## {section_name}\n', file=f)
            for subsection_name, items in subsections.items():
                print(f'### {subsection_name}\n', file=f)
                for item in items:
                    print(format_item(item), file=f)


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


def main() -> None:
    write_index_md(read_sections())


if __name__ == '__main__':
    main()
