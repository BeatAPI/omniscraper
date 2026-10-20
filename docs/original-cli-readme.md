# omni-scraper

Free-first content scraper for 17 platforms. BeatAPI is an optional last-resort fallback.

## Install
```bash
sudo apt-get install -y ffmpeg          # needed for audio extraction, frames, and B站 DASH merge
cd /workspace/omni-scraper
python3 -m venv .venv                    # keep the venv here (gitignored), never inside the skill folder
.venv/bin/pip install -r requirements.txt   # faster-whisper is only needed for --transcribe
```

## Use
```bash
.venv/bin/python scrape.py <url> [--out dir] [--with-media] [--with-comments] \
    [--transcribe] [--whisper-model small] [--max-mb 60] [--max-images 20] [--search KEYWORD] [--fallback-beatapi]
```
- Output (default `--out output/<platform>_<timestamp>`): `content.md`, `meta.json`, and with `--with-media` also `image_XX.jpg|webp`, `video.mp4|webm`, `audio.mp3`, `frame.jpg` (when there is no image), `subtitle.<lang>.vtt` (YouTube), and `transcript.txt` (with `--transcribe`, which needs `--with-media` and faster-whisper).
- Every method attempt is logged as `[OK ]` or `[FAIL]`. When all free methods for a capability fail, the script prints
  `>> '<cap>' failed with all free methods -> paid fallback: BeatAPI capability data:...`, plus setup links when no key is set (see "Paid fallback" below).
- BeatAPI is called only when `--fallback-beatapi` is passed AND `BEATAPI_API_KEY` is set. The key is never printed.
  Override the capability reference with `BEATAPI_REF_<PLATFORM>_<CAP>`, and the API base with `BEATAPI_BASE`.
- `--max-mb` caps each download. Direct downloads (抖音, B站 DASH, X mp4) are cut at that size, so long videos come out as playable partial samples. Raise the cap to get the full file.
- Exit code: 0 = main content scraped (comments or media may still have failed), 2 = main content failed.
- Platform modules: youtube, bilibili, x, wechat (公众号), douyin, xiaohongshu, tiktok, instagram, facebook, threads, linkedin, reddit, pinterest, telegram, medium, substack, bluesky, plus a generic fallback (yt-dlp, then OpenGraph tags).

## Paid fallback: BeatAPI setup

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

## Disclaimer
- Collect **public content only**. Do not use it to get around logins, paywalls, private accounts or access controls, and do not collect personal data you have no lawful basis to process.
- You are responsible for following each platform's Terms of Service and robots rules, and the copyright and data-protection laws that apply to you (for example GDPR or China's PIPL). Several techniques here (crawler user agents, guest tokens, locally generated request signatures, watermark-free media URLs) may be against some platforms' terms. Use them at your own risk, at low request rates, and for legitimate purposes such as research, archiving your own content, or analysis.
- Downloaded media stays the property of its creators. Do not republish it without permission.
- Third-party dependencies keep their own licenses: yt-dlp (Unlicense), gallery-dl (GPL-2.0, called as a separate CLI process), xhshow (MIT), faster-whisper (MIT), requests (Apache-2.0), numpy (BSD). Check them before you redistribute anything. arctic-shift and BeatAPI are third-party services with their own terms.
- Provided as-is, with no warranty. Platform changes can break any method at any time.

## Regression
`tests/run_regression.sh --with-media --max-mb 8 --max-images 3` runs one real URL per platform (`tests/regression_urls.txt`). Logs and results go to `output/regression/`. Latest results: `tests/REGRESSION.md`.

## Layout
- `scrape.py`: entry point, URL detection, media, fallback
- `core.py`: HTTP, yt-dlp, ffmpeg/whisper, writers
- `beatapi.py`: optional fallback
- `platforms/*.py`: one module per platform, each defining `MATCH` and `scrape(res, opts)` with an ordered list of free methods

## License

MIT, see [LICENSE](LICENSE). Copyright (c) 2026 BeatAPI. The license covers this code only; scraped content stays subject to each platform's terms and its authors' rights.
