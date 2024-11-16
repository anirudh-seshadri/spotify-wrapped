let trackReady = false;
let device_id;
let player;
let accessToken;
// let tries = parseInt(localStorage.getItem('playCount')) || 0;

window.onSpotifyWebPlaybackSDKReady = () => {

    // Use the getAccessToken function to retrieve the access token asynchronously
    getAccessToken().then(token => {
        if (token) {
            accessToken = token;
            console.log('Access Token: ' + accessToken);

            // Initialize the Spotify player once the access token is obtained
            player = new Spotify.Player({
                name: 'Web Playback SDK Quick Start Player',
                getOAuthToken: cb => { cb(accessToken); },  // Use the access token
                volume: 0.5
            });

            // Ready
            player.addListener('ready', ({ device_id: readyDeviceId }) => {
                device_id = readyDeviceId;
                console.log('Ready with Device ID', device_id);
            });

            // Not Ready
            player.addListener('not_ready', ({ device_id }) => {
                console.log('Device ID has gone offline', device_id);
            });

            player.addListener('initialization_error', ({ message }) => {
                console.log('INITIALIZATION');
                console.error(message);
            });

            player.addListener('authentication_error', ({ message }) => {
                console.log('AUTHENTICATION');   
                console.error(message);
            });

            player.addListener('account_error', ({ message }) => {
                console.log('ACCOUNT ERROR');
                console.error(message);
            });

            player.connect();  // Connect to the player once it's ready
        } else {
            console.error('No access token found.');
        }
    }).catch(error => {
        console.error('Error retrieving access token:', error);
    });
};

const playClip = async () => {
    try {
        if (!device_id) {
            console.error('Device ID not available');
            return;
        }

        const trackUri = localStorage.getItem('trackUri');
        console.log('trackURi: ' + trackUri);

        // Start playback at the beginning of the track
        await fetch(`https://api.spotify.com/v1/me/player/play?device_id=${device_id}`, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${accessToken}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ uris: [trackUri] })
        });

        const duration = (parseInt(localStorage.getItem('tries')) + 1) * 1000;
        console.log(`Playing for ${duration / 1000} seconds`);

        setTimeout(async () => {
            await player.pause();
            console.log(`Paused after ${duration / 1000} seconds`);
        }, duration); 
    } catch (error) {
        console.error('Error playing the track:', error);
    }
};

document.getElementById('play').onclick = function() {
    console.log('PLAYING');
    playClip();
};

document.getElementById('addSecond').onclick = function() {
    console.log('Adding a second!!');
    let currentValue = parseInt(localStorage.getItem('tries')) || 0;
    currentValue++;
    localStorage.setItem('tries', currentValue);
};

document.getElementById('submit').onclick = function() {
    submit();
};

document.getElementById('guess').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault();  
        submit();
    }
});

function submit(){
    if(document.getElementById('guess').value.replace(/\W/g, '').toLowerCase() === localStorage.getItem('songName').replace(/\W/g, '').toLowerCase()){
        alert("YOU DID IT! I'm so proud of you :)");
    }else{
        let currentValue = parseInt(localStorage.getItem('tries')) || 0;
        currentValue++;
        localStorage.setItem('tries', currentValue);
        alert('WRONG :(');
    }
    document.getElementById('guess').value = '';
}

async function getAccessToken() {
    try {
        const response = await fetch('/get_access_token/');
        
        if (response.ok) {
            const data = await response.json();
            return data.access_token;  // Return the access token from the response
        } else {
            console.error('Failed to retrieve access token:', response.statusText);
            return null;
        }
    } catch (error) {
        console.error('Error fetching access token:', error);
        return null;
    }
}