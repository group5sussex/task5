import {Render} from './Render.js';
import WebGL from 'three/addons/capabilities/WebGL.js'
import {Pyramid} from './Pyramid.js';
import {ControlPyramidView} from './ControlPyramidView.js';
import {ControlPieces} from "./ControlPieces";
import {ViewPieces} from "./ViewPieces";
import {ControlPiecePlacement} from "./ControlPiecePlacement";
import {ControlSolutions} from "./ControlSolutions";
import {ControlResetButton} from "./ControlResetButton";
import {ControlSendButton} from "./ControlSendButton";



const init = () => {
    let piecesHolder = document.getElementById("pieces");
    let piecesControl = new ControlPieces()
    let controlPieces = new ViewPieces(piecesControl, piecesHolder);

    const size = {innerWidth: 640, innerHeight: 480};

    let render = new Render(
        size,
        undefined,
        undefined,
        undefined,
        document.getElementById('scene'),
        {x: 100/2, y: 350/2, z: 200/2}
    );

    let pyramid = new Pyramid(render, piecesControl.colors);

    let controlView = new ControlPyramidView(pyramid, document.getElementById("button-layer"),
        document.getElementById("button-row"), document.getElementById("button-column"));

    let controlPiecePlacement = new ControlPiecePlacement(render, pyramid, piecesControl, controlView);
    let controlSolutions = new ControlSolutions(
        document.getElementById("next"),
        document.getElementById("prev"),
        document.getElementById("solution"),
        pyramid,
        document.getElementById("solution-changer"));
    let resetButton = document.getElementById("reset");
    let controlResetButton = new ControlResetButton(resetButton, pyramid, controlPieces, render, controlSolutions);
    let sendButton = document.getElementById("solve");


    let controlSendButton = new ControlSendButton(controlSolutions, sendButton, pyramid, "http://127.0.0.1:8000/kanoodle/3d/submit");
}

if ( WebGL.isWebGL2Available() ) {
    init();
} else {
    const warning = WebGL.getWebGL2ErrorMessage();
    console.log(warning);
}