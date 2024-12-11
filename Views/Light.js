import * as THREE from 'three';

export class Light {
    static create(pos = {x:100, y:100, z:100}, color, intensity) {
        const light = new THREE.DirectionalLight(color, intensity);
        light.position.set(pos.x, pos.y, pos.z).normalize();
        return light;
    }
}