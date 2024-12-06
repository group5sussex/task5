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

        this.eventSource = this.startSSE(JSON.stringify(this.pyramid), this.onMessage, this.onError);
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
}