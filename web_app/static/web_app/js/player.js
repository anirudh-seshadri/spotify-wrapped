// let player;  // Declare the player variable globally so it can be accessed after initialization

// window.onSpotifyWebPlaybackSDKReady = () => {
//     const token = document.getElementById('audio-player').getAttribute('data-token');
//     console.log('poop');
//     console.log(token);

//     if (!token) {
//         console.error('No access token available!');
//         return;  // Early exit if no token is found
//     }

//     player = new Spotify.Player({
//         name: 'My Web Playback SDK Player',
//         getOAuthToken: cb => { cb(token); },
//         volume: 0.5
//     });

//     // Error handling
//     player.addListener('initialization_error', ({ message }) => { console.error(message); });
//     player.addListener('authentication_error', ({ message }) => { console.error(message); });
//     player.addListener('account_error', ({ message }) => { console.error(message); });
//     player.addListener('playback_error', ({ message }) => { console.error(message); });

//     // Playback status updates
//     player.addListener('player_state_changed', state => { console.log(state); });

//     // Ready
//     player.addListener('ready', ({ device_id }) => {
//         console.log('Ready with Device ID', device_id);
//     });

//     // Not Ready
//     player.addListener('not_ready', ({ device_id }) => {
//         console.log('Device ID has gone offline', device_id);
//     });

//     // Connect to the player!
//     player.connect();
// };

// // Add the event listener to the play button to start playing the song when clicked
// document.getElementById("play").addEventListener("click", function() {
//     if (!player) {
//         console.error("Player is not initialized yet.");
//         return;
//     }

//     // Example: Playing a specific song (replace with actual track URI you want to play)
//     const trackUri = "spotify:track:3n3PpTejTy2lGZtH60RnpP";  // Replace with the URI of the track you want to play
    
//     player.togglePlay()  // Ensure that the player starts playing
//         .then(() => {
//             return player.play({ uris: [trackUri] });  // Play the track using its URI
//         })
//         .catch(error => {
//             console.error("Error while trying to play the track:", error);
//         });
// });

// player.js
// window.onSpotifyWebPlaybackSDKReady = () => {
//     const player = new Spotify.Player({
//         name: 'Your Web Player',
//         getOAuthToken: cb => { cb(token); },
//         volume: 0.5
//     });

//     const token = document.getElementById('audio-player').getAttribute('data-token');
//     console.log('poop');
//     console.log(token);

//     player.addListener('initialization_error', ({ message }) => { console.error(message); });
//     player.addListener('authentication_error', ({ message }) => { console.error(message); });
//     player.addListener('account_error', ({ message }) => { console.error(message); });
//     player.addListener('playback_error', ({ message }) => { console.error(message); });

//     player.addListener('player_state_changed', state => {
//         console.log(state);
//     });

//     player.addListener('ready', ({ device_id }) => {
//         console.log('The Web Playback SDK is ready with Device ID', device_id);
//     });

//     player.addListener('not_ready', ({ device_id }) => {
//         console.log('The Web Playback SDK has left the device', device_id);
//     });

//     // Initialize the player
//     player.connect();
// };

// window.onSpotifyWebPlaybackSDKReady = () => {
//     const token = document.getElementById('audio-player').getAttribute('data-token');
//     console.log('poop');
//     console.log(token);
//     const player = new Spotify.Player({
//       name: 'Web Playback SDK Quick Start Player',
//       getOAuthToken: cb => { cb(token); },
//       volume: 0.5
//     });

//     // Ready
//     player.addListener('ready', ({ device_id }) => {
//       console.log('Ready with Device ID', device_id);
//     });
  
//     // Not Ready
//     player.addListener('not_ready', ({ device_id }) => {
//       console.log('Device ID has gone offline', device_id);

//       player.addListener('initialization_error', ({ message }) => {
//         console.error(message);
//     });
  
//     player.addListener('authentication_error', ({ message }) => {
//         console.error(message);
//     });
  
//     player.addListener('account_error', ({ message }) => {
//         console.error(message);
//     });
  
//     });
//     console.log('peepee')

//     player.connect();

// }  

window.onSpotifyWebPlaybackSDKReady = () => {
    // let token = document.getElementById('audio-player').getAttribute('data-token');
    // console.log('poop');
    // console.log(token);

    // token = decodeURIComponent(token);
    // console.log(token);

    // const token = 'BQAyoAXAJu652M3jK6fyo3-xzVF9hK7YDKqPRGcsG3fJHAeBhLUcIeqE6l-m3fdab-eeQtRZMJr2Qlnog60PK7gsrCJWSz2BnvmjkOTixUh9N0Mkc8F4j57O1FRdJST8STph2GWqYAn7m6YMyixzh6YDktPcUFsUbF06UOmm5Ytr_BEAjEk5BLChwgT_0tzPMziHU8W9GVDRFzDPTwtQ4Pjf8hPVJOql56Uy3RGeeoaC77oEGSWvzeCYGg'

    const token = JSON.parse(document.getElementById('access-token').textContent);
    console.log('Retrieved Token:', token);  // Optional: Check the token in the console


    const player = new Spotify.Player({
        name: 'Web Playback SDK Quick Start Player',
        getOAuthToken: cb => { cb(token); },
        volume: 0.5
    });

    // Ready
    player.addListener('ready', ({ device_id }) => {
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

    player.connect();
}


