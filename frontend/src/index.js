import Alpine from 'alpinejs'
import persist from '@alpinejs/persist'

import './index'
import './base'
import './home'
import './player'
import './jewippy'

window.Alpine = Alpine
Alpine.plugin(persist)
Alpine.start()
