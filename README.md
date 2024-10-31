<a name="readme-top"></a>

<br /> 
<div align="center"> 
<h3 align="center">Hypixel-Api-Lib</h3> 
<p align="center"> A Python library for interacting with the Hypixel SkyBlock API.
<br /> 
<a href="https://github.com/Feromond/hypixel-api-lib"><strong>Explore the docs »</strong></a> <br /> 
<br /> 
<a href="https://github.com/Feromond/hypixel-api-lib/issues">Report Bug</a> · <a href="https://github.com/Feromond/hypixel-api-lib/issues">Request Feature</a> </p> </div> 
<details> 
<summary>Table of Contents</summary> 
<ol> <li> <a href="#about-the-project">About The Project</a> </li> <li>
<a href="#directory-information">Directory Information</a></li> <ul> <li>
<a href="#hypixel-api-lib">hypixel-api-lib/</a></li> 
<li><a href="#tests">tests/</a></li> 
<li><a href="#examples">examples/</a></li> 
<li><a href="#root-files">Root Files</a></li> </ul> 
<li><a href="#built-with">Built With</a></li> 
<li> <a href="#getting-started">Getting Started</a> <ul> 
<li><a href="#prerequisites">Prerequisites</a></li> 
<li><a href="#installation">Installation</a></li> </ul> </li> 
<li><a href="#usage">Usage</a></li> 
<li><a href="#roadmap">Roadmap</a></li> 
<li><a href="#contact">Contact</a></li> </ol> </details>

<!-- ABOUT THE PROJECT -->

## About The Project

`hypixel-api-lib` is a Python library that provides an easy-to-use interface for interacting with the Hypixel SkyBlock API. It simplifies the process of fetching and processing data from the API, allowing developers to focus on building applications and tools for the Hypixel SkyBlock community.

The library includes components for accessing player profiles, game statistics, items, skills, and events like the current Bingo event. It handles API requests, data parsing, and provides convenient classes and methods to work with the data.

Our goal with `hypixel-api-lib` is to create a comprehensive and efficient library for developers to build rich applications, bots, or analytics tools related to Hypixel SkyBlock.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Directory Information

### **hypixel-api-lib/**

```sh
geophysics_lib/
├── __init__.py
├── Elections.py
├── Collections.py
├── Items.py
├── Skills.py
└── etc.... (more in-progress)
```

This is the core of the library, containing all the modules and packages that implement the API interactions and data models.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### **tests/**

```sh
tests/
├── test_bingo.py
├── test_items.py
├── test_skills.py
└── ... etc ...
```

This directory contains all the unit tests for the library modules, ensuring code quality and correctness. Each test file corresponds to a module in the library.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### **examples/**

```sh
examples/
├── bingo_example.py
├── items_example.py
├── skills_example.py
└── ... etc ...
```

This directory contains all the example code for this library. Each component has some sample code included that demonstrates how it could be used and some generate structure. Still largely a work in progress.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### **Root Files**

```sh
.
├── LICENSE            # None set yet
├── README.md          # This file
├── .gitignore         # Files to ignore during our git process
├── .env               # (Will be gitignored) File to store environment vairables such as API keys for examples.
├── Makefile           # Commands for building, initializing, and other tasks
├── requirements.txt   # Lists the Python package dependencies
├── setup.py           # Setup script for packaging and distribution
├── examples/
├── hypixel_api_lib/
└── tests/

```

The root directory includes important files for building and managing the project.

- Makefile: Simplifies common tasks such as building the package or installing requirements.

- requirements.txt: Specifies the required Python packages.

- setup.py: Used for packaging and distributing the library.

- LICENSE: Contains the license information for the project.

- README.md: Provides an overview and documentation of the project.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Built With

![](https://img.shields.io/badge/Code-Python-informational?style=flat&logo=Python&logoColor=white&color=4AB197)
![](https://img.shields.io/badge/Package-Requests-informational?style=flat&logo=Requests&logoColor=white&color=4AB197)
![](https://img.shields.io/badge/Package-Pandas-informational?style=flat&logo=Pandas&logoColor=white&color=4AB197)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

Python 3.12 or higher

Git (for cloning the repository)

### Installation

1. Clone the repository

   ```sh
   git clone https://github.com/Feromond/hypixel-api-lib.git
   cd hypixel-api-lib
   ```

2. Install the required packages and setup venv

   ```make
   make init
   ```

3. Install the library

   In editable mode:

   ```make
   make build_local
   ```

      <p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->

## Usage

Here we will describe how to use `Hypixel-Api-Lib`, including examples of how to import and utilize the library's functions in your own projects.

### Fetching the Current Bingo Event

```Python
from hypixel_api_lib.Bingo import BingoEvents

# Initialize the BingoEvents manager
bingo_events = BingoEvents()

# Get the current bingo event
current_event = bingo_events.get_current_event()

# Print event details
print(f"Bingo Event: {current_event.name} (ID: {current_event.id})")
print(f"Modifier: {current_event.modifier}")

```

### Retrieving Item Information

```Python
from hypixel_api_lib.Items import Items

# Initialize the Items manager
items = Items()

# Get item details by item ID
item_id = 'ASPECT_OF_THE_END'
item = items.get_item_by_id(item_id)

# Print item information
print(f"Item Name: {item.name}")
print(f"Description: {item.get_clean_lore()}")

```

For more examples and usage instructions, please refer to the documentation or check out the `examples/` folder for more full code examples

<!-- ROADMAP -->

## Roadmap

- [x] Set up project structure and initial modules
- [ ] Implement core components (Bingo, Items, Skills, Profiles etc...)
- [ ] Write unit tests for core modules
- [ ] Expand documentation with examples and tutorials
- [ ] Publish package to PyPI
- [ ] Add support for additional API endpoints outside skyblock
- [ ] Improve existing code to support future developer experiences

See the [open issues](https://github.com/Feromond/hypixel-api-lib/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->

## Contact

Jacob Mish - [Portfolio](https://jacobmish.com) - [LinkedIn](https://www.linkedin.com/in/jacob-mish-25915722a/) - JacobPMish@gmail.com

Desmond O'Brien- [LinkedIn](https://www.linkedin.com/in/des-ob/) - desmond.obrien@ucalgary.ca

Project Link: [https://github.com/Feromond/hypixel-api-lib](https://github.com/Feromond/hypixel-api-lib)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
