export class ControlPyramidView {
    switcher = {layer: false, rowY: false, rowX: false};

    constructor(pyramid, layerButton, rowYButton, rowXButton) {
        this.Pyramid = pyramid;
        this.layerButton = layerButton;
        this.rowYButton = rowYButton;
        this.rowXButton = rowXButton;

        this.layerButton.addEventListener("click", this.layerButtonHandler.bind(this));
        this.rowYButton.addEventListener("click", this.rowYButtonHandler.bind(this));
        this.rowXButton.addEventListener("click", this.rowXButtonHandler.bind(this));
        this.defaultPositions = this._saveUserData(pyramid);
    }

    rowYButtonHandler() {
        let rowY = !this.switcher.rowY;
        let layer = false;
        let rowX = false;


        this.updateView(rowY, layer, rowX);
    }

    rowXButtonHandler() {
        let rowX = !this.switcher.rowX;
        let layer = false;
        let rowY = false;


        this.updateView(rowY, layer, rowX);
    }

    layerButtonHandler() {
        let layer = !this.switcher.layer;
        let rowY = false;
        let rowX = false;

        this.updateView(rowY, layer, rowX);
    }

    get state(){
        for (const key in this.switcher) {
            if (this.switcher[key]) {
                return key;
            }
        }
        return false;
    }

    updateView(rowY, layer, rowX){
        const params = { rowY, layer, rowX };
        const divideFunctions = {
            rowY: this.divideByRowsY.bind(this),
            layer: this.divideByLayers.bind(this),
            rowX: this.divideByRowsX.bind(this),
        };
        const multiplyFunctions = {
            rowY: this.multiplyByRows.bind(this),
            layer: this.multiplyByLayers.bind(this),
            rowX: this.multiplyByRows.bind(this),
        };

        for (const axis in params) {
            if (this.switcher[axis] !== params[axis]) {
                if (params[axis]) {
                    divideFunctions[axis](this.Pyramid);
                } else {
                    multiplyFunctions[axis](this.Pyramid);
                }
            }
        }

        Object.assign(this.switcher, params);
    }

    divideByLayers(pyramid, scale = 30){

        const addZCoordinate = (sphere, l, r, e) => {
            let xc = sphere.position.x;
            let yc = sphere.position.y;
            let zc = sphere.position.z;

            let xc1 = xc;
            let yc1 = yc;
            let zc1 = zc + (scale*(4-l));

            sphere.position.set(xc1, yc1, zc1);
        }

        pyramid.forEachElement(addZCoordinate);
    }

    divideByRowsY(pyramid, scale = 1.5){

        const addYCoordinate = (sphere, l, r, e) => {
            let xc = sphere.position.x;
            let yc = sphere.position.y;
            let zc = sphere.position.z;

            let a = (xc+yc)

            let delta = a === 0 ? 0 : 1;

            let xc1 = xc + delta * scale * ((a)/2);
            let yc1 = yc + delta * scale * ((a)/2);
            sphere.position.set(xc1, yc1, zc);
        }

        pyramid.forEachElement(addYCoordinate);
    }

    divideByRowsX(pyramid, scale = 1.5){

        const addYCoordinate = (sphere, l, r, e) => {
            let xc = sphere.position.x;
            let yc = sphere.position.y;
            let zc = sphere.position.z;

            let a = (yc - xc)

            let delta = a === 0 ? 0 : 1;

            let xc1 = xc - delta * scale * (a/2);
            let yc1 = yc + delta * scale * (a/2);
            sphere.position.set(xc1, yc1, zc);
        }

        pyramid.forEachElement(addYCoordinate);
    }

// inverse functions of divideByLayers and divideByRows
    multiplyByLayers(pyramid, scale = 30){

        const addZCoordinate = (sphere, l, r, e) => {
            let xc = sphere.position.x;
            let yc = sphere.position.y;
            let zc = sphere.position.z;

            let xc1 = xc;
            let yc1 = yc;
            let zc1 = zc - (scale*(4-l));

            sphere.position.set(xc1, yc1, zc1);
        }

        pyramid.forEachElement(addZCoordinate);
    }

    multiplyByRows(pyramid){

        let defaultPyramidHolder = this.defaultPositions;

        const addYCoordinate = (sphere, l, r, e) => {
            let xc1 = defaultPyramidHolder[l][r][e].position.x;
            let yc1 = defaultPyramidHolder[l][r][e].position.y;
            let zc1 = defaultPyramidHolder[l][r][e].position.z;

            sphere.position.set(xc1, yc1, zc1);
        }

        pyramid.forEachElement(addYCoordinate);

    }


    _saveUserData(pyramid){
        let layersLength = pyramid.pyramidHolder.length;

        let defaultUserData = [];
        for (let i = 0; i < layersLength; i++) {
            let rowsLength = pyramid.pyramidHolder[i].length;

            let layer = [];

            for (let j = 0; j < rowsLength; j++) {
                let row = [];

                let elementsLength = pyramid.pyramidHolder[i][j].length;

                for (let k = 0; k < elementsLength; k++) {
                    let element = pyramid.pyramidHolder[i][j][k];
                    let userData = element.userData;
                    row.push(userData);
                }
                layer.push(row);
            }
            defaultUserData.push(layer);
        }
        return defaultUserData;
    }
}