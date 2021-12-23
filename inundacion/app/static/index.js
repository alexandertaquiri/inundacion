import { RecorridoMap } from "./RecorridoMap.js";

const submitHandler = (event, map) => {
    if (!marker) {
        event.preventDefault();
        alert('Debes ingresar un recorrido en el mapa');
    }
    else {
        const name = document.querySelector('#detalleCoordenadas').value;
        
        //Obtiene todas las coordenadas del recorrido
        const coordinates = map.drawlawers[0].getLatLngs().flat().map(coordinate => {
            return { lat: coordinate.lat, lng: coordinate.lng }
        });

        const formData = new FormData();
        formData.append('name', name);
        formData.append('cordinates', JSON.stringify(coordinates));

        // fetch ('/recorridos', {
        //     method = 'POST',
        //     body: formData
        // })     
    }

    window.onload = () => {
        const map = new RecorridoMap ({
            selector: 'map',
            addSearch: true
        });

        const form = document.querySelector('#create-form');
        form.addEventListener('submit', (event) => submitHandler (event, map));
    }
}
