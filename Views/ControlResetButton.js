import {Pyramid} from "./Pyramid";
import {Render} from "./Render";
import {ControlPieces} from "./ControlPieces";
import {ControlSolutions} from "./ControlSolutions";

export class ControlResetButton{
    constructor(button, pyramid, controlPieces, render, controlSolutions){
        this.button = button;
        this.pyramid = pyramid;
        this.button.addEventListener("click", this.buttonHandler.bind(this));
        this.controlPieces = controlPieces;
        this.render = render;
        this.controlSolutions = controlSolutions;
    }

    buttonHandler(){
        this.controlPieces.reset();
        this.pyramid.reset()
        this.controlSolutions.reset();
    }
}