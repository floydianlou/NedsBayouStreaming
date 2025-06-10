function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function copyPlaylistLink(button, playlistId = null, event=null) {
  if (event) {
        event.stopPropagation();
    }

    let playlistUrl = playlistId ? `${window.location.origin}/playlist/${playlistId}/` : window.location.href;
    navigator.clipboard.writeText(playlistUrl).then(() => {

        const statusSpan = button.querySelector('.copy-status');
        statusSpan.innerHTML = '✔️';

        setTimeout(() => {
            statusSpan.innerHTML = '';
        }, 2000);
    }).catch(err => {
        console.error("Failed to copy link: ", err);
    });
}