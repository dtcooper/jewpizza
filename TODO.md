# TODO List


* [x] Collect emails, have a mailing list + notification of shows
* [x] Scroll up on page load
* [x] Use [umami](https://github.com/mikecao/umami) for tracking
* [x] Investigate whether to complete JSON rendering in middleware.
* [x] Move send notification outside of admin, in a superuser-only area with a
    single link from admin, but using a classless CSS reset.
* [x] Add "I would like to also be signed up for the newsletter" to contact form.
* [x] Make minimum input size 16px to avoid mobile safari zoom.
    [More info here](https://stackoverflow.com/a/6394497).
* [x] Log IP from contact form.
* [x] Vertically center homepage hero
* [x] namespace webcore static assets with a folder `webcore/`
* [x] [Optimize images](https://imageoptim.com/mac)
* [x] favicon emoji using inline SVG (google it)
* [x] Remove automatic `SECRET_KEY` generation, just document it in README. This needs to be set before first run.
* [x] set timezones in ALL containers
* [x] Remove _all_ radio-uplink code
* [x] Add metadata delay to sse publisher
    - [x] Switch to actual json messages, with `type` and `delay` (optional, with a max), and `message`
* [x] Restart radio liquidsoap script with watchdog when `DEBUG=1`
* [x] Report on prod JS exceptions via email
* [x] Custom error pages
    - [x] nginx 502 unavailable during deployment (static file @ `frontend/unavailable.html`)
    - [x] Django specific (500, 404, 403)
* [ ] Icecast server + liquidsoap with player to play whatever show I'm on, read
      countdowns when I'm not on air
    - [ ] Call-in button via Twilio client
* [ ] Move [radio-calls](https://github.com/dtcooper/radio-calls) repo into this
* [ ] Warn on leave iff player is playing
* [ ] Testimonials / Calls / Etc in clippy?
* [ ] Social media card, Twitter card validator (Alpine day source code? 1200x660 jpg Twitter card.)
* [ ] Dark mode?
* [ ] Use devtools lighthouse?
* [ ] Leave space on bottom to render page / controls when clippy is maximized
    - [ ] Consider removing emoji footer
* [ ] Bitcoin donations
* [ ] Get duration and other info from ffprobe
    - `ffprobe -i <filename> -print_format json -hide_banner -loglevel error -show_format -show_error -show_streams -select_streams a:0`
* [ ] Use headphone jewippy when you click shows or listen
* [ ] Fixtures, at least for shows by GUID
* [ ] [Space Grotesk](https://fonts.google.com/specimen/Space+Grotesk) for body copy
* [ ] [Change Podcast RSS](https://castos.com/podcast-directories/)
* [ ] Decouple podcast namedtuples with shows?
* [ ] Radio should have a mountpoint to pre-empty and stream from

## Sections

1.  How to listen -- [expandable](https://codepen.io/philw_/pen/GREJEgx)
    1. Showgram
    2. Podcast
    3. WFMU
    4. BMIR
2. Bio
3. Social
4. Testimonials
5. Notifications (Newsletter)
6. Contact
