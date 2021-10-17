/* global Alpine, DATA */

document.addEventListener('alpine:init', () => {
  const animationBufferMS = 0.25

  Alpine.data('jewippy', function () { // Use function() here to bind $persist
    return {
      imgs: {},
      lengths: {},
      choices: new Set(),
      current: 'idle',
      open: this.$persist(true),
      imgStyle: this.$persist(null),
      idleLoaded: false,
      allLoaded: false,
      timeout: null,
      animationQueue: [],
      init () {
        if (this.imgStyle === null) {
          const apngTest = new window.Image()
          const apngTestCtx = document.createElement('canvas').getContext('2d')
          apngTest.addEventListener('load', () => {
            apngTestCtx.drawImage(apngTest, 0, 0)
            this.imgStyle = (apngTestCtx.getImageData(0, 0, 1, 1).data[3] === 0) ? 'apng' : 'gif'
            this.initWithImages()
          })
          apngTest.src = DATA.apngTestUrl
        } else {
          this.initWithImages()
        }
      },
      initWithImages () {
        let numLoaded = 0
        const numToLoad = Object.keys(DATA.jewippyGifs).length
        for (const gif of DATA.jewippyGifs) {
          const img = new window.Image()
          img.addEventListener('load', () => {
            numLoaded += 1
            if (gif.name === 'idle') {
              this.idleLoaded = true
              this.setImg('idle')
            }
            if (numLoaded === numToLoad) {
              this.allLoaded = true
              this.queueImg(['idle', 'idleAlt'], true)
            }
          })
          img.src = gif[this.imgStyle]
          this.imgs[gif.name] = img
          this.lengths[gif.name] = gif.length
          this.choices.add(gif.name)
        }
      },
      _debug (str) {
        // XXX remove me
        if (DATA.debug) {
          const d = new Date()
          const h = `${d.getHours()}`.padStart(2, '0')
          const m = `${d.getMinutes()}`.padStart(2, '0')
          const s = `${d.getSeconds()}`.padStart(2, '0')
          const ms = `${d.getMilliseconds()}`.padStart(3, '0')
          console.log(`${h}:${m}:${s}.${ms} ${str}`)
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
        this.timeout = setTimeout(() => this._timeoutFunc(), this.lengths[actual] - animationBufferMS)
      },
      queueImg (name, emptyQueue, hook) {
        if ((Array.isArray(name) && name.every((val) => this.choices.has(val))) || this.choices.has(name)) {
          if (emptyQueue) {
            this.animationQueue = []
          }
          this.animationQueue.push({ name: name, hook: hook })
          this._debug(`adding to animation queue: [${JSON.stringify(name)}] (emptyQueue=${emptyQueue || false}) (queue=${JSON.stringify(this.animationQueue)})`)
        } else if (DATA.debug) {
          console.error(`invalid animation(s): [${JSON.stringify(name)}]`)
        }
      },
      testClick () {
        if (this.allLoaded) {
          this.queueImg(['idle', 'idleAlt'], true)
          this.queueImg('xanaxRain', false)
        }
      }
    }
  })
})
