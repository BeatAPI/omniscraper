# Regression 2026-10-14 run 2 (well-known creators; datacenter IP, no login, no BeatAPI; --with-media --with-comments --max-mb 8 --max-images 3)

| Key | URL | Author scraped | Result |
|---|---|---|---|
| youtube | https://www.youtube.com/watch?v=0e3GPea1Tyg | MrBeast | PASS |
| bilibili | https://www.bilibili.com/video/BV132pr6aEXS | 英雄联盟赛事 | PASS |
| x | https://x.com/elonmusk/status/1585341984679469056 | Elon Musk (@elonmusk) | PASS |
| x_profile | https://x.com/elonmusk | @elonmusk | PASS |
| wechat | https://mp.weixin.qq.com/s/kJRaBFPVB-KO6ennSP9MLA | 新闻联播 | PASS |
| douyin | https://www.douyin.com/video/7372484719365098803 | 萧萧不吃辣 | PASS |
| xiaohongshu | https://www.xiaohongshu.com/explore | – | **FAIL** (461 risk control on this IP; needs residential IP or BeatAPI) |
| tiktok | https://www.tiktok.com/@zachking/video/6768504823336815877 | zachking | PASS |
| instagram | https://www.instagram.com/p/DW1nTDiDvnF/ | NASA | PASS |
| facebook | https://www.facebook.com/watch/?v=10153231379946729 | Facebook | PASS |
| threads | https://www.threads.com/@zuck/post/DZpPDXbCeTt | zuck | PASS |
| linkedin | https://www.linkedin.com/posts/microsoft_getting-help-at-work-shouldnt-feel-like-activity-7513274728854429696-68qR | Microsoft | PASS |
| reddit | https://www.reddit.com/r/IAmA/comments/z1c9z/i_am_barack_obama_president_of_the_united_states/ | u/PresidentObama | PASS |
| pinterest | https://www.pinterest.com/pin/99360735500167749/ | kentbrew | PASS |
| telegram | https://t.me/telegram/300 | @telegram | PASS |
| medium | https://medium.com/@netflixtechblog | Netflix Technology Blog | PASS |
| substack | https://www.noahpinion.blog/p/a-nobel-for-new-keynesian-macro-at | Noah Smith | PASS |
| bluesky | https://bsky.app/profile/bsky.app/post/3l6oveex3ii2l | Bluesky (@bsky.app) | PASS |

17/18 entries pass (16/17 platforms). 抖音 still uses the v1 video: no free way found to locate an official-account video ID from this machine. Old URL list: tests/regression_urls.v1.txt; previous report: tests/REGRESSION.v1.md (also below).

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
