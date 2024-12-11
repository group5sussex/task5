import * as THREE from 'three';

export class Sphere{
    static create(radius, color, widthS = 16, heightS = 32) {
        const geometry = new THREE.SphereGeometry(radius, widthS, heightS);
        const material = new THREE.MeshStandardMaterial({color: color});
        return new THREE.Mesh(geometry, material);
    }
}