# radio

jingle = single(fallible=false, '/jingle.mp3')

output.harbor(
    %wav(duration=0., stereo=true, channels=2, samplesize=16, header=true),
    mount='radio',
    # Since we're encoding WAV it's much larger. This may prevent upstreams reverting to failsafe intermittently.
    burst=65534 * 16,
    buffer=327675 * 16,
    jingle,
)
