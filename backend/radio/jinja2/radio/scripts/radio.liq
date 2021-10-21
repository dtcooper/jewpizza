# radio

settings.server.telnet.set(true)
settings.server.telnet.port.set(1234)
settings.server.telnet.bind_addr.set("0.0.0.0")

REDIS_PUBSUB_CHANNEL = {{ REDIS_PUBSUB_CHANNEL|liqval }}
ICECAST_HOSTNAME = {{ config.ICECAST_HOSTNAME|liqval }}
ICECAST_PORT = {{ config.ICECAST_PORT|liqval }}
ICECAST_USERNAME = {{ config.ICECAST_USERNAME|liqval }}
ICECAST_PASSWORD = {{ config.ICECAST_PASSWORD|liqval }}
ICECAST_PROTOCOL = {{ config.ICECAST_PROTOCOL|liqval }}

jingle = single(fallible=false, '/jingle.mp3')

def show_announcement()
    minutes = random.int(min=1, max=20)
    minutes_str = '#{string_of(minutes)} minute' ^ if minutes == 1 then '' else 's' end
    announcement = 'The show will begin in #{minutes_str}!'
    uri = 'annotate:title="jew.pizza Annoucement: The show begins in #{minutes_str}":text2wave:#{announcement}'
    [request.create(uri)]
end

radio = mksafe(rotate([request.dynamic.list(show_announcement), jingle]))

def send_metadata_to_redis(m)
    j = json()
    j.add("title", metadata.title(m))
    j.add("full", metadata.export(m))
    message = json.stringify(compact=true, j)
    cmd = 'redis-cli -h redis publish #{process.quote(REDIS_PUBSUB_CHANNEL)} #{process.quote("metadata:" ^ message)}'
    print(cmd)
    process.run(cmd)
end

radio.on_metadata(send_metadata_to_redis)

radio = mksafe(radio)
output.dummy(radio)
output = output.icecast(
    %mp3,
    host=ICECAST_HOSTNAME,
    port=ICECAST_PORT,
    user=ICECAST_USERNAME,
    password=ICECAST_PASSWORD,
    protocol=ICECAST_PROTOCOL,
    mount='radio',
    radio,
)
