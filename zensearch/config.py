class Config:
    """
        SETTINGS
    ------------------
    If the cache setting is turned on, 
    the app will set up reverse index for faster lookup.

    * Note that, additionally spaces will be needed.

    After changing the config, please restart the app.

    """

    # Data json files
    USER_JSON = 'zensearch/data/users.json'
    TICKET_JSON = 'zensearch/data/tickets.json'

    # region User caching

    # Enable reverse lookup users using name
    CACHE_USER_NAME = True

    # Enable reverse lookup users using created_at
    CACHE_USER_CREATED_AT = True

    # Enable reverse lookup users using verified
    CACHE_USER_VERIFIED = True

    # endregion User caching

    # region Ticket caching

    # Enable reverse lookup tickets using created_at
    CACHE_TICKET_CREATED_AT = True

    # Enable reverse lookup tickets using type
    CACHE_TICKET_TYPE = True

    # Enable reverse lookup tickets using subject
    CACHE_TICKET_SUBJECT = True

    # Enable reverse lookup tickets using assignee_id
    CACHE_TICKET_ASSIGNEE_ID = True

    # Enable reverse lookup tickets using tags
    CACHE_TICKET_TAGS = True

    # endregion Ticket caching
