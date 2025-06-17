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

    let playlistUrl = playlistId ? `${window.location.origin}/music/playlist/${playlistId}/` : window.location.href;
    navigator.clipboard.writeText(playlistUrl).then(() => {

        const statusSpan = button.querySelector('.copy-status');
        statusSpan.innerHTML = '<i class="fa-solid fa-check"></i>';

        setTimeout(() => {
            statusSpan.innerHTML = '';
        }, 2000);
    }).catch(err => {
        console.error("Can't copy link right now: ", err);
    });
}


document.addEventListener('DOMContentLoaded', function() {
    const phoneInput = document.querySelector("#phoneInput");
    let iti = null;

    if (phoneInput) {
        iti = window.intlTelInput(phoneInput, {
            initialCountry: "auto",
            geoIpLookup: callback => {
                fetch('https://ipapi.co/json')
                    .then(res => res.json())
                    .then(data => callback(data.country_code))
                    .catch(() => callback("IT"));
            },
            utilsScript: "https://cdn.jsdelivr.net/npm/intl-tel-input@17/build/js/utils.js"
        });

        const form = document.querySelector("form");
        if (form) {
            form.addEventListener("submit", function(e) {
                if (phoneInput && iti) {
                    phoneInput.value = iti.getNumber();
                }
            });
        }
    }
});