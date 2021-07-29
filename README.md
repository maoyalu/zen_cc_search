# Zensearch

Submission for Coding Challenge

![workflow](https://github.com/maoyalu/zen_cc_search/actions/workflows/ci.yml/badge.svg)
[![codecov](https://codecov.io/gh/maoyalu/zen_cc_search/branch/master/graph/badge.svg?token=0NNV59BG3O)](https://codecov.io/gh/maoyalu/zen_cc_search)

---

## How to install

1. Clone and go into the root directory

```bash
git clone https://github.com/maoyalu/zen_cc_search.git

cd zen_cc_search
```

2. Restore project requirements

```bash
pip install -r requirements.txt
```

3. Run

```bash
python -m zensearch
```

## How to use

???

## Tradeoffs

1. In order to approach O(1) time as much as possible, additional spaces are allocated. Searching generally will take O(n) time so perform lookups to prevent searching if possible.

## Assumptions

1. Users have no problem using CLI.

2. Memory is sufficient for storing all the data.

3. Optional fields are observed from the json files provided.

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
