# radio

settings.server.telnet.set(true)
settings.server.telnet.port.set(1234)
settings.server.telnet.bind_addr.set("0.0.0.0")
settings.server.timeout.set(-1.)

REDIS_PUBSUB_CHANNEL = {{ REDIS_PUBSUB_CHANNEL|liqval }}
HOSTNAME = {{ config.ICECAST_HOSTNAME|liqval }}
PORT = {{ config.ICECAST_PORT|liqval }}
USERNAME = {{ config.ICECAST_USERNAME|liqval }}
PASSWORD = {{ config.ICECAST_PASSWORD|liqval }}
PROTOCOL = {{ config.ICECAST_PROTOCOL|liqval }}

jingle = single(fallible=false, '/jingle.mp3')

def show_announcement_request()
    minutes = random.int(min=1, max=20)
    minutes_str = '#{string_of(minutes)} minute' ^ if minutes == 1 then '' else 's' end
    announcement = 'The show will begin in #{minutes_str}! Please stay tuned.'
    title = 'jew.pizza Annoucement: The show begins in #{minutes_str}'
    uri = 'annotate:title="#{string.escape(title)}":text2wave:#{announcement}'
    [request.create(uri)]
end

radio = mksafe(rotate([request.dynamic.list(show_announcement_request), jingle]))

def send_message_to_redis(type, message)
    message = "#{type}:#{json.stringify(compact=true, message)}"
    cmd = 'redis-cli -h redis publish #{process.quote(REDIS_PUBSUB_CHANNEL)} #{process.quote(message)}'
    if not process.test(cmd) then
        log("ERROR: error publishing to redis with command: #{cmd}")
    else
        log("#{type} message sent to #{REDIS_PUBSUB_CHANNEL}")
    end
end

def send_metadata_to_redis(m)
    message = json()
    message.add("title", metadata.title(m))
    message.add("full", metadata.export(m))
    send_message_to_redis('metadata', message)
end

radio.on_metadata(send_metadata_to_redis)

radio = mksafe(radio)
output.dummy(radio)
output = output.icecast(
    %mp3,
    host=HOSTNAME,
    port=PORT,
    user=USERNAME,
    password=PASSWORD,
    protocol=PROTOCOL,
    mount='radio',
    on_error=fun(e) -> begin
        log("ERROR: error connecting to #{PROTOCOL}://#{USERNAME}:#{PASSWORD}@#{HOSTNAME}:#{PORT}/radio: #{e}")
        1.
    end,
    radio,
)
