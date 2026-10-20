---
name: Multi-platform content scraping
description: Use when the user shares a link (or asks to collect content) from YouTube, B站/Bilibili, 抖音/Douyin, 小红书/Xiaohongshu, 公众号/WeChat articles, X/Twitter, TikTok, Instagram, Facebook, Threads, LinkedIn, Reddit, Pinterest, Telegram channels, Medium, Substack or Bluesky, and needs the text, media (images/video/audio/subtitles), comments or metadata. Free methods come first; BeatAPI is only an optional paid fallback.
---
# Multi-platform content scraping

## 0. Ground rules
- Public content only. Never use the user's personal accounts or cookies. Never touch login-only or private data (DMs, private groups or accounts, follower lists, anything behind a login wall). Never post, like, follow or perform any other write action.
- "Guest" identifiers are fine: anonymous device or session tokens that a site gives every logged-out visitor (B站 buvid3, 抖音 ttwid, a 小红书 guest session).
- Free methods go first, in the order listed below. BeatAPI is called only when the user has set `BEATAPI_API_KEY` and you pass `--fallback-beatapi`. Never print or echo the key.
- If a free method fails and the user has no `BEATAPI_API_KEY` yet, tell them exactly which capability needs the paid fallback (the name the script prints, for example `data:douyin.app.v3.fetch_video_comments`) and send them the sign-up and key steps from section 4b. In Grok Bot, offer a secret-input card for `BEATAPI_API_KEY`. Never ask for the key in plain chat, and never run paid calls without their go-ahead.
- Download only short samples of large media unless the user asks for the full file (`--max-mb`).

## 1. Install and run
Code lives in `/workspace/omni-scraper`. If that directory does not exist, rebuild it from section 5.
```bash
sudo apt-get install -y ffmpeg
cd /workspace/omni-scraper && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
# requirements: requests yt-dlp gallery-dl xhshow numpy faster-whisper(optional)
.venv/bin/python scrape.py "<url>" --out out/<name> [--with-media] [--with-comments] [--transcribe] [--max-mb 60] [--search KEYWORD] [--fallback-beatapi]
```
- The platform is detected from the URL. Each run writes `content.md` and `meta.json` plus any media files.
- The log shows `[OK ]` or `[FAIL]` for every method tried. If all free methods fail, it prints `>> '<cap>' failed with all free methods -> paid fallback: BeatAPI capability data:...` plus setup links. Report that capability name to the user.
- Regression check: `tests/run_regression.sh --with-media --max-mb 8 --max-images 3` runs one real URL per platform.

## 2. Capability matrix (tested from a datacenter IP, logged out)
✅ = free and tested, 🟡 = free but needs a residential IP, a guest cookie or self-hosting, 🅱️ = BeatAPI fallback (🅱️* = only the generic page reader `data:web.read`: page text, no structured fields), – = not applicable. Last regression: see `tests/REGRESSION.md`.

| Platform | Text | Author | Stats | Images | Video (no watermark) | Audio | Subtitles | Comments | Profile/list | Search |
|---|---|---|---|---|---|---|---|---|---|---|
| YouTube | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ (429 risk; 🅱️ captions) | ✅ | 🟡 (🅱️) | 🟡 (🅱️) |
| B站 | ✅ | ✅ | ✅ | ✅ | ✅ DASH | ✅ | ✅ whisper | ✅ guest | 🟡 wbi | 🟡 wbi |
| X | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | – | 🅱️ | ✅ timeline | 🅱️ |
| 公众号 | ✅ | ✅ | 🅱️ | ✅ | 🟡 | – | ✅ | 🅱️ | 🟡 | 🟡 |
| 抖音 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ whisper | 🅱️ | 🅱️ | 🅱️ |
| 小红书 | 🅱️ | 🅱️ | 🅱️ | 🟡 original via ci.xiaohongshu.com | 🟡 | 🟡 | 🟡 | 🅱️ | 🟡 guest feed (461 on flagged IPs) | 🅱️ |
| TikTok | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ whisper | 🅱️ | 🟡 | 🅱️ |
| Instagram | ✅ | ✅ | ✅ | 🟡 ~853px | 🟡 reels | 🟡 | – | ✅ few (🅱️ for all) | 🅱️ | 🅱️ |
| Facebook | ✅ | ✅ | ✅ | ✅ frame | ✅ | ✅ | – | 🅱️* | 🅱️* | 🅱️* |
| Threads | ✅ | ✅ | ✅ | ✅ | 🟡 | – | – | 🟡 (🅱️) | ✅ (🅱️) | 🅱️ |
| LinkedIn | ✅ | ✅ | ✅ | ✅ | 🟡 | – | – | ✅ JSON-LD (🅱️ full) | 🟡 company (🅱️ person/company/jobs) | 🅱️ jobs |
| Reddit | ✅ | ✅ | ✅ | ✅ | 🟡 | – | – | ✅ | ✅ RSS | 🟡 |
| Pinterest | ✅ | ✅ | ✅ | ✅ | 🟡 | – | – | 🅱️* | 🟡 | 🅱️* |
| Telegram | ✅ | ✅ | ✅ views | ✅ | 🟡 | – | – | – | ✅ | 🅱️ |
| Medium | ✅ | ✅ | 🅱️* claps | ✅ | – | – | – | 🅱️* | ✅ RSS | 🟡 |
| Substack | ✅ | ✅ | ✅ | ✅ | – | 🟡 podcast | – | ✅ | ✅ | 🟡 |
| Bluesky | ✅ | ✅ | ✅ | ✅ | 🟡 | – | – | ✅ | ✅ | 🟡 |

## 3. Free method chains and key tricks (in order)
- **YouTube**: yt-dlp `-j` gives metadata; add `getcomments` for comments. Auto subtitles: download the vtt from `automatic_captions` (can return 429 on datacenter IPs). Video uses format `b[filesize<N]/…/bv*[height<=480]+ba`; audio uses `yt-dlp -x`.
- **B站**: get guest `buvid3`/`buvid4` from `api.bilibili.com/x/frontend/finger/spi`, and send UA + `Referer: https://www.bilibili.com` on every request.
  - Metadata: `x/web-interface/wbi/view?bvid=` (works without w_rid). If that fails, try `view`, then the page's `__INITIAL_STATE__`, then yt-dlp (yt-dlp gets 412 on datacenter IPs).
  - Comments: `x/v2/reply?type=1&oid=<aid>&sort=1`.
  - Media: `x/player/playurl?avid&cid&fnval=16` returns DASH; download the audio and video tracks with the Referer, then merge with ffmpeg.
  - B站 has no public CC subtitles for logged-out visitors; use faster-whisper.
- **X**: for a single tweet, `cdn.syndication.twimg.com/tweet-result?id=<id>&token=4` (text, likes, media, mp4 variants). For a profile, `syndication.twitter.com/srv/timeline-profile/screen-name/<user>` and parse `__NEXT_DATA__` (about 100 tweets). twscrape and twikit need accounts, so do not use them with the user's accounts.
- **公众号**: GET the article HTML and parse `#js_content`. Title comes from `og:title`, the author from `var nickname`, the time from `var ct`, and images from `data-src` on mmbiz.qpic.cn. Read and like counts are not public.
- **抖音**:
  1. Register a guest `ttwid` by POSTing to `ttwid.bytedance.com/ttwid/union/register/`.
  2. Request `https://www.iesdouyin.com/share/video/<id>/` with an **Android mobile UA** and parse `_ROUTER_DATA` to get the item (desc, statistics, cover, `images[]` for 图集 posts, `video.play_addr`).
  3. **Replace `playwm` with `play`** in the play URL to get the 720p no-watermark mp4. Extract audio with ffmpeg.
  - Fallback: request `www.douyin.com/video/<id>` with a **Googlebot UA**. The SEO page has a meta description with title, author, date and likes, plus `commentCount` and the cover.
  - Comments, search and profiles need the a_bogus signature and get blocked by Argus, so use the paid fallback.
- **小红书**:
  1. Use the open-source signer `xhshow` (github.com/Cloxl/xhshow) to generate `a1`/`webId` locally, then POST `edith.xiaohongshu.com/api/sns/web/v1/login/activate` with the signed x-s headers to get a guest `web_session`.
  2. The signed `homefeed` returns note_id + **xsec_token** + title/author/likes/cover.
  3. Note detail: signed `/api/sns/web/v1/feed` with `source_note_id` + `xsec_token`, or the note page `/explore/<id>?xsec_token=…` and its `__INITIAL_STATE__`.
  - A note URL without its xsec_token fails with error 300031, so always keep the full share link. `xhslink.com` short links redirect to a URL that includes the token.
  - **Original images**: take the trace id from any xhscdn URL and request `https://ci.xiaohongshu.com/<trace>?imageView2/format/jpg`.
  - From datacenter IPs, `/feed` and later even `homefeed` return **461** (risk control), comments return 406 and search returns -104 (login required). Use a residential IP, or fall back to BeatAPI.
- **TikTok**: yt-dlp (its default play stream has no watermark), with oEmbed `tiktok.com/oembed?url=` as a fallback. Comments come back empty for guests, so use BeatAPI.
- **Instagram**: yt-dlp `--ignore-no-formats-error` on `/p/<code>/` gives caption, like/comment counts, carousel thumbnails (~853px) and a few comments. Profiles (`web_profile_info` returns 401), 1080px originals and full comments need login. Mirror sites (imginn, pixwox) are mostly dead.
- **Facebook**: yt-dlp for public videos (title, uploader, views). A Googlebot UA page fetch exposes "1.3K reactions / 2.8M views". If there is no thumbnail, grab a frame with ffmpeg. Posts and profiles need login.
- **Threads**: fetch the post or profile page with a **Googlebot** or `facebookexternalhit` UA. You get og:title and og:description plus SSR JSON (`code`, `like_count`, `taken_at`).
- **LinkedIn**: logged-out company and post pages contain JSON-LD (`SocialMediaPosting`/`VideoObject`) with text, likes, commentCount and a few comments. Personal profiles and search are behind the authwall, so the free path does not touch them; with the user's agreement, the paid fallback has dedicated LinkedIn capabilities (post, comments, person, company, jobs).
- **Reddit**: try the `.json` suffix first (blocked with 403 on datacenter IPs), then `.rss` (Atom; may be empty when rate-limited), then **arctic-shift** (`arctic-shift.photon-reddit.com/api/posts/ids?ids=`, `/api/comments/search?link_id=`) for score and comments. Arctic-shift values are archive snapshots. PRAW with the user's own free OAuth app is also fine if they provide one.
- **Pinterest**: `gallery-dl -j <pin>` (original image, saves, description), with oEmbed `pinterest.com/oembed.json?url=` as a fallback.
- **Telegram** (public channels only): `https://t.me/s/<channel>` (use `?before=<id+1>` to reach older posts). Parse `tgme_widget_message_text`, views, datetime and photo backgrounds.
- **Medium**: `medium.com/feed/@user` (or `<sub>.medium.com/feed`) has full text in `content:encoded`. Otherwise fall back to the article's og tags.
- **Substack**: `<pub>/api/v1/posts/<slug>` returns body, reactions and comment count. Comments come from `<pub>/api/v1/post/<id>/comments`, and a list from `/api/v1/posts?limit=`.
- **Bluesky**: the public AppView `public.api.bsky.app/xrpc/` needs no key. Use `app.bsky.feed.getPostThread` for a post plus replies, and `getAuthorFeed` for a profile.
- **Anything else**: yt-dlp generic extractor, then OpenGraph tags.
- **Transcripts**: run faster-whisper (tiny/small, CPU int8) on audio decoded by ffmpeg to 16 kHz PCM. Pass a numpy array instead of a file path, because some PyAV versions break `decode_audio`.

## 4. Datacenter IP limits
- Cloud and datacenter IPs get extra blocks: B站 yt-dlp/view (412), Reddit `.json` (403), 小红书 (302/461/300011), YouTube subtitles (429), Instagram profiles (401). A residential IP or proxy unlocks most of these without any account. Try that before paying.
- Use the paid fallback only when every free method in the chain failed, the user needs that capability, and the user has agreed to paid calls.

## 4b. Paid fallback: BeatAPI setup

**Default: everything runs on free methods**, with no account or key needed. BeatAPI is called only when you pass `--fallback-beatapi` **and** `BEATAPI_API_KEY` is set.

### When you need it
Only when every free method for a capability has failed and you really need that data. The scraper then prints:
`>> '<capability>' failed with all free methods -> paid fallback: BeatAPI capability data:...`

Mapped capabilities (`python beatapi.py check` verifies them live; 53 mappings, 44 unique references):

| Platform | Capability → BeatAPI reference (input taken from the URL) |
|---|---|
| 抖音 | content `data:douyin.app.v3.fetch_one_video` · comments `data:douyin.app.v3.fetch_video_comments` · profile `data:douyin.web.handler_user_profile` · list `data:douyin.web.fetch_user_post_videos` (sec_user_id from `/user/<id>`) · search `data:douyin.app.v3.open_douyin_app_to_keyword_search` |
| 小红书 | content `data:xiaohongshu.web_v3.fetch_note_detail` (note_id + xsec_token) · comments `data:xiaohongshu.app_v2.get_note_comments` · profile `data:xiaohongshu.web_v3.fetch_user_info` · list `data:xiaohongshu.app_v2.get_user_posted_notes` · search `data:xiaohongshu.app_v2.search_notes` |
| TikTok | comments `data:tiktok.app.v3.fetch_video_comments` · profile `data:tiktok.web.fetch_user_profile` (uniqueId) · list `data:tiktok.web.fetch_user_post` (needs secUid from profile, pass via `BEATAPI_INPUT`) · search `data:tiktok.app.v3.fetch_general_search_result` |
| Instagram | comments `data:instagram.v2.fetch_post_comments` · list `data:instagram.v2.fetch_user_posts` (username) · search `data:instagram.v2.general_search` |
| X | comments `data:twitter.web.fetch_post_comments` · list `data:twitter.web.fetch_user_post_tweet` · search `data:twitter.web.fetch_search_timeline` |
| YouTube | comments `data:youtube.web_v2.get_video_comments` · subtitles `data:youtube.web_v2.get_video_captions` (srt) · list `data:youtube.web_v2.get_channel_videos` (`/channel/UC…`) · search `data:youtube.web_v2.get_general_search` |
| B站 | comments `data:bilibili.web.fetch_video_comments` · list `data:bilibili.web.fetch_user_post_videos` (space uid) · search `data:bilibili.web.fetch_general_search` |
| 公众号 | content `data:wechat_mp.v2.fetch_article_detail_h5` · stats `data:wechat_mp.v2.fetch_article_stats` · comments `data:wechat_mp.v2.fetch_article_comments` (no keyword-search capability found; `data:wechat_mp.v2.fetch_account_articles` lists an account's articles by username) |
| Threads | content/comments `data:threads.web.fetch_post_detail_v2` · profile `data:threads.web.fetch_user_info` · list `data:threads.web.fetch_user_posts` (needs user_id from profile, pass via `BEATAPI_INPUT`) · search `data:threads.web.search_recent` |
| LinkedIn | post `data:linkedin.web_v2.get_post_detail` · comments `data:linkedin.web_v2.get_post_comments` (activity urn) · person `data:linkedin.web_v2.get_user_profile` / `get_user_posts` · company `data:linkedin.web_v2.get_company_profile` / `get_company_posts` · job `data:linkedin.web_v2.get_job_detail` · search (jobs) `data:linkedin.web_v2.search_jobs` |
| Reddit | search `data:reddit.app.fetch_dynamic_search` |
| Facebook, Pinterest, Medium, other sites | generic page reader `data:web.read` (input `urls: [url]`; returns page text, not structured fields) |

The URL type picks the capability automatically (for example LinkedIn `/in/` → person, `/company/` → company, `/jobs/` → job). Keyword search: `scrape.py "<platform home URL>" --search "<keyword>" --fallback-beatapi` (there is no free keyword search). For two-step inputs, add or override fields with `BEATAPI_INPUT='{"secUid":"..."}'`.

Facebook and Pinterest have no dedicated capability yet; they fall back to the generic page reader `data:web.read`. Bluesky, Telegram, Substack and Reddit (via arctic-shift) rarely need a paid fallback.

### Sign up and get a key
1. Sign up: https://beatapi.io/sign-up (existing users sign in at https://beatapi.io/sign-in).
2. Create a key at Dashboard → API Keys: https://beatapi.io/dashboard/apikeys. Copy it right away; it is shown only once.
3. Top up in the dashboard: https://beatapi.io/dashboard/billing. Prices are on the pricing page: https://beatapi.io/pricing.
4. Docs: https://docs.beatapi.io/quick-guide and https://docs.beatapi.io/capabilities.

### Provide the key
- **In Grok Bot**: ask the bot to open a **secret-input card** for `BEATAPI_API_KEY`. Never paste a key into normal chat.
- **Local shell**: `export BEATAPI_API_KEY=...`, or keep it out of shell history with `read -rsp "BeatAPI API key: " BEATAPI_API_KEY && echo && export BEATAPI_API_KEY`.
- Never commit the key, put it in a URL, or print it. The scripts never log it.

### Turn it on
```bash
.venv/bin/python beatapi.py check                     # verify mapped references exist (no key needed)
.venv/bin/python beatapi.py find "抖音 视频评论"        # look up references by platform + action
.venv/bin/python beatapi.py inspect data:douyin.app.v3.fetch_video_comments   # input schema
.venv/bin/python scrape.py "<one test link>" --with-comments --fallback-beatapi --out out/beat-test
#   -> out/beat-test/beatapi_<capability>.json; errors show code + request_id (401 key, 402 balance)
```
Override a mapping with `BEATAPI_REF_<PLATFORM>_<CAP>=data:...` (for example `BEATAPI_REF_DOUYIN_COMMENTS`).

### 中文简版
- 默认全部走免费方法，不用注册，也不用 key。只有同时加了 `--fallback-beatapi`、又设置了 `BEATAPI_API_KEY`，才会调用 BeatAPI。
- 什么时候需要：某一项的免费方法全部失败、而这项数据确实需要时。对应的能力名见上表。关键词搜索没有免费方法，用 `--search "关键词" --fallback-beatapi`。Facebook、Pinterest 暂无专门能力，用通用网页读取 `data:web.read` 兜底；LinkedIn 有专门能力，帖子、评论、个人、公司、职位都有。
- 注册：https://beatapi.io/sign-up ；创建 key：https://beatapi.io/dashboard/apikeys （只显示一次）；在控制台充值：https://beatapi.io/dashboard/billing ；价格见价格页：https://beatapi.io/pricing 。
- 填 key：在 Grok Bot 里让 bot 弹出 `BEATAPI_API_KEY` 的密钥输入卡片；本地命令行用 `export BEATAPI_API_KEY=...`。
- 开启：先用 `python beatapi.py check` / `find` / `inspect` 核对能力名，再加 `--fallback-beatapi`，拿一条链接自测。

## 5. Rebuilding /workspace/omni-scraper if it is missing
Create the following, then run the regression script:
- `requirements.txt`: requests, yt-dlp, gallery-dl, xhshow, numpy, faster-whisper.
- `core.py`:
  - UA constants (desktop Chrome, Android Chrome, Googlebot, facebookexternalhit)
  - a `Result` object: platform, url, title, author, published, text, stats, images, videos, comments, items, extra, methods log, media_files, needs_beatapi
  - `attempt(res, capability, [(name, fn), …])`: try each function in order, log OK/FAIL, and add the capability to `needs_beatapi` when all fail
  - helpers: yt-dlp info/download wrappers (quiet, size-capped format), `download(url, path, ua, referer, max_bytes)`, ffmpeg audio extraction, faster-whisper transcription
  - `write_outputs` to write content.md and meta.json
- `platforms/<name>.py`: one module per platform with a `MATCH` regex and `scrape(res, opts)` implementing the chain from section 3. `platforms/__init__.py` defines `detect(url)` by checking platforms in order and falling back to generic.
- `scrape.py`:
  - argparse with `url --out --with-media --with-comments --transcribe --max-mb --max-images --fallback-beatapi`
  - detect the platform and run its `scrape`
  - with `--with-media`, download images and video (B站 DASH merge, 抖音 Android UA, yt-dlp for tuples), extract audio, take a frame if there are no images, download subtitles, and transcribe if asked
  - for each capability in `needs_beatapi`, print the BeatAPI hint, or with the flag and the env key set, call `beatapi.run`
- `beatapi.py`: `POST /v1/capabilities/search` and `/inspect` (no key) for `find`, `inspect` and `check`; `POST /v1/capabilities/run` with `{reference, operation:"start", input:<schema-specific ids such as aweme_id, note_id+xsec_token, tweet_id, video_id, code_or_url>, view:"full"}` with `Authorization: Bearer $BEATAPI_API_KEY` to `$BEATAPI_BASE` (default `https://api.beatapi.io`). Map (platform, capability) to a reference name, overridable with `BEATAPI_REF_<PLATFORM>_<CAP>`. Never log the key.
- `tests/regression_urls.txt` (one `name url` per line) and `tests/run_regression.sh`, which loops over the file running scrape.py with `< /dev/null` so ffmpeg does not eat stdin.
