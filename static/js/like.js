// js function to dynamically like a song and add it to user's liked songs

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.like-button').forEach(button => {
    button.addEventListener('click', () => {
      const songId = button.dataset.songId;
      const icon = button.querySelector('i');

      fetch(`/like/${songId}/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCookie('csrftoken'),
          'X-Requested-With': 'XMLHttpRequest'
        }
      })
      .then(response => response.json())
      .then(data => {
        if (data.liked !== undefined) {
          if (data.liked) {
            icon.classList.remove('far');
            icon.classList.add('fas');
            icon.style.color = 'black';
          } else {
            icon.classList.remove('fas');
            icon.classList.add('far');
            icon.style.color = '#aaa';
          }
        }
      });
    });
  });
});