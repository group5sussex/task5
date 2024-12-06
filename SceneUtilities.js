import * as THREE from 'three';

export class SceneUtilities {
    static rotateScene(scene, angles={x: 0, y: 90, z:0}) {
        scene.rotation.set(angles.x, angles.y, angles.z);
    }

    static changeColor(mesh, color) {
        mesh.material.color.set(color);
    }
}