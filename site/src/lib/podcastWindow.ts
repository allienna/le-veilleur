// Podcast episodes' audio lives on a GCS bucket with a 30-day lifecycle deletion rule (see
// infra/podcast.tf); the site's podcast page and RSS feed must never link to an episode whose
// audio has already been purged. Shared here so the page and the feed can't drift apart.
export function withinRetentionWindow(date: Date, days = 30): boolean {
  const cutoff = Date.now() - days * 24 * 60 * 60 * 1000;
  return date.getTime() >= cutoff;
}
