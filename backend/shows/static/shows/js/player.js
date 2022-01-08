/* global Alpine, WaveSurfer */

document.addEventListener('alpine:init', () => {
  Alpine.data('episodePlayer', (assetUrl) => ({
    init () {
      this.playing = false
      this.wavesurfer = WaveSurfer.create({
        container: this.$refs.wavesurfer,
        barWidth: 3,
        barMinHeight: 1,
        normalize: true,
        progressColor: '#f10486',
        waveColor: '#fc49ab'
      })
      this.wavesurfer.load(assetUrl)
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
