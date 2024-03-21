<script>
  import "../app.css"

  import { PUBLIC_DOMAIN_NAME as DOMAIN_NAME, PUBLIC_UMAMI_WEBSITE_ID as UMAMI_WEBSITE_ID } from "$env/static/public"
</script>

<svelte:head>
  {#if UMAMI_WEBSITE_ID}
    <script defer src="https://a.{DOMAIN_NAME}/s.js" data-website-id={UMAMI_WEBSITE_ID}></script>
  {/if}
</svelte:head>

<slot />
