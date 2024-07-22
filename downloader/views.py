from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from .forms import VideoDownloaderFrom
import yt_dlp
import os

def home(request):
    if request.method == 'POST':
        form = VideoDownloaderFrom(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            try:
                response = download_with_yt_dlp(url)
                return JsonResponse({'success': True})
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)}, status=400)
        return JsonResponse({'success': False, 'error': 'Invalid form data'}, status=400)
    else:
        form = VideoDownloaderFrom()
    return render(request, 'index.html', {'form': form})

def download_with_yt_dlp(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloads/%(title)s.%(ext)s'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        video_title = info_dict.get('title', None)
        video_extension = info_dict.get('ext', None)
        filename = f'downloads/{video_title}.{video_extension}'
        
        response = HttpResponse(content_type='video/mp4')
        response['Content-Disposition'] = f'attachment; filename="{video_title}.{video_extension}"'
        with open(filename, 'rb') as f:
            response.write(f.read())
        
        # Remove the file after download to keep the server clean
        os.remove(filename)
        return response
