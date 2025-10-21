(function($) {
  $.fn.imagePopup = function(options) {
    console.log('imagePopup plugin initialized'); // Debug: Confirm plugin initialization
    var settings = $.extend({
      overlay: true,
      closeButton: true,
      zoom: true,
      controls: true,
      caption: true,
      navigation: true,
      onOpen: function() {},
      onClose: function() {},
      onLoad: function() {}
    }, options);

    var $body = $('body');
    var $overlay = $('<div id="zz_frame"></div>');
    var $media = $('<div id="zz_media"></div>');
    var $close = $('<button class="zz_close">&times;</button>');
    var $controls = $('<div class="zz_controls"></div>');
    var $zoomIn = $('<button class="zz_zoom_in">+</button>');
    var $zoomOut = $('<button class="zz_zoom_out">-</button>');
    var $caption = $('<div class="zz_caption"></div>');
    var $prev = $('<button class="zz_prev">&lt;</button>');
    var $next = $('<button class="zz_next">&gt;</button>');

    var currentImageIndex = 0;
    var images = [];

    function openPopup(index) {
      console.log('openPopup called with index:', index); // Debug: Confirm openPopup call
      currentImageIndex = index;
      var image = images[currentImageIndex];

      $media.empty();
      $media.append($('<img src="' + image.src + '"></div>'));

      if (settings.caption && image.caption) {
        $caption.text(image.caption);
        $media.append($caption);
      }

      if (settings.zoom) {
        $controls.append($zoomIn).append($zoomOut);
      }

      if (settings.navigation && images.length > 1) {
        $controls.append($prev).append($next);
      }

      if (settings.controls) {
        $media.append($controls);
      }

      if (settings.closeButton) {
        $media.append($close);
      }

      $overlay.append($media);
      $body.append($overlay);

      $overlay.fadeIn(function() {
        settings.onOpen();
        settings.onLoad();
      });
    }

    function closePopup() {
      $overlay.fadeOut(function() {
        $overlay.remove();
        settings.onClose();
      });
    }

    function zoomImage(scale) {
      var $img = $media.find('img');
      var currentScale = $img.data('scale') || 1;
      var newScale = currentScale * scale;
      $img.css({
        transform: 'scale(' + newScale + ')',
        'transform-origin': 'center center'
      }).data('scale', newScale);
    }

    this.each(function() {
      console.log('Processing element:', this); // Debug: Log each element being processed
      var $this = $(this);
      images.push({
        src: $this.attr('src'),
        caption: $this.attr('alt')
      });

      $this.on('click', function() {
        var index = $(this).index('.zz_image');
        openPopup(index);
      });
    });

    $close.on('click', closePopup);
    $overlay.on('click', function(e) {
      if ($(e.target).is($overlay)) {
        closePopup();
      }
    });

    $zoomIn.on('click', function() {
      zoomImage(1.2);
    });

    $zoomOut.on('click', function() {
      zoomImage(0.8);
    });

    $prev.on('click', function() {
      var prevIndex = (currentImageIndex - 1 + images.length) % images.length;
      openPopup(prevIndex);
    });

    $next.on('click', function() {
      var nextIndex = (currentImageIndex + 1) % images.length;
      openPopup(nextIndex);
    });

    return this;
  };
}(jQuery));