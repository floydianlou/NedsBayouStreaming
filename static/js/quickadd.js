// script to create popup button for quick adding songs
document.querySelectorAll('.quickAddBtn').forEach(btn => {
  btn.addEventListener('click', function () {
    const songId = this.dataset.songId;

    fetch(`/music/get_user_playlists/?song_id=${songId}`)
      .then(response => response.json())
      .then(data => {
        const list = document.getElementById("playlistList");
        list.innerHTML = "";

        if (data.playlists && data.playlists.length > 0) {
          data.playlists.forEach(p => {
            const li = document.createElement("li");
            const button = document.createElement("button");
            button.textContent = `➕ ${p.name}`;
            button.classList.add("playlist-btn");

            button.addEventListener("click", () => {
              fetch('/music/add_song_to_playlist/', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                  'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                  song_id: songId,
                  playlist_id: p.id
                })
              })
                .then(response => response.json())
                .then(data => {
                  if (data.success) {
                    button.disabled = true;
                    button.textContent = "✅ Added!";
                    button.classList.add("added");
                  } else {
                    button.textContent = "⚠️ Error";
                  }
                });
            });

            li.appendChild(button);
            list.appendChild(li);
          });
        } else {
          list.innerHTML = `
            <p>You either have this song in all your playlists or don't have one!
              <a href="/music/create-playlist/" class="create-link">Make it here.</a>
            </p>`;
        }

        document.getElementById("quickAddModal").classList.remove("hidden");
      });
  });
});

document.getElementById("quickAddModal").addEventListener("click", function (e) {
  if (!e.target.closest(".modal-content")) {
    this.classList.add("hidden");
  }
});