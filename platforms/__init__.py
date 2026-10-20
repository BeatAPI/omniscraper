import re
from . import youtube, bilibili, x, wechat, douyin, xiaohongshu, tiktok, instagram, facebook, threads, linkedin, reddit, pinterest, telegram, medium, substack, bluesky, generic
ALL = [youtube, bilibili, x, wechat, douyin, xiaohongshu, tiktok, instagram, facebook, threads, linkedin, reddit, pinterest, telegram, medium, substack, bluesky]


def detect(url):
    for m in ALL:
        if re.search(m.MATCH, url, re.I):
            return m
    return generic
