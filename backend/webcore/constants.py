CACHE_KEY_PREFIX_STATIC_ASSET_MD5SUM = "static-asset-md5sum::"

NAVIGATION_LINKS = [
    # Name, url_name, icon, is_subnav
    ("Home", "webcore:index", "ic:baseline-home", False),
    ("Shows", "shows:shows", "mdi:calendar-check-outline", False),
    ("Listen", None, "ic:outline-radio", False),
    ("Bio", "webcore:bio", "mdi:text-account", False),
    ("Newsletter", None, "mdi:email-newsletter", True),
    ("Testimonials", None, "bi:chat-text", True),  # XXX url_name to to show an active one
    ("Social", None, "mdi:twitter", True),
    ("Contact", None, "mdi:email", True),
]
