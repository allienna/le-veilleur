import type { APIContext } from 'astro';
import { getCollection } from 'astro:content';
import { withinRetentionWindow } from '../lib/podcastWindow';

// Hand-written rather than through @astrojs/rss's helper: its RSSFeedItem shape has no native
// `enclosure`/`itunes:duration` support, which a podcast-app subscription needs to find the
// actual audio file. Escaping is done manually since this is the only writer of this feed.
function escapeXml(value: string): string {
  return value
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}

export async function GET(context: APIContext) {
  const episodes = (await getCollection('podcasts'))
    .filter((episode) => withinRetentionWindow(episode.data.date))
    .sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());

  const siteUrl = context.site ?? new URL('https://allienna.github.io');
  const channelLink = new URL('podcasts/', siteUrl).toString();

  const items = episodes
    .map((episode) => {
      const title = escapeXml(episode.data.title);
      const audioUrl = escapeXml(episode.data.audioUrl);
      const duration = episode.data.durationSeconds;
      return `
    <item>
      <title>${title}</title>
      <pubDate>${episode.data.date.toUTCString()}</pubDate>
      <enclosure url="${audioUrl}" type="audio/mpeg"${duration ? ` length="${duration}"` : ''} />
      ${duration ? `<itunes:duration>${duration}</itunes:duration>` : ''}
      <guid isPermaLink="false">${audioUrl}</guid>
      <link>${audioUrl}</link>
    </item>`;
    })
    .join('');

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
  <channel>
    <title>Le Veilleur — Podcast</title>
    <link>${channelLink}</link>
    <description>La revue tech quotidienne du Veilleur, en version audio.</description>
    <language>fr</language>
    <itunes:explicit>false</itunes:explicit>${items}
  </channel>
</rss>`;

  return new Response(xml, {
    headers: { 'Content-Type': 'application/rss+xml; charset=utf-8' },
  });
}
