from django.shortcuts import render
from model.generator import generate_recommendations

def recommend_playlist(request):
    if request.method == 'POST':
        # POST isteği ile gelen formu al
        playlist_url = request.POST.get('playlist_url', '')

        # Algoritmanızı kullanarak öneri playlistini oluşturun (bu kısmı kendi algoritmanıza göre özelleştirin)
        recommend_playlist = generate_recommendations(playlist_url)

        # Öneri playlistini HTML şablonuna gönderin
        return render(request, 'recommend_playlist.html', {'recommend_playlist': recommend_playlist, 'playlist_url': playlist_url})

    return render(request, 'recommend_playlist_form.html')  # Eğer POST isteği değilse, basit bir form sayfası göster
