// Gallery lightbox and filter behavior (vanilla JS)
document.addEventListener('DOMContentLoaded', function () {
  // Elements
  const categoryFilters = document.querySelectorAll('[data-filter-category]');
  const tagFilters = document.querySelectorAll('[data-filter-tag]');
  const galleryItems = document.querySelectorAll('.gallery-item');

  function filterItems() {
    const activeCategory = document.querySelector('[data-filter-category].active')?.dataset.filterCategory || 'all';
    const activeTag = document.querySelector('[data-filter-tag].active')?.dataset.filterTag || 'all';

    galleryItems.forEach(item => {
      const itemCategory = item.dataset.category;
      const itemTags = item.dataset.tags || '';

      let showItem = true;
      if (activeCategory !== 'all' && itemCategory !== activeCategory) showItem = false;
      if (activeTag !== 'all' && !itemTags.includes(activeTag)) showItem = false;

      if (showItem) {
        item.style.display = '';
        item.classList.add('fade-in-up');
      } else {
        item.style.display = 'none';
        item.classList.remove('fade-in-up');
      }
    });

    // Refresh lightbox after DOM changes
    refreshLightbox();
  }

  categoryFilters.forEach(filter => {
    filter.addEventListener('click', function () {
      categoryFilters.forEach(f => f.classList.remove('active'));
      this.classList.add('active');
      filterItems();
    });
  });

  tagFilters.forEach(filter => {
    filter.addEventListener('click', function () {
      tagFilters.forEach(f => f.classList.remove('active'));
      this.classList.add('active');
      filterItems();
    });
  });

  // Lightbox instance
  let lightbox = null;

  function initLightbox() {
    try {
      if (lightbox && typeof lightbox.destroy === 'function') {
        lightbox.destroy();
        lightbox = null;
      }

      const anchors = Array.from(document.querySelectorAll('.gallery-link')).filter(a => a.offsetParent !== null);
      if (!anchors.length) return;

      lightbox = new SimpleLightbox(anchors, {
        captions: true,
        captionSelector: 'img',
        captionType: 'attr',
        captionsData: 'title',
        nav: true,
        loop: true,
        history: false,
        close: true,
        enableKeyboard: true
      });
      window.galleryLightbox = lightbox;
    } catch (err) {
      console.warn('Lightbox init failed', err);
    }
  }

  function refreshLightbox() {
    if (lightbox && typeof lightbox.refresh === 'function') {
      lightbox.refresh();
    } else {
      initLightbox();
    }
  }

  // Init on load
  initLightbox();
});
