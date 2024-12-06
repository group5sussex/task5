export class ControlBoard{
    constructor(ControlPieces, Render){
        this.ControlPieces = ControlPieces;
        this.Render = Render;
    }

    placeFigureOnLayer(layer, figure, x, y){
        for(let i = 0; i < figure.length; i++){
            for(let j = 0; j < figure[i].length; j++){
                this.ControlPieces.virtualBoard[layer][x + i][y + j] = figure[i][j];
            }
        }
    }
}