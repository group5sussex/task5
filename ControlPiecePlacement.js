import * as THREE from "three";

export class ControlPiecePlacement {
    constructor(render, pyramid, piecesControl, controlView){
        this.render = render;
        this.pyramid = pyramid;
        this.pieceControl = piecesControl;
        this.controlView = controlView;
        this._addEventClickMesh(this.render.scene, this.render, this.render.size, this.handlePieceClick.bind(this));
    }

    // places piece on the layer of the pyramid
    placePieceLayer(layer, row, column, pieceId, piece){
        let virtualBoard = this.pyramid.virtualBoard;
        virtualBoard = this.removePiece(pieceId, virtualBoard);
        for (let i = 0; i < piece.length; i++) {
            if (piece[i].length > virtualBoard[layer].length) return;
            for (let j = 0; j < piece[i].length; j++) {
                if (row + i >= virtualBoard[layer].length || column + j >= virtualBoard[layer][i].length) return;
                if (virtualBoard[layer][row + i][column + j] !== 0 && piece[i][j] !== 0) return;
                if (piece[i][j] === 0) continue;
                virtualBoard[layer][row + i][column + j] = piece[i][j];
            }
        }
        this.pyramid.loadVirtualBoard(virtualBoard);
    }

    placingPieceRowX(layer, row, column, pieceId, piece){
        let virtualBoard = this.pyramid.virtualBoard;
        virtualBoard = this.removePiece(pieceId, virtualBoard);
        virtualBoard = this._arrayToObj(virtualBoard);
        let indexes = this._transformCoordinatesToIndex(layer, row, column);
        let diags = this._diagSlicesX(virtualBoard);
        let diag = this._transformDiag(diags[indexes["z"]]);

        indexes["y"] = indexes["y"] - indexes["x"];

        if (!this._putPieceOnDiag(diag, piece, indexes["x"], indexes["y"])) return;
        virtualBoard = this._objToArray(virtualBoard);
        this.pyramid.loadVirtualBoard(virtualBoard);
    }

    placingPieceRowY(layer, row, column, pieceId, piece){
        let virtualBoard = this.pyramid.virtualBoard;
        virtualBoard = this.removePiece(pieceId, virtualBoard);
        virtualBoard = this._arrayToObj(virtualBoard);

        // for (let i = 0; i < virtualBoard.length; i++) {
        //     for (let j = 0; j < virtualBoard[i].length; j++) {
        //         for (let k = 0; k < virtualBoard[i][j].length; k++) {
        //             virtualBoard[i][j][k]["value"] = `${i} ${j} ${k}`;
        //         }
        //     }
        // }
        let slices = this._diagSlicesY(virtualBoard);

        slices = this._removeEmptyArrays(slices);

        let diag = this._transformDiag(slices[4-layer + row + column]);

        let layerIndex = 4 - layer + row + column;
        let rowIndex = row - Math.max(0, row+column  - layer);
        let elementIndex = rowIndex - row + column;

        if(!this._putPieceOnDiag(diag, piece, rowIndex, elementIndex)) return;
        virtualBoard = this._objToArray(virtualBoard);
        this.pyramid.loadVirtualBoard(virtualBoard);
    }

    handlePieceClick(mesh){
        if (!mesh.userData) return;
        if (this.pieceControl.chosenPiece === 0) return;
        if (!this.controlView.state) return;

        let {position, indexL, indexR, indexE, pieceId} = mesh.userData;

        let placeFunctions = {
            layer: this.placePieceLayer.bind(this),
            rowX: this.placingPieceRowX.bind(this),
            rowY: this.placingPieceRowY.bind(this)
        }

        let piece = this.pieceControl.pieces[this.pieceControl.chosenPiece];


        placeFunctions[this.controlView.state](indexL, indexR, indexE, parseInt(this.pieceControl.chosenPiece), piece);
    }

    // removes piece from pyramid by using virtual board
    removePiece(pieceId, virtualBoard){
        let result = [];

        for (let i = 0; i < virtualBoard.length; i++) {
            let layer = [];
            for (let j = 0; j < virtualBoard[i].length; j++) {
                let row = [];
                for (let k = 0; k < virtualBoard[i][j].length; k++) {
                    if (virtualBoard[i][j][k] === pieceId) {
                        row.push(0);
                    }
                    else {
                        row.push(virtualBoard[i][j][k]);
                    }
                }
                layer.push(row);
            }
            result.push(layer);
        }

        return result;
    }

    _arrayToObj(array){
        let result = [];
        for (let i = 0; i < array.length; i++) {
            let layer = [];
            for (let j = 0; j < array[i].length; j++) {
                let row = [];
                for (let k = 0; k < array[i][j].length; k++) {
                    row.push({value: array[i][j][k]});
                }
                layer.push(row);
            }
            result.push(layer);
        }
        return result;
    }

    _objToArray(obj){
        let result = [];
        for (let i = 0; i < obj.length; i++) {
            let layer = [];
            for (let j = 0; j < obj[i].length; j++) {
                let row = [];
                for (let k = 0; k < obj[i][j].length; k++) {
                    row.push(obj[i][j][k]["value"]);
                }
                layer.push(row);
            }
            result.push(layer);
        }
        return result;
    }

    _diagSlicesX(arr){
        let result = [];
        let slices = this._createEmptySlices(arr);
        for (let i = 0; i < arr.length; i++) {
            for (let j = 0; j < arr[i].length; j++) {
                for (let k = 0; k < arr[i][j].length; k++) {
                    let index = this._transformCoordinatesToIndex(i, j, k);
                    slices[index["z"]][index["y"]][index["x"]] = arr[i][j][k];
                }
            }
        }

        result = slices;

        return result;
    }

    _diagSlicesY(arr){
        const slices = [];

        // There are 5 levels: 0 to 4
        // We want 9 slices as before
        for (let n = 1; n <= 9; n++) {
            const slice = [];

            // Each slice n has n sub-arrays
            for (let k = 1; k <= n; k++) {
                const level = 4 - n + k;

                // If the computed level is out of range, just push an empty array
                if (level < 0 || level > 4) {
                    slice.push([]);
                    continue;
                }

                const targetSum = k - 1;
                const subArray = [];

                // Now each level L is a square matrix: indices from 0 to L
                for (let r = 0; r <= level; r++) {
                    for (let c = 0; c <= level; c++) {
                        if (r + c === targetSum) {
                            subArray.push(arr[level][r][c]);
                        }
                    }
                }

                slice.push(subArray);
            }

            slices.push(slice);
        }

        return slices;
    }

    _isEmptyArray(arr) {
        // An array is empty if:
        // 1. It has length 0, or
        // 2. Every element is also an empty array (recursively checked)
        if (!Array.isArray(arr)) return false;
        if (arr.length === 0) return true;

        return arr.every(element =>
            Array.isArray(element) && this._isEmptyArray(element)
        );
    }

    _removeEmptyArrays(arr) {
        if (!Array.isArray(arr)) return arr;

        // Recursively clean each element first
        const cleaned = arr.map(this._removeEmptyArrays.bind(this));

        // Filter out any empty arrays
        return cleaned.filter(element => !this._isEmptyArray(element));
    }


    _createEmptySlices(arr){
        let result = [];
        for (let i = 0; i < arr.length * 2 - 1; i++) {
            let slice = [];
            for (let j = 0; j < (i<=4? i + 1: arr.length * 2 - 1 - i) ; j++) {
                let row = [];
                for (let k = 0; k <= j; k++) {
                    row.push(0);
                }
                slice.push(row);
            }
            result.push(slice);
        }
        return result
    }

    _transformCoordinatesToIndex(x, y, z){
        let result = {};
        result["z"] = 4 - y + z
        result["y"] = x - y - z + 2 * Math.min(x, y, z);
        result["x"] = Math.min(x, y, z);

        return result;
    }

    _transformDiag(arr){
        const maxLength = Math.max(...arr.map(row => row.length));
        const inverted = [];

        for (let col = 0; col < maxLength; col++) {
            const newRow = [];
            for (let row = arr.length - 1; row >= 0; row--) {
                if (arr[row][col] !== undefined) {
                    newRow.push(arr[row][col]);
                }
            }
            inverted.push(newRow);
        }


        for (let i = 0; i < inverted.length; i++) {
            inverted[i] = inverted[i].reverse();
        }

        return inverted;

        // const result = [];
        // const rows = arr.length;
        //
        // for (let i = 0; i < rows; i++) {
        //     const temp = [];
        //     let r = rows - 1 - i; // Start from the bottom row moving upward as i increases
        //     let c = 0;
        //
        //     while (r < rows && c < (arr[r].length)) {
        //         temp.push(arr[r][c]);
        //         r++;
        //         c++;
        //     }
        //
        //     result.push(temp);
        // }
        //
        // return result;
    }

    _putPieceOnDiag(slice, piece, x, y){
        for (let i = 0; i < piece.length; i++) {
            if (piece[i].length > slice.length) return false;
            for (let j = 0; j < piece[i].length; j++) {
                if (piece[i][j] === 0) continue;
                if ((x + i >= slice.length || y + j >= slice[i+x].length)) return false;
                if (slice[x + i][y + j]['value'] !== 0 && piece[i][j] !== 0) return false;
                slice[x + i][y + j]['value'] = piece[i][j];
            }
        }

        return true;
    }

    _addEventClickMesh(mesh, render, size, callback) {
        const raycaster = new THREE.Raycaster();
        const mouse = new THREE.Vector2();

        render.renderer.domElement.addEventListener('click', (event) => {
            const rect = render.renderer.domElement.getBoundingClientRect();
            mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
            mouse.y = - ((event.clientY - rect.top) / rect.height) * 2 + 1;

            raycaster.setFromCamera(mouse, render.camera);
            const intersects = raycaster.intersectObjects(render.scene.children);

            if (intersects.length > 0) {
                callback(intersects[0].object);
            }
        });
    }
}