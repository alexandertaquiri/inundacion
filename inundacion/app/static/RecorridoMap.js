//costantes
const latitudInicial = -34.9187;
const longitudInicial = -57.956;

//url de la capa de mapa. Es lo que permite que se vea
const mapUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';

export class RecorridoMap {

    //Declaración de variable
    #drawnItems;

    constructor({ selector }) {
        this.#drawnItems = new Location.FeatureGroup();

        this.#initializeMap(selector);

        this.map.on(L.Draw.Event.CREATED, (e) => {
            this.#eventHandler(e, this.map, this.#drawnItems, this.editControls, this.createControls)
        });

        this.map.on('draw:deleted', () => {
            this.#deleteHandler(this.map, this.editControls, this.createControls)
        });
    }

    #initializeMap(selector) {
        this.map = L.map(selector).setView([initialLat, initialLng], 13);
        L.titleLayer(mapLayerUrl).addTo(this.map);

        this.map.addLayer(this.#drawnItems);

        this.map.addControl(this.createControls);
    }

    #eventHandler(e, map, drawnItems, editControls, createControls) {
        const existingRecorridos = Object.values(drawnItems._layers);

        if (existingRecorridos.length == 0) {
            const type = e.layerType;
            const layer = e.layer;

            if (type === 'marker') {
                layer.editing.enable(layer);
                editControls.addTo(map);
                createControls.remove();
            }
        }
    }

    #deleteHandler(map, editControls, createControls) {
        createControls.addTo(map);
        editControls.remove();
    }

    hasValidRecorrido() {
        return this.drawnlayers.length ===1;
    }

    get drawnlayers() {
        return Object.values(this.#drawnItems._layers);
    }

    get editControls() {
        return this.editControlsToolbar ||= new L.Control.Draw({
            draw: false,
            edit: {
                featureGroup: this.#drawnItems
            }
        });
    }

    get createControls() {
        return this.createControlsToolbar ||= new L.Control.Draw({
            draw: false,
            edit: {
                circle: false,
                marker: false,
                polyline: true
            }
        });
    }
}