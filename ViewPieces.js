export class ViewPieces{
    // gets controlPieces instance and div element where pieces will be rendered
    constructor(controlPieces, piecesDiv){
        this.controlPieces = controlPieces;
        this.piecesDiv = piecesDiv;
        this.renderPieces()
    }

    // renders pieces in piecesDiv, each piece is div element with class piece, data-pieceId attribute and onclick event listener
    // there is also rotate and mirror button for each piece inside div element with required attribute data-pieceId
    renderPieces(){
        this.piecesDiv.innerHTML = '';
        Object.entries(this.controlPieces.pieces).forEach(([key, piece]) => {
            let pieceDiv = document.createElement('div');
            if (this.controlPieces.chosenPiece === key) pieceDiv.classList.add('chosen');
            pieceDiv.classList.add('piece');
            pieceDiv.dataset.pieceId = key
            pieceDiv.onclick = this.pieceClickHandler.bind(this);
            let [table, buttons] = this._renderPiece(piece, key, pieceDiv);

            pieceDiv.innerHTML = pieceDiv.innerHTML + table;
            pieceDiv.appendChild(buttons);
            this.piecesDiv.appendChild(pieceDiv);
        });

    }

    // renders piece in html, piece is array of arrays, each array is row of piece
    // output should be table  with rows and columns, each cell is div element with class cell, also colored from controlPieces.colors
    // there is also rotate and mirror button for piece that will appear on chosenPiece
    _renderPiece(piece, key, pieceDiv){
        let result = '';
        result += '<table cellspacing="0">';
        piece.forEach((row, i) => {
            result += '<tr>';
            row.forEach((cell, j) => {
                let backgroundColor = 'transparent';
                if (cell !== 0) {
                    let color = this.controlPieces.colors[cell];
                    const { r, g, b } = this._transformColorFromHexToRgb(color);
                    backgroundColor = `rgb(${r}, ${g}, ${b})`;
                }
                result += `<td class="cell" style="background-color: ${backgroundColor};"></td>`;
            });
            result += '</tr>';
        });
        result += '</table>';

        let buttonContainer = document.createElement('div')

        if (this.controlPieces.chosenPiece === key){

            let rotateButton = document.createElement('button');
            rotateButton.onclick = this.rotateButtonHandler.bind(this);
            rotateButton.innerHTML = 'Rotate';
            rotateButton.classList.add('rotate-button');
            buttonContainer.appendChild(rotateButton);

            let mirrorButton = document.createElement('button');
            mirrorButton.onclick = this.mirrorButtonHandler.bind(this);
            mirrorButton.innerHTML = 'Mirror';
            mirrorButton.classList.add('mirror-button');
            buttonContainer.appendChild(mirrorButton);
        }
        return [result, buttonContainer];
    }

    _transformColorFromHexToRgb(hex){
        let result = /^0x?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
        return result ? {
            r: parseInt(result[1], 16),
            g: parseInt(result[2], 16),
            b: parseInt(result[3], 16)
        } : null;
    }

    pieceClickHandler(event){
        event.preventDefault();
        event.stopPropagation(); // Prevent event from bubbling up
        let pieceId = event.target.dataset.pieceId;
        if(this.controlPieces.chosenPiece === pieceId){
            this.controlPieces.chosenPiece = 0;
        } else {
            this.controlPieces.chosenPiece = pieceId;
        }

        this.renderPieces()
    }

    rotateButtonHandler(event){
        event.stopPropagation();
        event.preventDefault();
        this.controlPieces.rotateClickHandler(this.controlPieces.chosenPiece);
        this.renderPieces()
    }

    mirrorButtonHandler(event){
        event.preventDefault();
        event.stopPropagation();
        this.controlPieces.mirrorClickHandler();
        this.renderPieces()
    }
}