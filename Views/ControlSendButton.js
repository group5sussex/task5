export class ControlSendButton{
    constructor(controlSolutions, button, pyramid, url){
        this.button = button;
        this.pyramid = pyramid;
        this.controlSolutions = controlSolutions;
        this.button.addEventListener("click", this.buttonHandler.bind(this));
        this.eventSource = null;
        this.url = url;
    }

    buttonHandler(){
        this.close_connection();

        // this.eventSource = this.startSSE(JSON.stringify(this.pyramid.virtualBoard), this.onMessage, this.onError);

        let data = this._sendGetRequest();
        let solutions;
        data.then((data) => {
            for (const solution of data) {
                solutions = this._transformSolution(solution);

                this.controlSolutions.addSolution(solutions);
            }
        });
    }

    close_connection(){
        if (this.eventSource) {
            this.eventSource.close();
            this.eventSource = null;
        }
    }

    startSSE(data, onMessage, onError) {
        const eventSource = new EventSource(`${this.url}/?positions=${encodeURIComponent(data)}`);

        eventSource.onmessage = onMessage;

        eventSource.onerror = onError;

        return eventSource;
    }

    onError(event) {
        console.error("EventSource failed:", event);
        this.close_connection();
    }

    onMessage(event) {
        const solution = JSON.parse(event.data);
        this.controlSolutions.addSolution(solution);

    }

    _transformSolution(data){
        let solution = this._fixKeys(data);

        solution = this._fixCoordinates(solution);

        solution = this._solutionToVBoard(solution);

        return solution;
    }

    _fixKeys(data) {
        let solution = {}
        for (const key in data) {
            solution[parseInt(key) - 54] = data[key];
        }
        return solution
    }

    _fixCoordinates(solution) {
        let fixedSolution = {};
        for (const key in solution) {
            fixedSolution[key] = solution[key].map((position) => {
                return [position[0], position[1], 4-position[2]];
            });
        }
        return fixedSolution;
    }

    _solutionToVBoard(solution){
        let vBoard = this.pyramid.virtualBoard;
        for (const key in solution) {
            for (const position of solution[key]) {
                vBoard[position[2]][position[1]][position[0]] = parseInt(key)
            }
        }
        return vBoard
    }

    _vBoardToSolution(vBoard){
        let solution = {};
        for (let i = 0; i < vBoard.length; i++) {
            for (let j = 0; j < vBoard[i].length; j++) {
                for (let k = 0; k < vBoard[i][j].length; k++) {
                    if (vBoard[i][j][k] !== 0) {
                        if (solution[vBoard[i][j][k]] === undefined) {
                            solution[vBoard[i][j][k]] = [];
                        }
                        solution[vBoard[i][j][k]].push([k, j, i]);
                    }
                }
            }
        }

        return solution
    }

    _unFixCoordinates(solution) {
        let fixedSolution = {};
        for (const key in solution) {
            fixedSolution[key] = solution[key].map((position) => {
                return [position[0], position[1], 4-position[2]];
            });
        }
        return fixedSolution;
    }

    _unFixKeys(data) {
        let solution = {}
        for (const key in data) {
            solution[parseInt(key) + 54] = data[key];
        }
        return solution
    }

    _fromObjToArr(solution){
        let result = [];

        for (const key in solution) {
            result.push({[key]: solution[key]});
        }

        return result
    }

    _prepareOutput(){
        let sendingData = this._vBoardToSolution(this.pyramid.virtualBoard)
        sendingData = this._unFixCoordinates(sendingData)
        sendingData = this._unFixKeys(sendingData)
        sendingData = this._fromObjToArr(sendingData)
        return sendingData
    }

    async _sendGetRequest() {
        let sendingData = this._prepareOutput();
        console.log('Sending Data:', JSON.stringify(sendingData))

        try {
            const response = await fetch(`${this.url}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                    // 'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: JSON.stringify({
                    "initial_state": sendingData
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const data = await response.json(); // Parse the JSON from the response
            console.log('Saved Value:', data.key); // Replace 'key' with the desired property

            return data; // Return the fetched data
        } catch (error) {
            console.error('Error fetching data:', error);
            throw error; // Re-throw the error if necessary
        }
    }
}