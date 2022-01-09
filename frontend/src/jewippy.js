/* global DATA */
import Alpine from 'alpinejs'

if (DATA.enabledJewippy) {
  document.addEventListener('alpine:init', () => {
    let component = null

    Alpine.store('jewippy', {
      open: false,
      get setImg () {
        return function () { return component.setImg.apply(component, arguments) }
      },
      get queueImg () {
        return function () { return component.queueImg.apply(component, arguments) }
      }
    })

    Alpine.data('jewippy', function () { // Use function() here to bind $persist
      return {
        imgs: {},
        lengths: {},
        choices: new Set(),
        current: 'idle',
        open: this.$persist(true).as('jewippy-open'),
        imageType: this.$persist(null).as('jewippy-image-type'),
        bubbleOpen: true,
        idleLoaded: false,
        allLoaded: false,
        timeout: null,
        animationQueue: [],
        init () {
          if (this.imageType) {
            this._debug(`Loading with ${this.imageType} ($persist)`)
            this.initAfterImageDetection()
          } else {
            const webp = new window.Image()
            webp.onload = () => {
              if ((webp.width > 0) && (webp.height > 0)) {
                this.imageType = 'webp'
              } else {
                this.imageType = 'gif'
              }
              this._debug(`Loading with ${this.imageType} (onload)`)
              this.initAfterImageDetection()
            }
            webp.onerror = () => {
              this.imageType = 'gif'
              this._debug(`Loading with ${this.imageType} (onerror)`)
              this.initAfterImageDetection()
            }
            webp.src = DATA.jewippyTestWEBP
          }
        },
        initAfterImageDetection () {
          component = this
          const store = Alpine.store('jewippy')
          store.open = this.open
          this.$watch('open', (value) => { store.open = value })

          let numLoaded = 0
          const jewippyGifs = Array.from(DATA.jewippyGifs)
          const numToLoad = jewippyGifs.length

          const first = jewippyGifs.shift() // First load idle gif
          const firstImg = new window.Image()
          firstImg.addEventListener('load', () => {
            numLoaded += 1
            this.idleLoaded = true
            this.setImg(first.name)
            this._debug(`${first.name} image loaded`)

            for (const gif of jewippyGifs) {
              const img = new window.Image()
              img.addEventListener('load', () => {
                this._debug(`${gif.name} loaded`)
                numLoaded += 1
                if (numLoaded === numToLoad) {
                  this.allLoaded = true
                  this.queueImg(['idle', 'idleAlt'], true)
                  this.openBubbleDemo() // XXX
                }
              })
              img.src = gif[this.imageType]
              this.imgs[gif.name] = img
              this.lengths[gif.name] = gif.length
              this.choices.add(gif.name)
            }
          })

          firstImg.src = first[this.imageType]
          this.imgs[first.name] = firstImg
          this.lengths[first.name] = first.length
          this.choices.add(first.name)
        },
        _debug (str) {
          // XXX remove me
          if (DATA.debug) {
            const d = new Date()
            const h = `${d.getHours()}`.padStart(2, '0')
            const m = `${d.getMinutes()}`.padStart(2, '0')
            const s = `${d.getSeconds()}`.padStart(2, '0')
            const ms = `${d.getMilliseconds()}`.padStart(3, '0')
            console.log(`jewippy: ${h}:${m}:${s}.${ms} ${str}`)
          }
        },
        _timeoutFunc () {
          let hook = null
          if (this.allLoaded) {
            if (this.animationQueue.length) {
              const item = this.animationQueue.pop()
              this.current = item.name
              hook = item.hook
            }
          }
          this._debug(`timeout func ran setting img to: ${JSON.stringify(this.current)}`)
          this.setImg(this.current, false, hook)
        },
        _resolveName (name) {
          if (Array.isArray(name)) {
            name = name[Math.floor(Math.random() * name.length)]
          }
          return name
        },
        setImg (name, emptyQueue, hook) {
          clearTimeout(this.timeout)
          if (emptyQueue) {
            this.animationQueue = []
          }
          if (hook) {
            hook()
          }
          this.current = name
          const actual = this._resolveName(name)
          this._debug(`setImg(${JSON.stringify(name)} / actual=${actual}) (emptyQueue=${emptyQueue || false}) (queue=${JSON.stringify(this.animationQueue)})`)
          this.$refs.jewippyGif.src = this.imgs[actual].src
          this.timeout = setTimeout(() => this._timeoutFunc(), this.lengths[actual])
        },
        queueImg (name, emptyQueue, hook) {
          if ((Array.isArray(name) && name.every((val) => this.choices.has(val))) || this.choices.has(name)) {
            if (emptyQueue) {
              this.animationQueue = []
            }
            this.animationQueue.push({ name: name, hook: hook })
            this._debug(`adding to animation queue: [${JSON.stringify(name)}] (emptyQueue=${emptyQueue || false}) (queue=${JSON.stringify(this.animationQueue)})`)
          } else if (DATA.debug) {
            console.error(`invalid animation(s): ${JSON.stringify(name)}. Valid choices: ${JSON.stringify([...this.choices])}`)
          }
        },
        bubbleDemoHTML: '',
        bubbleDemoLink: null,
        bubbleDemoClick () {
          this.setImg('explode')
          this.queueImg(['idle', 'idleAlt'], true)
          window.navigate(this.bubbleDemoLink)
          this.bubbleDemoClose(7500)
        },
        bubbleDemoClickMinimize (animation) {
          this.bubbleDemoClose(12500)
          this.setImg(animation || 'melting')
          this.queueImg(['idle', 'idleAlt'], true)
        },
        bubbleDemoClose (reopenTimeout) {
          this.bubbleOpen = false
          this._debug(`Closing bubble for ${reopenTimeout / 1000}s`)
          setTimeout(() => this.openBubbleDemo(), reopenTimeout)
        },
        openBubbleDemo () {
          const links = Array.from(DATA.bubbleDemoNavLinks)
          const currentPage = links.findIndex((link) => link[1] === Alpine.store('page').current)
          if (currentPage > -1) {
            links.splice(currentPage, 1)
          }
          const link = links[Math.floor(Math.random() * links.length)]
          this.bubbleDemoHTML = `Have you seen the <strong>${link[0]}</strong> page? Check it out!`
          this.bubbleDemoLink = link[1]
          this._debug(`Opening bubble demo with ${link[0]} link`)
          this.bubbleOpen = true
          // Doesn't want to scroll immediately, so set a 10ms delay
          setTimeout(() => { document.getElementById('jewippy-scroller').scrollTop = 0 }, 10)
        }
      }
    })
  })
}
