// Contact Admin JavaScript Enhancements

document.addEventListener('DOMContentLoaded', function() {
    // Enhanced map address functionality
    const mapAddressField = document.querySelector('#id_map_address');
    const latitudeField = document.querySelector('#id_latitude');
    const longitudeField = document.querySelector('#id_longitude');
    
    if (mapAddressField && latitudeField && longitudeField) {
        // Add helper text
        addMapAddressHelper();
        
        // Add geocoding functionality
        addGeocodingButton();
        
        // Add map preview
        addMapPreview();
    }
});

function addMapAddressHelper() {
    const mapAddressField = document.querySelector('#id_map_address');
    if (!mapAddressField) return;
    
    const helper = document.createElement('div');
    helper.className = 'map-address-helper';
    helper.innerHTML = `
        <strong>💡 Tip:</strong> Enter a complete address including street, city, state/province, and country. 
        For example: "123 Main Street, Mumbai, Maharashtra, India"
    `;
    
    mapAddressField.parentNode.insertBefore(helper, mapAddressField.nextSibling);
}

function addGeocodingButton() {
    const mapAddressField = document.querySelector('#id_map_address');
    if (!mapAddressField) return;
    
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'button';
    button.innerHTML = '🌍 Get Coordinates';
    button.style.marginLeft = '10px';
    button.style.marginTop = '5px';
    
    button.addEventListener('click', function() {
        const address = mapAddressField.value.trim();
        if (!address) {
            alert('Please enter an address first.');
            return;
        }
        
        geocodeAddress(address);
    });
    
    mapAddressField.parentNode.appendChild(button);
}

function geocodeAddress(address) {
    const statusDiv = document.createElement('div');
    statusDiv.className = 'geocoding-status loading';
    statusDiv.textContent = 'Getting coordinates...';
    
    const mapAddressField = document.querySelector('#id_map_address');
    mapAddressField.parentNode.appendChild(statusDiv);
    
    // Simulate geocoding (in real implementation, this would call your Django view)
    setTimeout(() => {
        // This is a placeholder - in a real implementation, you'd call a Django view
        // that uses the Google Geocoding API
        statusDiv.className = 'geocoding-status success';
        statusDiv.textContent = 'Coordinates will be generated when you save the form.';
        
        setTimeout(() => {
            statusDiv.remove();
        }, 3000);
    }, 1000);
}

function addMapPreview() {
    const mapAddressField = document.querySelector('#id_map_address');
    const latitudeField = document.querySelector('#id_latitude');
    const longitudeField = document.querySelector('#id_longitude');
    
    if (!mapAddressField || !latitudeField || !longitudeField) return;
    
    const previewDiv = document.createElement('div');
    previewDiv.className = 'map-preview';
    previewDiv.style.display = 'none';
    previewDiv.innerHTML = `
        <div style="padding: 10px; background: #f8f9fa; border-bottom: 1px solid #ddd;">
            <strong>Map Preview:</strong>
        </div>
        <div id="map-preview-container"></div>
    `;
    
    mapAddressField.parentNode.appendChild(previewDiv);
    
    // Show preview when coordinates are available
    function updateMapPreview() {
        const lat = latitudeField.value;
        const lng = longitudeField.value;
        
        if (lat && lng) {
            previewDiv.style.display = 'block';
            const container = document.getElementById('map-preview-container');
            if (container) {
                container.innerHTML = `
                    <iframe 
                        src="https://www.google.com/maps/embed/v1/view?key={{ GOOGLE_MAPS_API_KEY }}&center=${lat},${lng}&zoom=15&maptype=roadmap"
                        width="100%" 
                        height="200" 
                        style="border:0;" 
                        allowfullscreen="" 
                        loading="lazy">
                    </iframe>
                `;
            }
        } else {
            previewDiv.style.display = 'none';
        }
    }
    
    // Update preview when coordinates change
    latitudeField.addEventListener('input', updateMapPreview);
    longitudeField.addEventListener('input', updateMapPreview);
    
    // Initial check
    updateMapPreview();
}

// Add form validation
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('#contactinfo_form');
    if (form) {
        form.addEventListener('submit', function(e) {
            const mapAddress = document.querySelector('#id_map_address').value.trim();
            const latitude = document.querySelector('#id_latitude').value;
            const longitude = document.querySelector('#id_longitude').value;
            
            if (mapAddress && (!latitude || !longitude)) {
                if (confirm('You have entered a map address but coordinates are not set. Would you like to continue? The coordinates will be generated automatically when you save.')) {
                    return true;
                } else {
                    e.preventDefault();
                    return false;
                }
            }
        });
    }
});

// Add keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl+G to geocode address
    if (e.ctrlKey && e.key === 'g') {
        e.preventDefault();
        const mapAddressField = document.querySelector('#id_map_address');
        if (mapAddressField && mapAddressField.value.trim()) {
            geocodeAddress(mapAddressField.value.trim());
        }
    }
});
