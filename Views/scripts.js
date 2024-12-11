import * as THREE from "three";

const createSphere = (radius, color, widthS = 16, heightS = 32) => {
    const geometry = new THREE.SphereGeometry(radius, widthS, heightS);
    const material = new THREE.MeshStandardMaterial({color: color});
    return new THREE.Mesh(geometry, material);
};

const createLight = (pos = {x:100, y:100, z:100}, color, intensity) => {
    const light = new THREE.DirectionalLight(color, intensity);
    light.position.set(pos.x, pos.y, pos.z).normalize();
    return light;
}

const createPyramid = (numOfLayers, radius) => {
    let result = [];

    for (let i = 0; i < numOfLayers; i++) {
        let layer = createLayerOfPyramid(i+1, radius, numOfLayers-(i+1));
        result.push(layer);
    }

    return result;
}

const createLayerOfPyramid = (side, radius, zIndex) => {
    let result = [];

    for (let i = 0; i < side; i++) {
        let row = createRowOfLayer(side, radius, i, zIndex);
        result.push(row);
    }

    return result;
}

const createRowOfLayer = (length, radius, yIndex, zIndex) => {
    let result = [];

    let yCoordinate = (yIndex * radius * 2) + radius * zIndex;
    let zCoordinate = zIndex * (radius * 2**0.5);


    for (let i = 0; i < length; i++) {

        let xCoordinate = (i * radius * 2) + (zIndex * radius);

        let sphere = createSphere(radius, 0x808080, 8, 8);
        sphere.position.set(xCoordinate, yCoordinate, zCoordinate);
        result.push(sphere);
    }

    return result;
}

const rotateScene = (scene, angles={x: 0, y: 90, z:0}) =>{
    scene.rotation.set(angles.x, angles.y, angles.z);
}

const addEventClickMash = (mesh, render, size, callback) => {
    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();

    render.renderer.domElement.addEventListener('click', (event) => {
        const rect = render.renderer.domElement.getBoundingClientRect();
        mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
        mouse.y = - ((event.clientY - rect.top) / rect.height) * 2 + 1;

        raycaster.setFromCamera(mouse, render.camera);
        const intersects = raycaster.intersectObjects(render.scene.children);

        if (intersects.length > 0) {
            callback(intersects[0].object);
        }
    });
}

const changeColor = (mesh, color) => {
    mesh.material.color.set(color);
}


export {createSphere, createLight, createPyramid, rotateScene, addEventClickMash, changeColor}