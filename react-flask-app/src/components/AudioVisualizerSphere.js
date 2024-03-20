import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';

const AudioVisualizerSphere = ({ src }) => {
  const mountRef = useRef(null);
  const audioRef = useRef(new Audio(src));
  const playingRef = useRef(false);

  useEffect(() => {
    // Update src when changed
    audioRef.current.src = src;
  }, [src]);

  useEffect(() => {
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight);
    mountRef.current.appendChild(renderer.domElement);

    // Sphere
    const geometry = new THREE.SphereGeometry(3, 32, 32);
    const material = new THREE.MeshBasicMaterial({ color: 0xffffff, wireframe: true });
    const sphere = new THREE.Mesh(geometry, material);
    scene.add(sphere);

    camera.position.z = 15;

    const animate = () => {
      requestAnimationFrame(animate);
      sphere.rotation.x += 0.001;
      sphere.rotation.y += 0.001;
      renderer.render(scene, camera);
    };
    animate();

    // Event listener for click to toggle audio play/pause
    const togglePlayPause = () => {
      if (playingRef.current) {
        audioRef.current.pause();
      } else {
        audioRef.current.play();
      }
      playingRef.current = !playingRef.current;
    };

    renderer.domElement.addEventListener('click', togglePlayPause);

    // Clean up
    return () => {
      mountRef.current.removeChild(renderer.domElement);
      renderer.domElement.removeEventListener('click', togglePlayPause);
      audioRef.current.pause(); // Ensure audio is stopped
    };
  }, [src]); // Rerender only if the src prop changes

  return <div ref={mountRef} />;
};

export default AudioVisualizerSphere;
