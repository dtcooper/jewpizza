import WaveSurfer from 'wavesurfer.js'
import TimelinePlugin from 'wavesurfer.js/dist/plugin/wavesurfer.timeline'
import CursorPlugin from 'wavesurfer.js/dist/plugin/wavesurfer.cursor'
import Alpine from 'alpinejs'

import tailwindConfig from '../tailwind.config'

const theme = tailwindConfig.daisyui.themes[0].jewpizza

document.addEventListener('alpine:init', () => {
  Alpine.data('episodePlayer', (url, peaks, duration) => ({
    init () {
      this.playing = false
      this.wavesurfer = WaveSurfer.create({
        container: this.$refs.wavesurfer,
        backend: 'MediaElement',
        barWidth: 3,
        barMinHeight: 1,
        barGap: 1.5,
        height: 120,
        responsive: true,
        normalize: true,
        partialRender: true,
        progressColor: theme['primary-focus'],
        waveColor: theme.primary,
        cursorColor: theme['secondary-focus'],
        cursorWidth: 3,
        plugins: [
          CursorPlugin.create({
            width: '1px',
            color: theme['base-content'],
            showTime: true,
            opacity: 1,
            customShowTimeStyle: {
              'font-family': '"Space Mono", "Courier New", monospace',
              'background-color': '#000',
              opacity: 1,
              color: '#fff',
              padding: '2px',
              'font-size': '12px'
            },
            formatTimeCallback (seconds) {
              const hours = Math.floor(seconds / 60 / 60)
              const minutes = Math.floor((seconds % (60 * 60)) / 60)
              const secondsStr = Math.floor(seconds % 60).toString().padStart(2, '0')
              if (hours) {
                return `${hours}:${minutes.toString().padStart(2, '0')}:${secondsStr}`
              } else {
                return `${minutes}:${secondsStr}`
              }
            }
          }),
          TimelinePlugin.create({
            container: this.$refs.timeline
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
