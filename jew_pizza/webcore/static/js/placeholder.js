document.addEventListener('alpine:init', () => {
    Alpine.data('obfuscatedEmail', () => ({
      jank: 'mzaDJiq2blRb6Kt6IEBkog1xFTK:C1sXQz4dyGlwp2cWa6XCJwQRVkvBSdLDSzzc5i7zuCyxRtXZXdy2ZXu92mWpmB@oVuskLGzw3myjjr'
        + 'R5ZEFwmqBgLj9e3Iebb7lZjsm4s3uw3rQw6nqH3Hrqtsdg.6zfrMHUsUbDhdB9vspQXw48WIi5FUaZco0LkiEX5ZCaPBCQ1GkM5vafAzEBeL'
        + 'xvwLHGOIOcGzbzl0zEFUMLKdYxWa0BZKWdmgg2a9SW8nreNfJ2cOUctNnsYBe',
      email() {
        let email = ''
        let jank = this.jank
        for (let i = 0; jank.length > 0; i++) {
          email += jank.charAt(i);
          jank = jank.substr(i + 1);
        }
        return email
      }
    }))
    Alpine.data('localizedTimeBlurb', () => ({
      userTZ: window.ENV.userTZ,
      showNightBefore: false,
      showNight: false,
      nextShowStart: null,
      nextShowEnd: null,
      weekStart: null,
      weekEnd: null,
      prettyDay(dt) {
        switch (dt.day()) {
          case 2:
            return 'Tues'
          case 3:
            return 'Weds'
          case 4:
            return 'Thurs'
          default:
            return dt.format('ddd')
        }
      },
      showTime() {
        let [displayWeekStart, displayWeekEnd] = [this.weekStart, this.weekEnd]
        if (this.showNightBefore) {
          [displayWeekStart, displayWeekEnd] = [moment(this.weekStart).subtract(1, 'days'), moment(this.weekEnd).subtract(1, 'days')]
        }

        s = `${this.prettyDay(displayWeekStart)} to ${this.prettyDay(displayWeekEnd)}`
        if (this.showNight) {
          s += ' nights'
        }
        return `${s} at ${this.nextShowStart.format('h:mma')}-${this.nextShowEnd.format('h:mma')} ${this.nextShowStart.format('z')}`
      },
      showTechnicalTime() {
        if (this.showNightBefore) {
          return ` (technically ${this.prettyDay(this.weekStart)} to ${this.prettyDay(this.weekEnd)} mornings)`
        } else {
          return ''
        }
      },
      init() {
        this.nextShowStart = moment.tz('US/Eastern')

        if (this.nextShowStart.isAfter(moment(this.nextShowStart).hour(2).minute(30).second(0))) {
          // if it's after 2:30 at night, clamp to tomorrow
          this.nextShowStart.add(1, 'days')
        }

        // clamp to next Monday if Sat or Sun
        if (this.nextShowStart.day() < 1 || this.nextShowStart.day() > 5) {
          this.nextShowStart.add(this.nextShowStart.day() == 0 ? 1 : 2, 'days')
        }

        // Set to start time
        this.nextShowStart.hour(1).minute(30).second(0)
        this.weekStart = moment(this.nextShowStart).day(1).tz(this.userTZ)
        this.weekEnd = moment(this.nextShowStart).day(5).tz(this.userTZ)

        // Show night before warning if it's below 3:30am local time
        this.nextShowStart.tz(this.userTZ)
        if (this.nextShowStart.isSameOrBefore(moment(this.nextShowStart).hour(3).minute(30).second(0))) {
          this.showNightBefore = true
          this.showNight = true
        } else if (this.nextShowStart.isSameOrAfter(moment(this.nextShowStart).hour(17).minute(0).second(0))) {
          // only show "nights" if show happens after 5pm local time
          this.showNight = true
        }

        this.nextShowEnd = moment(this.nextShowStart).add(1, 'hours')
      }
    }))
  });