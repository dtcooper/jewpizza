MAX_BUFFER = 10.

input = input.http(
    id='input',
    max_buffer=MAX_BUFFER,
    poll_delay=0.5,
    "http://radio:8000/radio",
)

failsafe = single(fallible=false, '/failsafe.mp3')

radio = fallback(track_sensitive=false, [input, failsafe])

host = {{ settings.ICECAST_HOST|liqval }}
port = {{ settings.ICECAST_PORT|liqval }}
username = {{ settings.ICECAST_USERNAME|liqval }}
password = {{ settings.ICECAST_PASSWORD|liqval }}
protocol = {{ settings.ICECAST_PROTOCOL|liqval }}

output.icecast(%mp3, host=host, port=port, user=username, password=password, protocol=protocol, mount='radio', radio)
