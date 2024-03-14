# Reflective

Reflective provides a plethora of ways to access and manipulate structured data.

**Notice!** This project is in early-stage development so the API may change aggressively,
and some features are not currently present.

## Branch Status

| Branch  | CodeQL                                                                                                                                                                                                                 | Build                                                                                                                                                                                             |
|---------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `dev`   | [![CodeQL](https://github.com/AzorianSolutions/reflective/actions/workflows/codeql-analysis.yml/badge.svg?branch=dev)](https://github.com/AzorianSolutions/reflective/actions/workflows/codeql-analysis.yml)           | [![Build](https://github.com/AzorianSolutions/reflective/actions/workflows/build.yml/badge.svg?branch=dev)](https://github.com/AzorianSolutions/reflective/actions/workflows/build.yml)           |
| `0.2.0` | [![CodeQL](https://github.com/AzorianSolutions/reflective/actions/workflows/codeql-analysis.yml/badge.svg?branch=release/0.2.0)](https://github.com/AzorianSolutions/reflective/actions/workflows/codeql-analysis.yml) | [![Build](https://github.com/AzorianSolutions/reflective/actions/workflows/build.yml/badge.svg?branch=release/0.2.0)](https://github.com/AzorianSolutions/reflective/actions/workflows/build.yml) |
| `0.2.1` | [![CodeQL](https://github.com/AzorianSolutions/reflective/actions/workflows/codeql-analysis.yml/badge.svg?branch=release/0.2.1)](https://github.com/AzorianSolutions/reflective/actions/workflows/codeql-analysis.yml) | [![Build](https://github.com/AzorianSolutions/reflective/actions/workflows/build.yml/badge.svg?branch=release/0.2.1)](https://github.com/AzorianSolutions/reflective/actions/workflows/build.yml) |

## Table of Contents

- [Branch Status](#branch-status)
- [TL;DR](#tldr)
- [Installation](#installation)
- [Project Documentation](#project-documentation)
    - [Project Information](#project-information)
    - [Contributing](#contributing)
    - [Configuration](#configuration)
    - [Library Development](#library-development)
    - [Library Testing](#library-testing)
- [Security Policy](#security-policy)
- [Support Policy](#support-policy)
- [Code of Conduct](#code-of-conduct)
- [License](#license)
- [Donate](#donate)

## TL;DR

With Reflective, you can access and update composite data structures in many ways:

```python
from reflective import Reflective

data = {
    "app": {
        "name": "Appy McAppface",
        "description": "The $r{/app/name} app is a great!",
        "version": "1.2.3",
        "tags": ["production", "release", "v$r{/app/version}"],
    }
}

r = Reflective(data)

print(r.app.name)  # Appy McAppface
print(r.app['description'])  # The Appy McAppface app is a great!
print(r.app('version'))  # 1.2.3
print(r.app.tags)  # ['production', 'release', 'v1.2.3']
print(r.app.tags().raw)  # ['production', 'release', 'v$r{/app/version}']
print(r.app.tags[2])  # v1.2.3
print(r.app.tags[2]().raw)  # v$r{/app/version}
```

For a much better explanation of all the features you see here, please see
the [Feature Documentation](./docs/wiki/project/features.md).

## Installation

**Notice! This requires Python 3.8+**

To install the Python package, run the following command in your Python environment:

```bash
python3 -m pip install reflective
```

The PyPi package is automatically built and published to the PyPi repository for each release. If you want to install
a release from the source, run the following commands in your terminal:

```bash
python3 -m pip install --upgrade git+
git clone https://github.com/AzorianSolutions/reflective.git
cd reflective
git checkout tags/v<release-version> -b release/<release-version>
python3 -m pip install .
```

## Project Documentation

### Project Information

For information about the project such as feature planning, the roadmap, and milestones, then please see the
[Project Information](./docs/wiki/project/README.md) section of the
wiki.

### Contributing

If you're interested in participating in the project design discussions, or you want to actively submit work to the
project then you should check out the
[Contribution Guide](./docs/wiki/contributing/README.md)!

### Configuration

For information about all the ways this library can be configured and what each setting does, please visit the
[Configuration Guide](./docs/wiki/configuration/README.md) section of the wiki.

### Library Development

For information about how the library is designed and actually works, please visit the
[Development Guide](docs/wiki/development/README.md) section of the wiki.

### Library Testing

For information on how to create and execute automated library tests, please visit the
[Testing Guide](./docs/wiki/testing/README.md) section of the wiki.

## Security Policy

Please see our [Security Policy](./.github/SECURITY.md).

## Support Policy

Please see our [Support Policy](./docs/wiki/support/README.md).

Looking to chat with someone? Join our [Discord Server](https://discord.azorian.solutions).

## Code of Conduct

Please see our [Code of Conduct](./.github/CODE_OF_CONDUCT.md).

## License

This project is released under the MIT license. For additional information, [see the full license](./LICENSE).

## Donate

Like my work?

<a href="https://www.buymeacoffee.com/AzorianMatt" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-blue.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>

**Want to sponsor me?** Please visit my organization's [sponsorship page](https://github.com/sponsors/AzorianSolutions).
