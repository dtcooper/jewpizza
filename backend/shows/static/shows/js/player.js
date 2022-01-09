/* global Alpine, WaveSurfer */

document.addEventListener('alpine:init', () => {
  Alpine.data('episodePlayer', (url, peaks, duration) => ({
    init () {
      this.playing = false
      this.wavesurfer = WaveSurfer.create({
        container: this.$refs.wavesurfer,
        backend: 'MediaElement',
        barWidth: 3,
        barMinHeight: 1,
        responsive: true,
        normalize: true,
        progressColor: '#f10486',
        waveColor: '#fc49ab',
        plugins: [
          WaveSurfer.timeline.create({
            container: this.$refs.timeline,
          })
        ]
      })
      this.wavesurfer.load(this.$refs.audio, peaks)
    },
    play () {
      this.playing = true
      this.wavesurfer.play()
    },
    stop () {
      this.playing = false
      this.wavesurfer.pause()
    },
    destroy () {
      this.wavesurfer.destroy()
    }
  }))
})
