export class ControlPieces {
    constructor(sizeMaxPyramid = 5,
        pieces = {
            1: [[1, 1, 1], [1, 0, 1]],
            2: [[0, 0, 2, 2], [2, 2, 2, 0]],
            3: [[0, 3, 0], [3, 3, 0], [0, 3, 3]],
            4: [[0, 4, 0], [4, 4, 4]],
            5: [[0, 5, 0, 0], [5, 5, 5, 5]],
            6: [[0, 6, 6], [6, 6, 6]],
            7: [[0, 7, 7], [7, 7, 0]],
            8: [[8, 8], [8, 0], [8, 0]],
            9: [[9, 9, 9], [0, 0, 9], [0, 0, 9]],
            10: [[10, 0, 0, 0], [10, 10, 10, 10]],
            11: [[0, 11], [11, 11]],
            12: [[12, 12, 0], [0, 12, 12], [0, 0, 12]]
        }, colors = {
        1: '0x005F73FF',
        2: '0x0A9396FF',
        3: '0x94D2BDFF',
        4: '0xE9D8A6FF',
        5: '0xEE9B00FF',
        6: '0xEE9B00FF',
        7: '0xBB3E03FF',
        8: '0xBB3E03FF',
        9: '0x9B2226FF',
        10: '0xA4363AFF',
        11: '0xC7652CFF',
        12: '0xD28B55FF',
    }){
        this.pieces = pieces;
        this.colors = colors;
        // Array with length of pieces, each i-th element is status of i-th piece (0 - not used, 1 - used)
        this.usedPieces = new Array(this.pieces.length).fill(0);
        this.statePieces = this._createPiecesStateHolder();
        // Index of chosen piece, 0 - no piece chosen, rest - index of piece
        this.chosenPiece = 0;

        this.virtualBoard = this._createVirtualBoard(sizeMaxPyramid);
    }

    // event handler that handles click on rotate button by rotating chosenPiece and saving in this.pieces, there is attribute data-pieceId in html that has index of piece
    rotateClickHandler(){
        if (this.chosenPiece === 0) return;

        this.pieces[this.chosenPiece] = this.rotatePiece(this.chosenPiece);
    }

    // event handler that handles click on mirror button by mirroring chosenPiece and saving in this.pieces, there is attribute data-pieceId in html that has index of piece
    mirrorClickHandler(){
        if (this.chosenPiece === 0) return;

        this.pieces[this.chosenPiece] = this.mirrorPiece(this.chosenPiece);
    }

    _createVirtualBoard(size){
        let result = [];

        for(let i = 0; i < size; i++){
            let layer = [];
            for(let j = 0; j < i; j++){
                let row = [];
                for(let k = 0; k < i; k++){
                    row.push(0);
                }
                layer.push(row);
            }
            result.push(layer);
        }

        return result;
    }

    _createPiecesStateHolder(){
        let result = [];
        for(let i = 0; i < Object.keys(this.pieces).length; i++){
            result.push({
                rotation: 0,
                mirror: 0,
            });
        }
        return result
    }

    _rotate90Clockwise(matrix) {
        const rows = matrix.length;
        const cols = matrix[0].length;
        const rotated = Array.from({ length: cols }, () => Array(rows));

        for (let i = 0; i < rows; i++) {
            for (let j = 0; j < cols; j++) {
                rotated[j][rows - 1 - i] = matrix[i][j];
            }
        }
        return rotated;
    }

    _mirrorByY(matrix) {
        let result = [];

        for (let i = 0; i < matrix.length; i++) {
            let row = [];
            for (let j = matrix[i].length - 1; j >= 0; j--) {
                row.push(matrix[i][j]);
            }
            result.push(row);
        }


        return result;
    }


    _copyVirtualBoard(vBoard){
        let result = [];

        for(let i = 0; i < vBoard.length; i++){
            let layer = [];
            for(let j = 0; j < vBoard[i].length; j++){
                let row = [];
                for(let k = 0; k < vBoard[i][j].length; k++){
                    row.push(vBoard[i][j][k]);
                }
                layer.push(row);
            }
            result.push(layer);
        }

        return result;
    }

    placeFigureOnLayer(layer, figure, x, y) {
        let copy = this._copyVirtualBoard(this.virtualBoard);

        for (let i = 0; i < figure.length; i++) {
            if (figure[i].length > copy[layer].length)                              return;

            for (let j = 0; j < figure[i].length; j++) {
                if (x + i >= copy[layer].length || y + j >= copy[layer][i].length)  return;
                if (copy[layer][x + i][y + j] !== 0 && figure[i][j] !== 0)          return;
                if (figure[i][j] === 0)                                             continue;


                copy[layer][x + i][y + j] = figure[i][j];
            }
        }
    }

    rotatePiece(pieceId){
        let piece = this.pieces[pieceId];
        let state = this.statePieces[pieceId];

        let rotated = this._rotate90Clockwise(piece);
        state.rotation = (state.rotation + 1) % 4;
        this.pieces[pieceId] = rotated;
        return rotated;
    }

    mirrorPiece(pieceId){
        let piece = this.pieces[pieceId];
        let state = this.statePieces[pieceId];

        let mirrored = this._mirrorByY(piece);
        state.mirror = (state.mirror + 1) % 2;
        this.pieces[pieceId] = mirrored;
        return mirrored
    }
}