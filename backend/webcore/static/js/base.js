/* global DATA, Alpine, Navigo */

(() => {
  let router

  const getCookie = function (name) {
    let cookieValue = null
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';')
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim()
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
          break
        }
      }
    }
    return cookieValue
  }

  let jank = "dNa1TvK\u000b3iJ@@Ydtee@W@Ug(8=\\jI'AJ8H6e@0DXDM(CwcJ,tTnl-_.`\\#CRm`UWmpf<}pL@h@p&Ki@Ji3Lg@d3r6Rz%o@l5xxj,|M\nDzo\nH_-\u000b;RU\tpu*zap0kDvl9gHhb@5Mb"
  let email = ''
  for (let i = 0; jank.length > 0; i++) {
    email += jank.charAt(i)
    jank = jank.substr(i + 1)
  }

  window.emailAddress = email

  const loadURL = async function (url, data) {
    Alpine.store('menuOpen', false)
    const store = Alpine.store('page')
    let json = null
    let response = null
    let debugResponse = null
    store.loading = true

    data = data || {}
    data.headers = { Accept: 'application/json', 'X-CSRFToken': getCookie('csrftoken') }

    try {
      response = await window.fetch(url, data)
      if (DATA.debug) {
        debugResponse = response.clone()
      }
      json = await response.json()
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
      Alpine.store('messages', [{ level: 'error', message: 'An error occurred. Please try loading the page again.' }])
      return
    }

    if (json.redirect) {
      router._setCurrent(null) // Force reloads
      router.navigate(json.redirect)
    } else {
      document.title = (DATA.debug ? '[dev] ' : '') + json.title
      store.current = url
      document.getElementById('content').innerHTML = json.content

      store.loading = false
      Alpine.store('messages', json.messages)
      router.updatePageLinks()
      document.getElementById('content-scroller').scrollTop = 0
    }
  }

  window.formSubmit = async function (e) {
    e.preventDefault()
    console.log(e.target)
    const url = e.target.getAttribute('action')
    await loadURL(url, {
      method: 'POST',
      credentials: 'same-origin',
      body: new window.FormData(e.target)
    })
  }

  document.addEventListener('alpine:init', () => {
    router = new Navigo('/')
    window.router = router

    router.on('*', async ({ url, ...args }) => {
      url = `/${url}`
      if (url !== '/') {
        url = `${url}/`
      }
      await loadURL(url)
    })

    Alpine.store('page', {
      current: DATA.currentPage,
      loading: false
    })
    Alpine.store('menuOpen', false)
    Alpine.store('messages', DATA.messages)
  })
})()
