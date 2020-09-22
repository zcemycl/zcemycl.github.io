var scene = new THREE.Scene();
var camera = new THREE.PerspectiveCamera(60, 1, 1, 1000);
camera.position.set(0, 0, 500);
var renderer = new THREE.WebGLRenderer({
  antialias: true
});
renderer.setClearColor(0x808080);
var canvas = renderer.domElement
document.body.appendChild(canvas);

var controls = new THREE.OrbitControls(camera, renderer.domElement);

var light = new THREE.HemisphereLight( 0xffffbb, 0x080820, 1 );
scene.add( light );

var loader = new THREE.GLTFLoader();

loader.load( './scene.gltf', function ( gltf ) {
  console.log(gltf);
  gltf.scene.position.z = -5;
  scene.add( gltf.scene );

}, undefined, function ( error ) {

  console.error( error );

} );




render();

function render() {
  if (resize(renderer)) {
    camera.aspect = canvas.clientWidth / canvas.clientHeight;
    camera.updateProjectionMatrix();
  }
  renderer.render(scene, camera);
  requestAnimationFrame(render);
}

function resize(renderer) {
  const canvas = renderer.domElement;
  const width = canvas.clientWidth;
  const height = canvas.clientHeight;
  const needResize = canvas.width !== width || canvas.height !== height;
  if (needResize) {
    renderer.setSize(width, height, false);
  }
  return needResize;
}
