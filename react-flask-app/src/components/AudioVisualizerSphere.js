import React, { useRef, useEffect } from 'react';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';

const AudioVisualizerSphere = ({ src }) => {
    const containerRef = useRef(null);
    const audioRef = useRef(null);
    const scene = useRef(null);
    const camera = useRef(null);
    const renderer = useRef(null);
    const sphere = useRef(null);

    useEffect(() => {
        init();
        animate();

        return () => {
            // Clean up Three.js scene on unmount
            scene.current.children = [];
            cancelAnimationFrame(animate);
            renderer.current.dispose();
        };
    }, []);

    useEffect(() => {
        if (audioRef.current) {
            audioRef.current.src = src;
            audioRef.current.play();
        }
    }, [src]);

    const init = () => {
        // Scene
        scene.current = new THREE.Scene();

        // Camera
        camera.current = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.current.position.z = 5;

        // Renderer
        renderer.current = new THREE.WebGLRenderer({ antialias: true });
        renderer.current.setSize(window.innerWidth, window.innerHeight);
        containerRef.current.appendChild(renderer.current.domElement);

        // Sphere
        const geometry = new THREE.SphereGeometry(1, 32, 32);
        const material = new THREE.MeshBasicMaterial({ color: 0xffffff, wireframe: true });
        sphere.current = new THREE.Mesh(geometry, material);
        scene.current.add(sphere.current);

        // Audio
        audioRef.current = new Audio();
        const listener = new THREE.AudioListener();
        camera.current.add(listener);
        const audio = new THREE.Audio(listener);
        const audioLoader = new THREE.AudioLoader();
        audioLoader.load(src, buffer => {
            audio.setBuffer(buffer);
            audio.setLoop(true);
            audio.play();
        });
    };

    const animate = () => {
        requestAnimationFrame(animate);
        renderer.current.render(scene.current, camera.current);
        sphere.current.rotation.y += 0.01;
    };

    return <div ref={containerRef} />;
};

export default AudioVisualizerSphere;
