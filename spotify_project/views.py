from django.shortcuts import render

from model.uri_to_playlist import get_full_songs

def recommend_playlist(request):
    if request.method == 'POST':
        # POST isteği ile gelen formu al
        playlist_url = request.POST.get('playlist_url', '')

        # Algoritmanızı kullanarak öneri playlistini oluşturun (bu kısmı kendi algoritmanıza göre özelleştirin)
        recommend_playlist = get_full_songs(playlist_url)

        # Öneri playlistini HTML şablonuna gönderin
        return render(request, 'recommend_playlist.html', {'recommend_playlist': recommend_playlist, 'playlist_url': playlist_url})

    return render(request, 'recommend_playlist_form.html')  # Eğer POST isteği değilse, basit bir form sayfası göster