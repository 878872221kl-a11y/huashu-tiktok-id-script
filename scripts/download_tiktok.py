"""Download individual TikTok references via existing yt-dlp; no default cookies."""
import argparse
import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
from urllib.parse import urlsplit


def extract_urls(texts):
    urls = []
    for text in texts:
        found = re.findall(r'https://[^\s<>\'"，。；！？）】]+', text)
        for url in found:
            url = url.rstrip('.,;!?)\u3001')
            try:
                p = urlsplit(url)
                allowed = p.hostname in {'tiktok.com', 'www.tiktok.com', 'm.tiktok.com', 'vm.tiktok.com', 'vt.tiktok.com'}
                individual = bool(re.fullmatch(r'/@[^/]+/video/\d+/?', p.path) or re.fullmatch(r'/t/[A-Za-z0-9]+/?', p.path))
                if p.hostname in {'vm.tiktok.com', 'vt.tiktok.com'}:
                    individual = bool(re.fullmatch(r'/[A-Za-z0-9]+/?', p.path))
                if allowed and individual and not p.username and not p.password and p.port in (None, 443) and url not in urls:
                    urls.append(url)
            except ValueError:
                continue
    if not 1 <= len(urls) <= 5:
        raise ValueError('Provide 1–5 individual TikTok video URLs, short links or share texts; local videos need no download.')
    return urls


def command(url, output_dir, browser=None):
    executable = shutil.which('yt-dlp')
    if executable:
        prefix = [executable]
    elif importlib.util.find_spec('yt_dlp'):
        prefix = [sys.executable, '-m', 'yt_dlp']
    else:
        raise RuntimeError('yt-dlp is unavailable. Use an existing yt-dlp environment or a local video.')
    args = prefix + ['--ignore-config', '--no-playlist', '--playlist-items', '1', '--no-progress',
                     '--no-overwrites', '--retries', '1', '--fragment-retries', '1', '--socket-timeout', '25',
                     '-f', 'b[ext=mp4]/b', '--no-simulate', '--print', 'after_move:filepath',
                     '-o', str(output_dir / 'tiktok-%(id)s.%(ext)s')]
    if browser:
        args += ['--cookies-from-browser', browser]
    return args + ['--', url]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--urls', nargs='+', required=True)
    p.add_argument('--output-dir', type=Path, default=Path('_temp/tiktok-downloads'))
    p.add_argument('--cookies-browser', choices=['chrome', 'edge', 'firefox'])
    p.add_argument('--dry-run', action='store_true')
    a = p.parse_args()
    urls = extract_urls(a.urls)
    out = a.output_dir.resolve()
    if a.dry_run:
        print(json.dumps({'urls': urls, 'output_dir': str(out), 'cookies_browser': a.cookies_browser, 'network': False}))
        return 0
    out.mkdir(parents=True, exist_ok=True)
    records = []
    for url in urls:
        try:
            r = subprocess.run(command(url, out, a.cookies_browser), capture_output=True,
                               text=True, encoding='utf-8', errors='replace', timeout=180)
            paths = [Path(line.strip()).resolve() for line in r.stdout.splitlines() if line.strip()]
            paths = [f for f in paths if f.is_file() and f.is_relative_to(out) and f.suffix.lower() in {'.mp4', '.webm', '.mkv', '.mov'}]
            if r.returncode or not paths:
                raise RuntimeError(f'yt-dlp failed (exit {r.returncode}); verify link/access or use a local video. No credentials were printed.')
            records.append({'url': url, 'success': True, 'path': str(paths[-1])})
        except (RuntimeError, OSError, subprocess.TimeoutExpired) as exc:
            records.append({'url': url, 'success': False, 'error': str(exc)[:400]})
    print(json.dumps({'results': records}, ensure_ascii=False, indent=2))
    return 0 if all(r['success'] for r in records) else 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValueError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
