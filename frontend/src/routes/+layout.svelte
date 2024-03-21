<script>
  import "../app.css"

  import { env } from "$env/dynamic/public"
</script>

<svelte:head>
  {#if env.PUBLIC_UMAMI_WEBSITE_ID}
    <script defer src="https://a.{env.PUBLIC_DOMAIN_NAME}/s.js" data-website-id={env.PUBLIC_UMAMI_WEBSITE_ID}></script>
  {/if}
</svelte:head>

<slot />
