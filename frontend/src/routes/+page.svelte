<script>
  let bioDialog

  const openEmail = ({ addr, tld, domain }) => {
    const email = `${tld}.${domain}@${addr}:otliam`.split("").reverse().join("")
    window.open(email, "_blank")
  }
</script>

<dialog class="modal" bind:this={bioDialog}>
  <div class="modal-box w-[97vw] max-w-5xl md:px-4 sm:px-3 px-2">
    <form method="dialog">
      <button class="btn btn-sm md:btn-md md:text-xl btn-circle btn-ghost absolute right-2 top-2">✕</button>
    </form>
    <h3 class="font-bold text-3xl italic text-center mb-1.5 md:mb-3 underline">Bio</h3>

    <article class="text-indent overflow-hidden">
      <enhanced:img
        alt=""
        src="$lib/assets/images/headshot.jpg"
        style="--custom-spin-duration: 33.711s; --custom-spin-direction: reverse"
        class="hidden md:block mx-auto sm:float-right h-2/3 w-2/3 sm:h-1/3 sm:w-1/3 lg:h-1/4 lg:w-1/4 sm:ml-3 rounded-full border-4 border-secondary animate-spin-custom select-none drag-none"
      />

      <p>
        David Cooper is a human train wreck and Canadian living in New York City. His extensive broadcasting credentials
        include having his interview requests denied by celebrities, world leaders, and restroom attendants.
      </p>
      <p>
        After growing up in Toronto, David fled to San Francisco where he was introduced to radio almost by accident:
        While dabbling in stand-up comedy, David wandered into a radio station to promote one of his shows. Something
        terrible clicked that day and there was no turning back.
      </p>

      <enhanced:img
        alt=""
        src="$lib/assets/images/david-bmir.jpg"
        style="--custom-spin-duration: 31.13s; --custom-spin-direction: normal"
        class="mx-auto sm:float-left h-2/3 w-2/3 sm:h-1/3 sm:w-1/3 lg:h-1/4 lg:w-1/4 sm:mr-5 rounded-full border-8 border-secondary animate-spin-custom select-none drag-none"
      />

      <p>
        Since 2016, David has hosted various radio shows on independent stations around San Francisco, including a wacky
        call-in program called <a href="#TODO">This Is Going Well, I Think</a> (visible from a coffee shop window). His
        experiment with a phone booth in the desert was showcased in
        <a href="#TODO">an NPR episode</a> (long story). And at the end of 2020, David quit his lucrative career as a
        software engineer to pursue radio opportunities full-time &ldquo;like an idiot&rdquo; (a direct quote from his
        overbearing Jewish mother). Addressing <a href="#">David&rsquo;s mother directly in a 2022 interview</a>, the
        mayor of Toronto stated that he&rsquo;s proud of David for his minor contributions to overnight radio.
      </p>
      <p>
        David&rsquo;s on-air style oscillates between frenzied comedy and confession-booth sincerity, blurring the lines
        between his personal relationships and on-air ones in a way both intimate and (arguably) intrusive. He can be
        heard nightly as contributor on the nationally syndicated
        <a href="#">Newstalk Tonight with Jim Richards</a> on iHeartRadio Canada&rsquo;s Talk Network; doing the
        occasional
        <a href="#">guest spot on WFMU</a>
        in New York/New Jersey; and every year in the Nevada Desert on
        <a href="#">Burning Man Information Radio (BMIR) 94.5 FM</a>, where he has interviewed everyone from
        stripper-clowns to George Stroumboulopoulos.
      </p>

      <div class="clear-both"></div>
    </article>
  </div>
  <form method="dialog" class="modal-backdrop">
    <button>close</button>
  </form>
</dialog>

<div class="hero min-h-screen">
  <div class="flex-col hero-content max-w-screen-lg lg:flex-row-reverse lg:rounded-3xl">
    <div class="flex flex-col lg:flex-col-reverse gap-y-3 items-center">
      <h1 class="italic text-xl md:text-2xl lg:text-xl font-bold">
        David Cooper <small class="font-normal">Radio Personality</small>
      </h1>
      <div class="overflow-hidden">
        <enhanced:img
          src="$lib/assets/images/headshot.jpg"
          style="--custom-spin-duration: 4000ms"
          alt=""
          class="max-w-[12rem] sm:max-w-xs lg:max-w-sm rounded-full border-8 border-secondary animate-spin-custom select-none drag-none"
        />
      </div>
    </div>
    <div>
      <h2 class="mb-6 sm:mb-8 lg:mb-10 text-2xl sm:text-3xl lg:text-5xl font-bold italic text-center lg:text-left">
        Welcome to <span class="text-accent underline underline-wavy animate-spin">jew.pizza</span>
      </h2>
      <p
        class="md:text-indent mb-1.5 sm:mb-2 lg:mb-2 mx-2 lg:mx-0 text-sm sm:text-base lg:text-lg"
        x-data="placeholder"
      >
        Here is my special website. Check out my <span class="font-bold">podcast</span>
        that releases <span class="font-bold"><span class="underline"> every weekday</span></span> called
        <a
          class="link link-primary link-hover umami--click--tigwit-podcast font-bold"
          target="_blank"
          href="https://shows.acast.com/this-is-going-well-i-think"
        >
          <span class="italic">This Is Going Well, I Think with David Cooper</span></a
        >.
      </p>
      <p class="md:text-indent mb-1.5 sm:mb-2 mx-2 lg:mx-0 text-sm sm:text-base lg:text-lg">
        I <span class="font-bold">descend on the desert every year</span> for the
        <a href="https://burningman.org/" target="_blank" class="link link-primary link-hover umami--click--burningman">
          Burning Man
        </a>
        event where <span class="font-bold">I'm an on-air personality</span> on
        <span class="font-bold"
          ><a href="https://bmir.org/" target="_blank" class="link link-primary link-hover umami--click--bmir"
            >Burning Man Information Radio</a
          ></span
        > (BMIR 94.5 FM).
      </p>
      <p class="md:text-indent mx-2 lg:mx-0 text-sm sm:text-base lg:text-lg">
        You can also <span class="font-bold">listen to my show</span>
        <a
          class="link link-primary link-hover font-bold umami--click--wfmu"
          href="https://www.wfmu.org/playlists/WD"
          target="_blank"
        >
          <span class="italic">That Went Well, I Think</span> on WFMU</a
        >.
      </p>
      <div class="grid grid-cols-1 sm:grid-cols-4 gap-1.5 lg:gap-1 mt-5 select-none">
        <a
          class="btn btn-neutral btn-rounded border-0 umami--click--twitter"
          href="https://twitter.com/dtcooper"
          target="_blank"
        >
          <span class="icon-[mdi--twitter] h-6 w-6" /> Twitter
        </a>
        <a
          class="btn btn-neutral btn-rounded border-0 umami--click--intagram"
          href="https://instagram.com/dtcooper"
          target="_blank"
        >
          <span class="icon-[mdi--instagram] h-6 w-6" /> Instgram
        </a>
        <button class="btn btn-neutral btn-rounded border-0 umami--click--bio" on:click={() => bioDialog.showModal()}>
          <span class="icon-[mdi--biography] h-6 w-6" /> Bio
        </button>
        <button
          class="btn btn-neutral btn-rounded border-0 umami--click--email"
          data-addr="divad"
          data-tld="azzip"
          data-domain="wej"
          on:click={(e) => openEmail({ ...e.target.dataset })}
        >
          <span class="icon-[mdi--email-outline] h-6 w-6" /> Email
        </button>
      </div>
    </div>
  </div>
</div>
