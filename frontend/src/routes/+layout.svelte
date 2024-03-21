<script>
  import "../app.css"

  import { PUBLIC_UMAMI_WEBSITE_ID, PUBLIC_DOMAIN_NAME } from '$env/static/public';
</script>

<svelte:head>
  {#if PUBLIC_UMAMI_WEBSITE_ID}
    <script defer src="https://a.{PUBLIC_DOMAIN_NAME}/s.js" data-website-id={PUBLIC_UMAMI_WEBSITE_ID}></script>
  {/if}
</svelte:head>

<slot />
