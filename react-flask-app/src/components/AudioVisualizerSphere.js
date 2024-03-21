import React from 'react';
import * as THREE from 'three';
import song from './Aimyon.wav';

class AudioVisualizerSphere extends React.Component {
  componentDidMount() {
    this.scene = new THREE.Scene();
    this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    this.renderer = new THREE.WebGLRenderer();
    this.renderer.setSize(window.innerWidth, window.innerHeight);
    this.mount.appendChild(this.renderer.domElement);
    
    // Camera setup
    this.camera.position.z = 5;
    
    // Audio setup
    const listener = new THREE.AudioListener();
    this.camera.add(listener);
    const sound = new THREE.Audio(listener);
    const audioLoader = new THREE.AudioLoader();
    audioLoader.load(song, buffer => {
      sound.setBuffer(buffer);
      sound.setLoop(true);
      sound.setVolume(0.5);
    });
    this.sound = sound;
    this.analyser = new THREE.AudioAnalyser(sound, 32);

    // Sphere setup
    this.createVisualizer();

    // Animation loop
    this.animate();

    // Event listeners
    window.addEventListener('resize', this.onWindowResize, false);
    this.mount.addEventListener('click', this.onClick, false);
  }

  createVisualizer = () => {
    const geometry = new THREE.SphereGeometry(1, 32, 32);
    const material = new THREE.MeshBasicMaterial({ color: 0xffffff, wireframe: true });
    this.sphere = new THREE.Mesh(geometry, material);
    this.scene.add(this.sphere);
  };

  animate = () => {
    requestAnimationFrame(this.animate);
    this.renderer.render(this.scene, this.camera);

    if (this.analyser) {
      const data = this.analyser.getAverageFrequency();
      // Use the frequency data to modify the sphere (e.g., scale, color)
      const scale = Math.max(1, data / 80); // Increase divisor for less sensitivity
      this.sphere.scale.set(scale, scale, scale);
    }
  };

  onClick = () => {
    if (this.sound.isPlaying) {
      this.sound.pause();
    } else {
      // Check if context needs to be resumed (it might be suspended on first user interaction)
      if (this.sound.context.state === 'suspended') {
        this.sound.context.resume().then(() => {
          this.sound.play();
        });
      } else {
        this.sound.play();
      }
    }
  };

  onWindowResize = () => {
    this.camera.aspect = window.innerWidth / window.innerHeight;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(window.innerWidth, window.innerHeight);
  };

  componentWillUnmount() {
    window.removeEventListener('resize', this.onWindowResize);
    this.mount.removeEventListener('click', this.onClick);
    if (this.sound.isPlaying) {
      this.sound.stop();
    }
    this.mount.removeChild(this.renderer.domElement);
  }

  render() {
    return <div ref={ref => (this.mount = ref)} style={{ width: '100%', height: '100%' }}></div>;
  }
}

export default AudioVisualizerSphere;
