# Zensearch

Submission for Coding Challenge

![workflow](https://github.com/maoyalu/zen_cc_search/actions/workflows/ci.yml/badge.svg)
[![codecov](https://codecov.io/gh/maoyalu/zen_cc_search/branch/master/graph/badge.svg?token=0NNV59BG3O)](https://codecov.io/gh/maoyalu/zen_cc_search)

---

## Prerequisites

1. To run this CLI application, you should have `Python 3.x` and `pip` installed and configured to use.

    You can download it here:

    https://www.python.org/downloads/

2. `git` for downloading code and version control.
    
    You can download it here:

    https://git-scm.com/downloads

## How to install

1. Clone and go into the root directory

```bash
git clone https://github.com/maoyalu/zen_cc_search.git

cd zen_cc_search
```

2. Restore project requirements

```bash
pip3 install -r requirements.txt
```

3. Run

```bash
python3 -m zensearch
```

## How to use

1. **Configure cache settings.**

    `zensearch/config.py` stores configs that enable reverse index. If it is set to `true`, additional spaces will be allocated for faster lookup, accelerating the search from `O(n)` to `O(1)`.

    To make new configs effective, you need to restart the app.

2. **Quit anytime.**

    Type `quit` into the prompt and hit `ENTER` anytime, ane then the program will request your confirmation for exit.

    `Y` - Exit

    `N` (default) - Cancel and go back to the main page

3. **Select options**

    Option list will be provided above the prompt.

    Select the option number and hit `ENTER`. If the option number is invalid, an error message will be shown.

4. **Search for the value**

    Empty value is supported.
    
    Simply hit `ENTER` without typing anything.

5. **Navigation**

    ```
    Main
     |----- Search
     |       |----- Users
     |       |----- Tickets
     |
     |----- View Searchable Fields

## Tradeoffs

1. In order to approach O(1) time as much as possible, additional spaces are allocated. Searching generally will take O(n) time so perform lookups to prevent searching if possible. 

    This feature can be switched off or partially enabled depending on users' actual situation.

    By defulat, this feature is **enabled**.

## Assumptions

1. Users are comfortable using CLI, but they are not that technical so interactions are designed in a humanly way instead of using command argument options.

2. Memory is sufficient for storing all the data.

3. No value of 'quit' exist in the data, otherwise it will contradict with the requirement 'Exit anytime'.

4. Optional fields are observed from the json files provided.

    ### User

    | Field | Description |
    |--|--|
    | _id | * **required**<br/>* **unique**<br/>* int |
    | name | * **required**<br/>* string |
    | created_at | * **required**<br/>* string |
    | verified | * optional<br/>* boolean<br/>* default `False`

    ### Ticket

    | Field | Description |
    |--|--|
    | _id | * **required**<br/>* **unique**<br/>* string |
    | created_at | * **required**<br/>* string |
    | type | * optional<br/>* string<br/>* default `None` |
    | subject | * **required**<br/>* string |
    | assignee_id | * optional<br/>* int<br/>* default `None` |
    | tags | * **required**<br/>* list of string |


## Scalability

Uses MVC structure to reduce coupling.

* Model - `database.py`
    
* View - `cli.py`

* Controller - `__main__.py`

* Constants - `constants.py`, `config.py`

<br/>

1. No changes to CLI required for changes of searchable fields.

    You only need to update the enum in `constants.py`

2. Easy to switch to use a database in the future.

    You only need to update the implementation of `database.py`

3. Use constants to prevent hardcoded string

## Future thoughts

1. Use date type instead of string for `created_at`

    It's ridiculous to use a date time format string to search.

    And date type allows more flexible searches like date range and provides better support for multi-timezone.

2. Cache on demand

    Another way to cache is storing them when they are searched along with an expiration time.

    It can reduce startup time and memory used in runtime comparing to the current cache strategy.

    This can be beneficial if the number of frequently searched items is very small.

3. Advanced search

    Current version only implements searching with one single field.

    Searches with a combination of fields generally take `O(n)` time. 

