"""Offline checks: python scripts/test_helpers.py. No downloads or real API requests."""
from contextlib import redirect_stdout
import io
import json
import os
from pathlib import Path
import tempfile
from types import SimpleNamespace
from unittest.mock import Mock, patch
import urllib.error

import analyze_video as av
import download_tiktok as dl


def rejected(fn):
    try:
        fn()
    except ValueError:
        return
    raise AssertionError('Invalid input was accepted')


def main():
    url = 'https://www.tiktok.com/@demo/video/123456789'
    assert dl.extract_urls(['分享 '+url+'。',url,'https://vt.tiktok.com/Zabc123/']) == [url,'https://vt.tiktok.com/Zabc123/']
    for bad in ['https://tiktok.com.evil.test/@x/video/1','https://tiktok.com@evil.test/@x/video/1',
                'https://www.tiktok.com/@x','https://www.tiktok.com:8443/@x/video/1','https://www.tiktok.com:bad/@x/video/1']:
        rejected(lambda: dl.extract_urls([bad]))
    rejected(lambda: dl.extract_urls([f'https://vt.tiktok.com/ID{i}/' for i in range(6)]))
    with patch('download_tiktok.shutil.which',return_value='yt-dlp'),patch.dict(os.environ,{'HTTPS_PROXY':'https://proxy.invalid'}):
        cmd=dl.command(url,Path('C:/output'))
        assert cmd[-2:]==['--',url] and '--cookies-from-browser' not in cmd
        assert '--no-check-certificates' not in cmd and '--proxy' not in cmd
        assert os.environ['HTTPS_PROXY']=='https://proxy.invalid'
        assert '--cookies-from-browser' in dl.command(url,Path('C:/output'),'edge')
    assert av.processing(1,3,2)=={'type':'static','start_offset':1,'end_offset':3,'fps':2}
    for values in [(-1,None,2),(2,1,2),(0,None,0),(float('nan'),None,2)]:
        rejected(lambda: av.processing(*values))
    assert av.extract_text({'status':'completed','outputs':[{'type':'text','text':'old'}]})=='old'
    assert av.extract_text({'steps':[{'content':[{'type':'thought','text':'hidden'},{'type':'text','text':'new'}]}]})=='new'
    rejected(lambda: av.extract_text({'status':'in_progress','output_text':'not done'}))
    rejected(lambda: av.extract_text({'outputs':[]}))
    fake=SimpleNamespace(state=SimpleNamespace(name='FAILED'),name='files/test')
    client=SimpleNamespace(files=Mock())
    rejected(lambda: av.wait_active(client,fake,10))
    client.files.get.assert_not_called()
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp);video=root/'clip.mp4';video.write_bytes(b'fake-video-for-offline-test')
        output=root/'report.md'
        args=['analyze_video.py','--video',str(video),'--output',str(output),'--question','分辨口播与配乐','--start','1','--end','3']
        with patch('sys.argv',args+['--dry-run']),patch.dict(os.environ,{},clear=True),patch('urllib.request.urlopen') as network,redirect_stdout(io.StringIO()):
            av.main();network.assert_not_called();assert not output.exists()
        response=Mock();response.__enter__=Mock(return_value=io.BytesIO(b'{"status":"completed","outputs":[{"type":"text","text":"evidence"}]}'));response.__exit__=Mock(return_value=False)
        with patch('sys.argv',args),patch.dict(os.environ,{'GEMINI_API_KEY':'offline-test-key'}),patch('urllib.request.urlopen',return_value=response) as network,redirect_stdout(io.StringIO()):
            av.main()
            assert network.call_count==1 and output.read_text(encoding='utf-8')=='evidence'
            body=json.loads(network.call_args.args[0].data)
            assert body['store'] is False and body['input'][0]['processing']==av.processing(1,3,2)
            assert '分辨口播与配乐' in body['input'][1]['text']
        with patch('sys.argv',args),patch('urllib.request.urlopen') as network:
            rejected(av.main);network.assert_not_called();assert output.read_text(encoding='utf-8')=='evidence'
        output.unlink()
        error=urllib.error.HTTPError(av.ENDPOINT,429,'quota',{},None)
        with patch('sys.argv',args),patch.dict(os.environ,{'GEMINI_API_KEY':'offline-test-key'}),patch('urllib.request.urlopen',side_effect=error) as network:
            try:av.main()
            except RuntimeError as exc:assert '429' in str(exc) and 'offline-test-key' not in str(exc)
            else:raise AssertionError('Quota error was not surfaced')
            assert network.call_count==1 and not output.exists()
        # Exercise Files API routing/cleanup with a sparse test file and fake SDK, without network.
        with video.open('wb') as f:f.truncate(13*1024*1024)
        uploaded=SimpleNamespace(state=SimpleNamespace(name='ACTIVE'),name='files/offline',uri='https://example.invalid/video')
        files=Mock();files.upload.return_value=uploaded
        sdk_client=SimpleNamespace(files=files,close=Mock())
        fake_types=SimpleNamespace(HttpOptions=lambda **kw:kw,HttpRetryOptions=lambda **kw:kw)
        fake_genai=SimpleNamespace(Client=Mock(return_value=sdk_client),types=fake_types)
        response=Mock();response.__enter__=Mock(return_value=io.BytesIO(b'{"output_text":"large-file evidence"}'));response.__exit__=Mock(return_value=False)
        with patch.dict('sys.modules',{'google':SimpleNamespace(genai=fake_genai),'google.genai':fake_genai}),patch('sys.argv',args),patch.dict(os.environ,{'GOOGLE_API_KEY':'offline-test-key'},clear=True),patch('urllib.request.urlopen',return_value=response) as network,redirect_stdout(io.StringIO()):
            av.main()
            body=json.loads(network.call_args.args[0].data)
            assert body['input'][0]['uri']==uploaded.uri and 'data' not in body['input'][0]
            assert body['input'][0]['processing']==av.processing(1,3,2)
            files.delete.assert_called_once_with(name=uploaded.name)
            sdk_client.close.assert_called_once()
            assert fake_genai.Client.call_args.kwargs['http_options']['retry_options']['attempts']==1
    print('PASS: URL boundaries, cookies/proxy defaults, time bounds, dry-run, response parsing, output preservation, quota no-retry.')


if __name__=='__main__':
    main()
