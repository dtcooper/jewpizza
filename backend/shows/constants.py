from collections import namedtuple


Show = namedtuple("Show", "code slug name has_banner_img podcast", defaults=(True, None))
Podcast = namedtuple("Podcast", "title author description")

SHOWS = (
    Show(
        name="The Late Showgram w/ Jim Richards",
        code="showgram",
        slug="showgram",
    ),
    Show(
        name="That Went Well, I Think w/ David Cooper",
        code="twwit",
        slug="that-went-well-i-think",
    ),
    Show(
        name="This Is Going Well, I Think w/ David Cooper",
        code="tigwit",
        slug="this-is-going-well-i-think",
        podcast=Podcast(
            title="This Is Going Well, I Think with David Cooper",
            author="David Cooper",
            description=(
                "It's not a podcast. It's a radio show.\nEnjoy the incoherency, bad listening skills and self-doubt"
                " that is host David Cooper. As I write this description I truly can't tell you what the show is about."
                " This is going well, I think. Broadcast live, there's comedians, callers with a real telephone,"
                " laughter, anger, and frustration. There's some very real moments. Oh, and flashing neon lights. It's"
                " a nightmare. Airing live most Tuesdays at 4pm PT / 7pm ET, we might take your calls or texts at +1"
                " (415) 857-1155. No promises. Listen live at shoutingfire.com or on iHeartRadio. Kill me."
            ),
        ),
    ),
    Show(
        name="Burning Man Information Radio (BMIR)",
        code="bmir",
        slug="bmir",
    ),
    Show(
        name="Misc. & Guest Appearances",
        code="misc",
        slug="misc",
        has_banner_img=False,
    ),
)

SHOW_CODES_TO_SHOW = {show.code: show for show in SHOWS}
SHOW_CHOICES = tuple((show.code, show.name) for show in SHOWS)
