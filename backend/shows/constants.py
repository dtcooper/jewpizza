from collections import namedtuple

Show = namedtuple("Show", "code slug name has_banner", defaults=(True,))

SHOWS = (
    Show("showgram", "showgram", "The Late Showgram w/ Jim Richards"),
    Show("twwit", "that-went-well-i-think", "That Went Well, I Think w/ David Cooper"),
    Show("tigwit", "this-is-going-well-i-think", "This Is Going Well, I Think w/ David Cooper"),
    Show("bmir", "bmir", "Burning Man Information Radio (BMIR)"),
    Show("misc", "misc", "Miscellaneous & Guest Apperances", has_banner=False),
)

SHOW_CHOICES = tuple((show.code, show.name) for show in SHOWS)
