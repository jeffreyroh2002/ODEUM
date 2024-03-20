import React, { Component } from 'react';
import * as THREE from 'three';
import { createNoise3D } from 'simplex-noise';

class AudioVisualizerSphere extends Component {
    constructor(props) {
        super(props);

        this.state = {
            audio: new Audio(this.props.src),
        };

        this.noise3D = createNoise3D(); // Create a noise3D function instance
        this.canvasRef = React.createRef();

        // Bind functions to the class instance
        this.fractionate = this.fractionate.bind(this);
        this.modulate = this.modulate.bind(this);
        this.avg = this.avg.bind(this);
        this.max = this.max.bind(this);
    }

    componentDidMount() {
        this.setupAudioVisualizer();
    }

    componentWillUnmount() {
        // Cleanup code if necessary
    }

    setupAudioVisualizer() {
        const canvas = this.canvasRef.current;
        const audio = this.state.audio;
        const { max, avg, modulate, noise3D } = this; // Destructuring the functions from the class

        const context = new AudioContext();
        const src = context.createMediaElementSource(audio);
        const analyser = context.createAnalyser();
        src.connect(analyser);
        analyser.connect(context.destination);
        analyser.fftSize = 512;
        const bufferLength = analyser.frequencyBinCount;
        const dataArray = new Uint8Array(bufferLength);

        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.z = 100;
        scene.add(camera);

        const renderer = new THREE.WebGLRenderer({ antialias: true, canvas });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setClearColor("#ffffff");

        const geometry = new THREE.IcosahedronGeometry(20, 3);
        const material = new THREE.MeshLambertMaterial({
            color: "#696969",
            wireframe: true
        });
        const sphere = new THREE.Mesh(geometry, material);

        const light = new THREE.DirectionalLight("#ffffff", 0.8);
        light.position.set(0, 50, 100);
        scene.add(light);
        scene.add(sphere);

        window.addEventListener('resize', () => {
            renderer.setSize(window.innerWidth, window.innerHeight);
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
        });

        function render() {
            analyser.getByteFrequencyData(dataArray);

            const lowerHalf = dataArray.slice(0, bufferLength / 2 - 1);
            const upperHalf = dataArray.slice(bufferLength / 2 - 1, bufferLength - 1);

            const lowerMax = max(lowerHalf);
            const upperAvg = avg(upperHalf);

            const lowerMaxFr = lowerMax / lowerHalf.length;
            const upperAvgFr = upperAvg / upperHalf.length;

            sphere.rotation.x += 0.001;
            sphere.rotation.y += 0.003;
            sphere.rotation.z += 0.005;

            WarpSphere(sphere, modulate(Math.pow(lowerMaxFr, 0.8), 0, 1, 0, 8), modulate(upperAvgFr, 0, 1, 0, 4));

            requestAnimationFrame(render);
            renderer.render(scene, camera);
        }

        function WarpSphere(mesh, bassFr, treFr) {
            // Check if mesh.geometry is defined
            if (mesh.geometry) {
              // Check if mesh.geometry.vertices is defined
              if (mesh.geometry.vertices) {
                mesh.geometry.vertices.forEach(function (vertex, i) {
                  const offset = mesh.geometry.parameters.radius;
                  const amp = 5;
                  const time = window.performance.now();
                  const rf = 0.00001;
                  const distance = (offset + bassFr) + noise.noise3D(vertex.x + time * rf * 4, vertex.y + time * rf * 6, vertex.z + time * rf * 7) * amp * treFr * 2;
                  vertex.multiplyScalar(distance);
                });
                mesh.geometry.verticesNeedUpdate = true;
                mesh.geometry.normalsNeedUpdate = true;
                mesh.geometry.computeVertexNormals();
                mesh.geometry.computeFaceNormals();
              } else {
                console.error("mesh.geometry.vertices is undefined");
              }
            } else {
              console.error("mesh.geometry is undefined");
            }
          }

        render();
    }

    fractionate(val, minVal, maxVal) {
        return (val - minVal) / (maxVal - minVal);
    }

    modulate(val, minVal, maxVal, outMin, outMax) {
        const fr = this.fractionate(val, minVal, maxVal);
        const delta = outMax - outMin;
        return outMin + (fr * delta);
    }

    avg(arr) {
        const total = arr.reduce((sum, b) => sum + b);
        return total / arr.length;
    }

    max(arr) {
        return arr.reduce((a, b) => Math.max(a, b));
    }

    render() {
        return (
            <canvas ref={this.canvasRef}></canvas>
        );
    }
}

export default AudioVisualizerSphere;
