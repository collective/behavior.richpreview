import tippy from 'tippy.js';


let instance = null;
export default class RichPreview {
  constructor() {
    if (instance != null) {
      return instance;
    }
    instance = this;

    // Change this option when style the tooltip
    this.dontHide = false;

    this.enabled = ($('#viewlet-richpreview').attr('data-enabled') === 'True');
    this.loadingMessage = $('#viewlet-richpreview > .richpreview-template').html().trim()
    this.errorMessage = $('#viewlet-richpreview').attr('data-error-message');

    if (this.enabled) {
      this.createTooltip();
    }
  }
  createTooltip() {
    tippy('#content a', {
      animation: 'shift-toward',
      arrow: true,
      theme: 'light',
      html: '#viewlet-richpreview > .richpreview-template',
      onShow: this.onShow.bind(this),
      // prevent tooltip from displaying over button
      popperOptions: {
        modifiers: {
          preventOverflow: {
            enabled: false
          },
          hide: {
            enabled: false
          }
        }
      }
    });
  }
  onShow(tip) {
    if (this.dontHide) {
      tip.hide = function() {};
    }

    const content = tip.popper.querySelector('.tippy-content');

    if (this.loading || (content.innerHTML || '').trim() !== this.loadingMessage) {
      return;
    }
    
    let $a = $(tip.reference);

    this.loading = true

    $.ajax({
      url: `${portal_url}/@@richpreview-json-view/${$a.attr('data-richpreview')}`,
      context: this
    }).done(function(data) {
      if ($.isEmptyObject(data)) {
        content.innerHTML = this.errorMessage;
        this.loading = false;
        return;
      }

      let $template = $('#viewlet-richpreview .richpreview');

      let $image = $('.richpreview-image > img', $template);
      $image.attr('src', data.image);

      let $text = $('.richpreview-text', $template);
      $text.html(data.title);

      content.innerHTML = $template[0].outerHTML;
      this.loading = false;
    }).fail(function() {
      content.innerHTML = this.errorMessage;
      this.loading = false;
    });
  }
}
