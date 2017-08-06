#!/usr/bin/env python3

from collections import defaultdict, OrderedDict
from operator import itemgetter
from pathlib import Path
from typing import Dict, List

from yaml import load as load_yaml


PROJECT_DIR = Path(__file__).parent
ITEMS_DIR = PROJECT_DIR / 'items'
TARGET_FILE = PROJECT_DIR / 'docs' / 'index.md'

PROLOGUE = """# Python for the Humanities

Lorem ipsum motivationales

For a list of general recommendations on Python libraries check out
[Awesome Python](https://awesome-python.com/)."""


def read_items() -> List[Dict]:
    result = []
    for item_file in ITEMS_DIR.glob('*.yml'):
        with open(item_file, 'rt') as f:
            result.append(load_yaml(f))
    return result


def group_and_sort_items(items: List[Dict]) -> OrderedDict:
    def group_by(items: List, key) -> Dict[str, List]:
        result = defaultdict(list)
        for item in items:
            result[item[key]].append(item)
        return result

    def key_sorted_mapping(mapping: Dict) -> OrderedDict:
        return OrderedDict(sorted(mapping.items(), key=itemgetter(0)))

    sections = key_sorted_mapping(group_by(items, 'section'))

    for section, items in sections.items():
        assert all(x[0].isupper() for x in section.split())
        subsections = key_sorted_mapping(group_by(items, 'subsection'))

        for subsection, items in subsections.items():
            assert all(x[0].isupper() for x in subsection.split())
            subsections[subsection] = sorted(items, key=itemgetter('name'))

        sections[section] = subsections

    return sections


def write_index_md(sections: OrderedDict) -> None:
    with open(TARGET_FILE, 'wt') as f:
        print(PROLOGUE, file=f)
        for section_name, subsections in sections.items():
            print(f'\n\n## {section_name}\n', file=f)
            for subsection_name, items in subsections.items():
                print(f'### {subsection_name}\n', file=f)
                for item in items:
                    print(format_item(item), file=f)


def format_item(item: Dict[str, str]) -> str:
    name = item['name']
    result = [f'#### {name}\n']

    result.append(f'![license](https://img.shields.io/pypi/l/{name}.svg)')
    result.append(f'![version](https://img.shields.io/pypi/v/{name}.svg)')
    result.append(f'![pyversions](https://img.shields.io/pypi/pyversions/{name}.svg)')
    result.append(f'![maturity](https://img.shields.io/pypi/status/{name}.svg)')

    github_repo = item.get('github_repo')
    if github_repo is not None:
        assert github_repo.count('/') == 1
        result.append(f'![stars](https://img.shields.io/github/stars/{github_repo}.svg)')
        result.append(f'![contributors](https://img.shields.io/github/contributors/{github_repo}.svg)')
        result.append(f'![forks](https://img.shields.io/github/forks/{github_repo}.svg)')

    result.append('')
    description = item['description']
    assert name in description
    result.append(description.replace(name, f'[{name}](https://pypi.python.org/pypi/{name})', 1))

    footer = []
    docs_url = item.get('docs_url')
    if docs_url is not None:
        footer.append(f'[documentation](docs_url)')
    if github_repo is not None:
        footer.append(f'[code repository](https://github.com/{github_repo})')
    if footer:
        result.append(' &ndash; '.join(footer))

    return '\n'.join(result)


def main() -> None:
    write_index_md(group_and_sort_items(read_items()))


if __name__ == '__main__':
    main()
