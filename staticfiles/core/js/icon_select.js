(function($) {
    $(document).ready(function() {
        // Function to update the displayed icon
        function updateIconDisplay(selectElement) {
            var selectedOption = $(selectElement).find('option:selected');
            var iconClass = selectedOption.data('icon');
            var iconPreview = $(selectElement).next('.icon-preview');

            if (iconPreview.length === 0) {
                iconPreview = $('<span class="icon-preview" style="margin-left: 10px;"></span>');
                $(selectElement).after(iconPreview);
            }

            iconPreview.html('<i class="' + iconClass + '"></i>');
        }

        // Apply to all icon select widgets on load
        $('.field-icon select').each(function() {
            updateIconDisplay(this);
        });

        // Update icon display on change
        $(document).on('change', '.field-icon select', function() {
            updateIconDisplay(this);
        });

        // Handle dynamic formsets (if any)
        $(document).on('formset:added', function(event, row) {
            $(row).find('.field-icon select').each(function() {
                updateIconDisplay(this);
            });
        });
    });
})(django.jQuery);