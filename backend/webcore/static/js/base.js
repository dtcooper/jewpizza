/* global Alpine, DATA */

document.addEventListener('alpine:init', () => {
  Alpine.data('obfuscatedEmail', () => ({
    jank: 'mzaDJiq2blRb6Kt6IEBkog1xFTK:C1sXQz4dyGlwp2cWa6XCJwQRVkvBSdLDSzzc5i7zuCyxRtXZXdy2ZXu92mWpmB@oVuskLGzw3myjjr' +
        'R5ZEFwmqBgLj9e3Iebb7lZjsm4s3uw3rQw6nqH3Hrqtsdg.6zfrMHUsUbDhdB9vspQXw48WIi5FUaZco0LkiEX5ZCaPBCQ1GkM5vafAzEBeL' +
        'xvwLHGOIOcGzbzl0zEFUMLKdYxWa0BZKWdmgg2a9SW8nreNfJ2cOUctNnsYBe',
    email () {
      let email = ''
      let jank = this.jank
      for (let i = 0; jank.length > 0; i++) {
        email += jank.charAt(i)
        jank = jank.substr(i + 1)
      }
      return email
    }
  }))

  Alpine.data('hero', () => ({
    showHero: DATA.force_hero ? true : !window.localStorage.getItem('hideHero'),
    init () {
      if (this.showHero) {
        const navbar = document.getElementById('navbar')
        const update = () => {
          if (navbar.getBoundingClientRect().y <= 0) {
            window.localStorage.setItem('hideHero', '1')
            window.removeEventListener('scroll', update)
            window.removeEventListener('resize', update)
          }
        }

        window.addEventListener('scroll', update)
        window.addEventListener('resize', update)
        update()
      }
    }
  }))
})
