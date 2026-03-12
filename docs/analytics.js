// analytics.js
(function () {
  // Only run if not on localhost/development
  if (
    window.location.hostname === "localhost" ||
    window.location.hostname === "127.0.0.1"
  ) {
    return;
  }

  const SUPABASE_URL = "https://wxanombcqzsbecwg.supabase.co";
  const SUPABASE_ANON_KEY = "sb_publishable_8sfuqDwp6Z08LkRIcgqPFA_Rm4cNh4Y";

  const data = {
    path: window.location.pathname || "/",
    user_agent: navigator.userAgent,
    language: navigator.language,
    screen_width: window.screen.width,
    screen_height: window.screen.height,
    timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
  };

  fetch(`${SUPABASE_URL}/rest/v1/page_views`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      apikey: SUPABASE_ANON_KEY,
      Authorization: `Bearer ${SUPABASE_ANON_KEY}`,
    },
    body: JSON.stringify(data),
  }).catch((err) => console.error("Analytics error:", err));
})();
