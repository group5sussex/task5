import * as THREE from "three";
import {SceneUtilities} from "./SceneUtilities";

export class Pyramid{
    pyramidHolder = [];
    defaultColor = 0x808080;


    constructor(render, colors) {
        this.pyramidHolder = this.createPyramid(5, 10);

        this.colors = colors;
        this.forEachElement((element, indexL, indexR, indexE) => {
            element.userData = {
                position: { x: element.position.x, y: element.position.y, z: element.position.z },
                indexL: indexL,
                indexR: indexR,
                indexE: indexE,
                pieceId: 0,
            };
            render.addMesh(element);
        });

        this.forEachElement((element) => {
            element.position.x -= 40;
            element.position.y -= 40;

            element.userData.position.x -= 40;
            element.userData.position.y -= 40;
        });

        SceneUtilities.rotateScene(render.scene, {x: -90, y: 0, z: 40});

        function animate() {
            render.render();
        }

        render.renderer.setAnimationLoop(animate);

        this._virtualBoard = this._createVirtualBoard();
    }

    forEachElement(callback){
        this.pyramidHolder.forEach((layer, indexL) =>{
            layer.forEach((row, indexR) => {
                row.forEach((element, indexE) => {
                    callback(element, indexL, indexR, indexE);
                });
            });
        });

        return this.pyramidHolder;
    }

    get pyramid(){
        return this.pyramidHolder;
    }

    // creates copy of the virtual board
    get virtualBoard(){
        let result = [];
        for (let i = 0; i < this._virtualBoard.length; i++) {
            let layer = [];
            for (let j = 0; j < this._virtualBoard[i].length; j++) {
                let row = [];
                for (let k = 0; k < this._virtualBoard[i][j].length; k++) {
                     row.push(this._virtualBoard[i][j][k]);
                }
                layer.push(row);
            }
            result.push(layer);
        }
        return result;
    }

    loadVirtualBoard(virtualBoard){
        this._virtualBoard = virtualBoard;
        this._virtualToRealBoard(this.virtualBoard);
    }


    _virtualToRealBoard(virtualBoard){
        for (let i = 0; i < virtualBoard.length; i++) {
            for (let j = 0; j < virtualBoard[i].length; j++) {
                for (let k = 0; k < virtualBoard[i][j].length; k++) {
                    if (virtualBoard[i][j][k] === 0){
                        this.pyramidHolder[i][j][k].material.color.set(this.defaultColor);
                        this.pyramidHolder[i][j][k].userData.pieceId = 0;
                    } else {
                        this.pyramidHolder[i][j][k].material.color.set(parseInt(this.colors[virtualBoard[i][j][k]], 16));
                        this.pyramidHolder[i][j][k].userData.pieceId = virtualBoard[i][j][k];
                    }
                }
            }
        }
    }

    createPyramid (numOfLayers, radius){
        let result = [];

        for (let i = 0; i < numOfLayers; i++) {
            let layer = this._createLayerOfPyramid(i+1, radius, numOfLayers-(i+1));
            result.push(layer);
        }

        return result;
    }

    _createLayerOfPyramid (side, radius, zIndex){
        let result = [];

        for (let i = 0; i < side; i++) {
            let row = this._createRowOfLayer(side, radius, i, zIndex);
            result.push(row);
        }

        return result;
    }

    _createRowOfLayer(length, radius, yIndex, zIndex) {
        let result = [];

        let yCoordinate = (yIndex * radius * 2) + radius * zIndex;
        let zCoordinate = zIndex * (radius * 2**0.5);


        for (let i = 0; i < length; i++) {

            let xCoordinate = (i * radius * 2) + (zIndex * radius);

            let sphere = this._createSphere(radius, this.defaultColor, 8, 8);
            sphere.position.set(xCoordinate, yCoordinate, zCoordinate);
            result.push(sphere);
        }

        return result;
    }

    _createSphere (radius, color, widthS = 16, heightS = 32) {
        const geometry = new THREE.SphereGeometry(radius, widthS, heightS);
        const material = new THREE.MeshStandardMaterial({color: color});
        return new THREE.Mesh(geometry, material);
    };



    _createVirtualBoard(){
        let result = [];

        for (let i = 0; i < this.pyramidHolder.length; i++) {
            let layer = [];
            for (let j = 0; j < this.pyramidHolder[i].length; j++) {
                let row = [];
                for (let k = 0; k < this.pyramidHolder[i][j].length; k++) {
                    row.push(0);
                }
                layer.push(row);
            }
            result.push(layer);
        }
        return result
    }
}