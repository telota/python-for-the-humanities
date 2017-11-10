# Contributing

> The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
> "SHOULD NOT", "RECOMMENDED",  "MAY", and "OPTIONAL" in this document are to
> be interpreted as described in [RFC 2119](https://www.ietf.org/rfc/rfc2119).


## Criteria

- The library must be available on the
  [Python Package Index](https://pypi.python.org).
- It shall not be a Python 2-only package.
- A code review must not reveal unmaintainable gibberish and common practices
  that implement quality assurance should be in place.
- TODO


## Guidelines

Each catalogue item is defined in a Markdown document with a metadata-section
at the top. Its location within the `items` folder defines the section it will
appear within the assembled catalogue. The name of the document file must match
the described package's name on the Python Package Index.

The description must meet these constraints:

- Its extent must be one paragraph.
- It should not contain more seven sentences.
- It must describe the package's functionality.
- It may mention design aspects and background of the package.
- The package's name must be mentioned at least once, the first appearance will
  be used as hyperlink text.

If there is a documentation resource available as web page, its URL must
be included in the metadata section assigned to the `docs_url` field, the URL
must be provided with `https` as protocol when available as such.

If the source code is hosted on [GitHub](https://github.com), it must be
denoted as `<username>/<repository_name` assigned to the `github_repo` field.

When adding a new section respectively folder, keep in mind that all words must
start with an uppercase character.

If you see more data on a package as appropriate to include, please open an
issue with your proposal.

## Building

Installing the required packages:

    pip install -r requirements.txt

Building the web page:

    make
    # or if GNU make is not available:   :-(
    ./generate-docs.py
    mkdocs build
