MAX_BUFFER = 10.

input = input.http(
    id='input',
    max_buffer=MAX_BUFFER,
    poll_delay=0.5,
    "http://radio:8000/radio",
)

failsafe = single(fallible=false, '/failsafe.mp3')

radio = fallback(track_sensitive=false, [input, failsafe])

hostname = {{ config.ICECAST_HOSTNAME|liqval }}
port = {{ config.ICECAST_PORT|liqval }}
username = {{ config.ICECAST_USERNAME|liqval }}
password = {{ config.ICECAST_PASSWORD|liqval }}
protocol = {{ config.ICECAST_PROTOCOL|liqval }}

output.icecast(%mp3, host=hostname, port=port, user=username, password=password, protocol=protocol, mount='radio', radio)
