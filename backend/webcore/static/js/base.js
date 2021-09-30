/* global DATA, Alpine, Navigo */

(() => {
  const getPage = async function (url) {
    const data = await (await window.fetch(url, { headers: { 'Content-Type': 'application/json' } })).json()
    return data.content
  }

  document.addEventListener('alpine:init', () => {
    const router = new Navigo('/')
    const contentElem = document.getElementById('content')
    router.on('*', async ({ url }) => {
      const store = Alpine.store('page')
      store.loading = true

      url = `/${url}`
      if (url !== '/') {
        url = `${url}/`
      }
      const html = await getPage(url)
      document.title = (DATA.debug ? '[dev] ' : '') + (DATA.nav_links[url] || 'jew.pizza')
      store.current = url
      contentElem.innerHTML = html
      store.loading = false
      router.updatePageLinks()
    })
    Alpine.store('page', {
      current: DATA.current_page,
      loading: false
    })
  })
})()
