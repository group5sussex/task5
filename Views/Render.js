import * as THREE from 'three';
import {Light} from "./Light";
import {OrbitControls} from "three/addons/controls/OrbitControls";

export class Render{
    constructor(size = {innerWidth: 640, innerHeight: 480},
                scene = new THREE.Scene(),
                camera = new THREE.PerspectiveCamera( 75, size.innerWidth / size.innerHeight, 30, 1000 ),
                renderer= new THREE.WebGLRenderer(),
                element = document.body,
                camPos = {x: 0, y: 200, z: 200},){
        this.size = size;
        this.scene = scene;
        this.camera = camera
        this.renderer = renderer
        this.renderer.setSize( size.innerWidth, size.innerHeight );
        this.renderer.setClearColor(0x000000, 0); // Transparentness of the background
        element.appendChild( renderer.domElement );
        camera.position.y = camPos.y;
        camera.position.z = camPos.z;
        camera.position.x = camPos.x;


        const directionalLight = Light.create({x:-100, y:100, z:100});
        this.scene.add(directionalLight);

        const controls = new OrbitControls(this.camera, this.renderer.domElement);
        controls.update();
    }

    addMesh(mesh){
        this.scene.add(mesh);
    }

    render(){
        this.renderer.render( this.scene, this.camera );
    }


}