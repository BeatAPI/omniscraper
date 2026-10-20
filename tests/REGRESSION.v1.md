# Regression 2026-10-14 (datacenter IP, no login, no BeatAPI; --with-media --with-comments)

| Platform | Result | Free method that worked | Content / media | Comments | Still needs BeatAPI |
|---|---|---|---|---|---|
| YouTube | PASS | yt-dlp | metadata, cover, ≤480p video, mp3 | 20 | subtitle download sometimes 429 on datacenter IP |
| B站 | PASS | api wbi/view (no w_rid) + guest buvid3 → playurl DASH | stats, cover, mp4, mp3 | 3 (guest) | – |
| X (tweet) | PASS | syndication tweet-result | text, likes, image, mp4 | – | comments |
| X (profile) | PASS | syndication timeline-profile | 100 tweets | – | – |
| 公众号 | PASS | article HTML #js_content | title, body, images | – | read counts, comments |
| 抖音 | PASS | iesdouyin share page (guest ttwid + Android UA), playwm→play | stats, cover, 720p no-watermark mp4, mp3 | – | comments |
| 小红书 | **FAIL** | xhshow guest session works, but homefeed now returns **461** (risk control; it worked earlier today from this IP) | – | – | note detail, list, comments, search |
| TikTok | PASS | yt-dlp (play stream, no watermark) | stats, cover, mp4, mp3 | 0 | comments |
| Instagram | PASS | yt-dlp post extractor | caption, likes/comments count, 3 images (~853px) | 12 | 1080 originals, profiles |
| Facebook | PASS | yt-dlp + Googlebot page counters | title, views, reactions, mp4, frame | – | comments, posts |
| Threads | PASS | Googlebot UA SSR | text, likes, image | – | comments |
| LinkedIn | PASS | guest JSON-LD (VideoObject/SocialMediaPosting) | text, likes, comment count, image | 10 (JSON-LD) | – |
| Reddit | PASS | .json 403 → .rss intermittently empty → arctic-shift | score 3544, 115 comments, image | 100 (arctic) | – |
| Pinterest | PASS | gallery-dl -j | description, saves, image | – | comments |
| Telegram | PASS | t.me/s preview | text, views, images | – | – |
| Medium | PASS | author RSS | full text, images | – | – |
| Substack | PASS | /api/v1/posts/<slug> | body, likes, image | 16 | – |
| Bluesky | PASS | public AppView | text, stats, images | 50 | – |

## Fresh-install smoke test 2026-10-14 17:5x (new venv in /tmp, `pip install -r requirements.txt`)
Bluesky ✅, 抖音 ✅ (no-watermark video; comments print the BeatAPI hint), B站 ✅ (wbi/view, DASH, guest comments), Telegram ✅. `beatapi.py check`: all mapped references exist.
