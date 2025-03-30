const coordinatesElement = document.getElementById('coordinates');
let coords;

// Below is a fix for mobile viewport thing, I cant be bothered with it yet
//const setHeight = () => {
//    document.getElementById("full-body").style.minHeight = window.innerHeight + "px"
//};

fetch('https://api.swider.dev')
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => updateNumbers(data[0].split(' ')[0],data[0].split(' ')[1] ))
  .catch(error => console.error('Fetch error:', error));


// Create EventSource for SSE endpoint
const eventSource = new EventSource('https://api.swider.dev/get-numbers');

eventSource.onopen = () => {
    console.log('EventSource connected')
    //Everytime the connection gets extablished clearing the previous data from UI
    tagOnline();
}

//In case of any error, if eventSource is not closed explicitely then client will retry the connection a new call to backend will happen and the cycle will go on.
eventSource.onerror = (error) => {
    console.error('EventSource failed', error)
    tagOffline();
}


function tagOffline() {
    // Your async code here
    const element = document.getElementById('statusTag');
    element.className = 'statusOffline';
    element.textContent = 'Disconnected'
}

function tagOnline() {
    // Your async code here
    const element = document.getElementById('statusTag');
    element.className = 'statusOnline';
    element.textContent = 'Connected'
}

var timeout= setTimeout(function() {
tagOffline();
}, 20000);

eventSource.addEventListener('locationUpdate', function (event) {
    clearTimeout(timeout);
        if (typeof event.data) {
    timeout= setTimeout(function() {
    tagOffline();
    }, 20000);


    coords = event.data;
    b = coords.split(' ')
    updateNumbers(b[0], b[1])
    }
});



// Function to update and display coordinates
function updateCoordinates(coordinates) {
    // Create a new paragraph element for each coordinate and append it
    const paragraph = document.createElement('p');
    paragraph.textContent = `Latitude: ${coordinates.lat}, Longitude: ${coordinates.lng}`;
    coordinatesElement.appendChild(paragraph);
}
function updateNumbers(a,b){
    document.getElementById("queNum").innerHTML = a;
    document.getElementById("waitNum").innerHTML = b;
    console.log("Function triggered.")
    }

