let addMarkerMode = false;
let deleteMarkerMode = false;
let editMarkerMode = false;


    function requireLogin(event) {
        if (!isAuthenticated) {
            event.preventDefault();
            alert("You must be logged in to perform this action.");
            // window.location.href = loginUrl;
            return false;
        }
        return true;
    }

function enableAddMarkerMode(event) {
  if(requireLogin(event)){
    try{
      event.preventDefault();
      addMarkerMode = true;
      console.log("Add marker mode enabled. Click on the map to place a marker.");
    }
    catch{
       console.error("Failed to enable Add Marker Mode:", error)
    }
  }
  else{
    console.error("login to add");
  }
  }
function enableDeleteMarkerMode(event){
  if(requireLogin(event)){
    try{
  event.preventDefault();
  deleteMarkerMode = true;
  console.log("Delete marker mode enabled");
   }
    catch{
       console.error("Failed to enable Add Marker Mode:", error)
    }
  }
  else{
    console.error("login to add");
  }
}
function enableEditMarkerMode(event){
  if(requireLogin(event)){
    try{
  event.preventDefault();
  editMarkerMode = true;
  console.log("Edit marker mode enabled");
   }
    catch{
       console.error("Failed to enable Add Marker Mode:", error)
    }
  }
  else{
    console.error("login to add");
  }
}