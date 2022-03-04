{#
    Radio script jinja template.
-#}

settings.server.telnet.set(true)
settings.server.telnet.port.set(1234)
settings.server.telnet.bind_addr.set("0.0.0.0")
settings.server.timeout.set(-1.)

log("Starting harbor (script generated " ^ {{ now()|liqval }} ^ ")")

PASSWORD = {{ settings.ICECAST_SOURCE_PASSWORD|liqval }}

METADATA_MESSAGE_DELAY = 5.
NCHAN_URL = "http://nginx:3000/"

{% include 'radio/reload.liq' %}
{% include 'radio/protocols.liq' %}
{% include 'radio/http.liq' %}

jingle = single(fallible=false, '/audio/jingle.mp3')

def show_announcement_request()
    minutes = random.int(min=1, max=20)
    minutes_str = "#{string_of(minutes)} minute" ^ if minutes == 1 then "" else "s" end
    announcement = "The show will begin in #{minutes_str}! Please stay tuned."
    title = "jew.pizza Annoucement: The show begins in #{minutes_str}"
    uri = 'annotate:title="#{string.escape(title)}":mimic:#{announcement}'
    [request.create(uri)]
end

radio = mksafe(rotate([request.dynamic.list(show_announcement_request), jingle]))

def pad(n, ~char="0", ~num=2)
    out = ref(string_of(n))
    while string.length(!out) < num do
        out := "#{char}#{!out}"
    end
    !out
end

def zulu_now()
    t = time.utc()
    "#{t.year}-#{pad(t.month)}-#{pad(t.day)}T#{pad(t.hour)}:#{pad(t.min)}:#{pad(t.sec)}Z"
end

def _send_message_to_nchan_http_post(type, message)
    data = json()
    data.add("type", type)
    data.add("message", message)
    data.add("timestamp", zulu_now())
    data = json.stringify(compact=true, data)
    response = http.post(data=data, headers=[("Accept", "text/json"), ("X-EventSource-Event", type)], NCHAN_URL)
    if response.status_code >= 201 and response.status_code <= 202 then
        num_subscribers = string_of(list.assoc(default=0, "subscribers", json.parse(default=[("_", 0)], response)))
        log("#{type} message sent to nchan to #{num_subscribers} subscriber(s) (code: #{response.status_code})")
    else
        log("ERROR: got code #{response.status_code} while sending #{type} message to nchan: #{response.status_message}")
    end
end

def send_message_to_nchan(type, message, ~delay=0.)
    if delay == 0. then
        _send_message_to_nchan_http_post(type, message)
    else
        log("Delaying #{type} message by #{delay} seconds")
        thread.run(fast=false, delay=delay, fun() -> _send_message_to_nchan_http_post(type, message))
    end
end

def send_metadata_to_nchan(m)
    message = json()
    message.add("title", metadata.title(m))
    send_message_to_nchan("metadata", message, delay=METADATA_MESSAGE_DELAY)
end

radio.on_metadata(send_metadata_to_nchan)

radio = mksafe(radio)
output.dummy(radio)
output = output.icecast(
    %mp3,
    host='icecast',
    port=8888,
    user='source',
    password=PASSWORD,
    mount="radio",
    on_error=fun(e) -> begin
        log("ERROR: error connecting to http://source:#{PASSWORD}@icecast:8888/radio: #{e}")
        1.
    end,
    radio,
)
