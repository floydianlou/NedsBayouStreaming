document.addEventListener('DOMContentLoaded', () => {
  const tabs = document.querySelectorAll('#typeTabs .tab');
  const items = document.querySelectorAll('.search-results-container .result-item');
  const genreBox = document.getElementById('genreFilterBox');
  const genreNotice = document.getElementById('genreFilterNotice');
  const genreForm = document.getElementById('genreFilterForm');
  const playlistLengthBox = document.getElementById('playlistLengthFilterBox');
  const playlistLengthForm = document.getElementById('genreFilterForm');
  const userLikesBox = document.getElementById('userLikesFilterBox');

  function getActiveGenres() {
    if (!genreBox) return [];
    return Array.from(genreBox.querySelectorAll('input[type="checkbox"]:checked')).map(cb => cb.value);
  }

  function updateResults(filter) {
    const activeGenres = getActiveGenres();
    const genreFilterActive = activeGenres.length > 0;

    items.forEach(item => {
      const type = item.dataset.type;

      if (filter === 'all') {
        if (genreFilterActive) {
          item.style.display = (type === 'song' || type === 'artist') ? '' : 'none';
        } else {
          item.style.display = '';
        }
      } else {
        item.style.display = (type === filter) ? '' : 'none';
      }
    });

    // Mostra/nasconde il blocco delle spunte (solo song/artist/all)
    if (genreBox) {
      genreBox.style.display = (filter === 'song' || filter === 'artist' || filter === 'all') ? 'block' : 'none';
    }

    // Mostra/nasconde playlistLengthFilterBox (SOLO playlist!)
    if (playlistLengthBox) {
      playlistLengthBox.style.display = (filter === 'playlist') ? 'block' : 'none';
    }

    // Mostra messaggio solo su Users o Playlists
    if (genreNotice) {
      const isUserOrPlaylist = (filter === 'user' || filter === 'playlist');
      genreNotice.style.display = isUserOrPlaylist ? 'block' : 'none';
    }

    const userLikesBox = document.getElementById('userLikesFilterBox');
    if (userLikesBox) {
      userLikesBox.style.display = (filter === 'user') ? 'block' : 'none';
    }
  }

  // Click sui TAB
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');

      const filter = tab.dataset.filter;

      // Aggiorno il campo hidden "type" per il form, così il submit mantiene la tab giusta!
      const typeInput = document.getElementById('typeInput');
      if (typeInput) {
        typeInput.value = filter;
      }

      updateResults(filter);
    });
  });

  // aggiorna i risultati anche quando clicchi sulle spunte (per generi)
  if (genreBox && genreForm) {
    const checkboxes = genreBox.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
      checkbox.addEventListener('change', () => {
        genreForm.submit();  // ricarica la pagina
      });
    });
  }

  // aggiorna i risultati anche quando clicchi sulle spunte (per playlist length)
  if (playlistLengthBox && playlistLengthForm) {
    const checkboxes = playlistLengthBox.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
      checkbox.addEventListener('change', () => {
        playlistLengthForm.submit();  // ricarica la pagina
      });
    });
  }

  // aggiorna i risultati anche quando clicchi sulle spunte (per user likes)
  if (userLikesBox && genreForm) {
    const checkboxes = userLikesBox.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
      checkbox.addEventListener('change', () => {
        genreForm.submit();  // ricarica la pagina
      });
    });
  }

  // All'avvio, aggiorna la pagina in base alla tab attiva
  const currentTab = document.querySelector('#typeTabs .tab.active');
  if (currentTab) {
    updateResults(currentTab.dataset.filter);
  }
});