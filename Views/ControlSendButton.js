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

    async _sendGetRequest() {
        try {
            const response = await fetch(`${this.url}/?positions=${encodeURIComponent(JSON.stringify(this.pyramid.virtualBoard))}`);

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