/* global DATA */
import Alpine from 'alpinejs'
import Navigo from 'navigo'

(() => {
  let router, contentScrollerDiv, contentDiv

  // Send JS Errors to backend
  async function reportError (title, detail, filename) {
    await window.fetch(DATA.jsErrorURL, {
      headers: { 'X-CSRFToken': DATA.csrfToken, 'Content-Type': 'application/json' },
      method: 'POST',
      credentials: 'same-origin',
      body: JSON.stringify({
        url: window.location.href,
        title,
        detail,
        filename: filename || null
      })
    })
  }

  window.addEventListener('error', async (event) => {
    let detail = event.message
    if (event.error && event.error.stack) {
      detail = event.error.stack
    }
    await reportError(event.message, detail, event.filename)
  })

  window.addEventListener('unhandledrejection', async (event) => {
    if (event.reason) {
      await reportError(event.reason.toString(), event.reason.stack)
    }
  })

  // Decode my email address
  let jank = DATA.encodedEmail
  let email = ''
  for (let i = 0; jank.length > 0; i++) {
    email += jank.charAt(i)
    jank = jank.substr(i + 1)
  }

  window.emailAddress = email

  // Main entrypoint for SPA, load a URL
  const loadURL = async function (url, data) {
    Alpine.store('menuOpen', false)
    const store = Alpine.store('page')
    let json = null
    let response = null
    let debugResponse = null
    store.loading = true

    data = data || {}
    data.headers = { Accept: 'application/json' }
    data.credentials = 'same-origin'

    try {
      response = await window.fetch(url, data)
      if (DATA.debug) {
        debugResponse = response.clone()
      }
      json = await response.json()

      if (DATA.debug && json.status >= 400) {
        document.open()
        const pre = document.createElement('pre')
        pre.textContent = json.content
        document.append(pre)
        document.close()
        return
      }
    } catch (err) {
      if (DATA.debug || DATA.isSuperuser) {
        console.error(`An error occurred while fetching ${url}`)
        console.error('data:', data)
        console.error('error:', err)
        if (debugResponse) {
          console.error('Response body...')
          console.error(await debugResponse.text())
        }
      }
      router._setCurrent(null) // Force reloads (allow retries)
      store.loading = false
      Alpine.store('messages', [{ level: 'error', message: 'An error occurred. Please try refreshing the page.' }])
      return
    }

    if (json.redirect) {
      router._setCurrent(null) // Force reloads if we never leave the page
      router.navigate(json.redirect)
    } else {
      document.title = (DATA.debug ? '[dev] ' : '') + (json.title ? `${json.title} - ` : '') + 'jew.pizza'
      store.current = url
      contentDiv.innerHTML = json.content

      store.loading = false
      Alpine.store('messages', json.messages)
      setTimeout(() => { contentScrollerDiv.scrollTop = 0 }, 2)
    }
  }

  // @submit function to use SPA instead of an actual POST
  window.formSubmit = async function (e) {
    e.preventDefault()
    const url = e.target.getAttribute('action')
    await loadURL(url, {
      method: 'POST',
      body: new window.FormData(e.target)
    })
  }

  document.addEventListener('alpine:init', () => {
    window.history.scrollRestoration = 'manual'

    contentScrollerDiv = document.getElementById('content-scroller')
    contentDiv = document.getElementById('content')
    router = new Navigo('/')
    window.navigate = router.navigate

    router.on('*', async ({ url, ...args }) => {
      url = `/${url}`
      if (url !== '/') {
        url = `${url}/`
      }
      await loadURL(url)
    })

    // Override <a> click events and send to navigo
    document.addEventListener('click', (e) => {
      for (let anchor = e.target; anchor && anchor !== this; anchor = anchor.parentNode) {
        if (anchor.tagName === 'A') {
          const href = anchor.getAttribute('href')
          // Open http/mailto/tel links as normal
          if (href.match(/^(?:https?|mailto|tel):/)) {
            if (window.location.host !== anchor.host) {
              // Dynamically add target=_blank for remote links
              anchor.setAttribute('target', '_blank')
            }
          } else {
            // Otherwise, intercept and route via navigo
            e.preventDefault()
            e.stopPropagation()
            router._setCurrent(null) // Force reloads if we never leave the page
            router.navigate(href)
          }
        }
      }
    }, false)

    Alpine.store('page', {
      current: DATA.currentPage,
      loading: false
    })
    Alpine.store('menuOpen', false)
    Alpine.store('messages', DATA.messages)

    // XXX Test eventsource
    if (DATA.playerEnabled) {
      Alpine.store('sse', {})

      const eventsource = window.eventsource = new window.EventSource(DATA.sseURL)
      eventsource.addEventListener('message', function (e) {
        const data = JSON.parse(e.data)
        Alpine.store('sse')[data.type] = data.message
        if (DATA.debug) {
          console.log(`Recieved ${data.type} SSE message at ${new Date()}: ${JSON.stringify(data.type, null, 2)}`)
        }
      })
    }
  })
})()
