# Contributing

## Criteria

- The library must be available on the [PyPI](https://pypi.python.org).
- TODO


## Guidelines

Each catalogue item is defined in a YAML document with a mappping as top-level
object that is located in the `items` directory. The following fields must be
provided:

- `name`
  - as on the PyPI
- `section`
  - all words must be capitalized
- `subsection`
  - same here
- `description`
  - the `name` value must be mentioned at least once, this wille be used as
    hyperlink text
  - describes functionality, design aspects and background
  - should be at most seven sentences


If there is a documentation resource available as web page, it's URL must
be included:

- `docs_url`
  - preferably with `https` as protocol

If the source code is hosted on [GitHub](https://github.com), this is also
mandatory:

- `github_repo`
  - `<username>/<repository_name`


## Building

Installing the required packages:

    pip install -r requirements.txt

Building the web page:

    make
    # or if GNU make is not available:   :-(
    ./generate-docs.py
    mkdocs build


*[PyPI]: Python Package Index
