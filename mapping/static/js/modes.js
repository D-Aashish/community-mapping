let addMarkerMode = false;
let deleteMarkerMode = false;
let editMarkerMode = false;

// Enable modes
function enableAddMarkerMode(event) {
  event.preventDefault();
  addMarkerMode = true;
  console.log("Add marker mode enabled. Click on the map to place a marker.");
}
function enableDeleteMarkerMode(event){
  event.preventDefault();
  deleteMarkerMode = true;
  console.log("Delete marker mode enabled");
}
function enableEditMarkerMode(event){
  event.preventDefault();
  editMarkerMode = true;
  console.log("Edit marker mode enabled");
}