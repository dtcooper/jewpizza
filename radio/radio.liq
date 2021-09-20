
BUFFER = 5.
MAX = 10.

radio = input.http('http://bmir-ice.streamguys.com/live', max_buffer=MAX)

output.icecast(
    %mp3,
    host='icecast',
    mount="radio",
    mksafe(radio),
)
