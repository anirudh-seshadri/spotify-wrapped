const startupValue = parseInt(localStorage.getItem('value'));
const startupID = localStorage.getItem('id');

let songName;
let artistName;

var selectedTrack = {};
var recent = [];
const whileMargin = 50; 
const probabilityLimit = 20; 

let trackReady = false;
let device_id;
let player;
let accessToken;
let tries = 0;

function newSong() {
    trackReady = false;
    document.getElementById('loading').classList.remove('hidden');

    switch(startupValue) {
        case 1: // By Artist (Name)
            console.log("YA PICKED ARTIST BY NAME")
            getTracks('artist', startupID)
            break; 

        case 2: // By Artist (ID)
            console.log("YA PICKED ARTIST BY ID")
            getTracks('artistID', startupID)
            break; 

        case 3: //By Playlist (Name)
            console.log("YA PICKED PLAYLIST BY NAME")
            getTracks('playlist', startupID)
            break; 

        case 4: //By Playlist (ID)
            console.log("YA PICKED PLAYLIST BY ID")
            getTracks('playlistID', startupID)
            break; 

        case 5: //By Album (name)
            console.log("YA PICKED ALBUM BY NAME")
            getTracks('album', startupID)
            break; 

        case 6: //By Album (ID)
            console.log("YA PICKED ALBUM BY ID")
            getTracks('albumID', startupID)
            break; 

        case 7: //Specific song
            console.log("YA PICKED SONG")
            fetchTrackDetails(startupID);

            break; 
        case 8: //My top 50 songs
            console.log("YA PICKED TOP 50 SONGS")
            getTracks('top50', 'placeholder')

            break; 
        case 9: //My liked songs
            console.log("YA PICKED LIKED SONGS")
            getTracks('liked', 'placeholder')

            break; 
        default: 
            break; 
    }
}

newSong();

async function getTracks(contentType, query) {
    const url = `/get_tracks/${contentType}/${encodeURIComponent(query)}/`;
    console.log('GETTING TRACKS');

    try {
        const response = await fetch(url);
        const data = await response.json();

        if (data.tracks) {
            const tracks = data.tracks;
            console.table(tracks, ["title", "artist", "uri", "duration"]); // Display tracks in a table format

            const lastItems = recent.length > probabilityLimit ? recent.slice(-probabilityLimit) : recent;
            let k = 0;

            do {
                const index = Math.floor(Math.random() * tracks.length);
                selectedTrack = tracks[index];
                k++;

            } while (lastItems.some(item => item.title.split(' - ')[0] === selectedTrack.title.split(' - ')[0]) && k < whileMargin);

            if (k == whileMargin){
                console.log('NO MORE UNIQUE SONGS! REPEATING RECENTS')
            }

            if (selectedTrack) {
                fetchTrackDetails(selectedTrack.uri.split(':')[2]);

                // Add the selected track to the recent list
                recent.push({
                    title: selectedTrack.title,
                    artist: selectedTrack.artist,
                    trackId: selectedTrack.uri.split(':')[2]
                });
            }else {
                console.log("No valid track selected after multiple attempts.");
            }
        } else if (data.error) {
            console.error('Error:', data.error);
        }
    }catch(error){
        console.error('Request failed', error);
    }
        
}

function fetchTrackDetails(trackID) {
    console.log('FETCHING SPECIFIC TRACK!!')
    const endpoint = `/get-spotify-track/${trackID}/`;


    fetch(endpoint)
    .then(response => response.json())
    .then(responseData => {
        if (responseData.error) {
            console.error(responseData.error);
            return;
        }

        selectedTrack = responseData;

        localStorage.setItem('trackUri', selectedTrack.uri);
        localStorage.setItem('songName', selectedTrack.song.split(' - ')[0]);
        localStorage.setItem('artistName', selectedTrack.song.split(' - ')[selectedTrack.song.split(' - ').length - 1]);
        localStorage.setItem('duration', selectedTrack.duration);
        tries = 0;

        songName = localStorage.getItem('songName');
        artistName = localStorage.getItem('artistName');

        // console.log('selectedTrack:', JSON.stringify(selectedTrack, null, 2));
        console.log('RECENTS', recent);
        trackReady = true;
        document.getElementById('loading').classList.add('hidden');

    })
    .catch(error => console.error(error));
}

document.getElementById('newSong').onclick = function() {
    console.log('PLAYING NEW SONG!!');

    closeNotification();
    newSong()
};

document.getElementById('skipSong').onclick = function() {
    if(!trackReady){
        console.log("YOU DIDN'T LISTEN TO THE SONG YET!!");
        return;
    }
    console.log('SKIPPING SONG!!');
    showNotification(`Skipped the song :( The song was ${songName} by ${artistName}. Better luck next time!`);

    const closeButton = document.getElementById('close-btn');
    closeButton.removeEventListener('click', closeNotification);
    closeButton.addEventListener('click', closeNotification);
};

window.onSpotifyWebPlaybackSDKReady = () => {
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
            player.connect();  
        } else {
            console.error('No access token found.');
        }
    }).catch(error => {
        console.error('Error retrieving access token:', error);
    });
};

async function playClip() {
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


        const duration = (tries + 1) * 1000;
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
    if(!trackReady){
        console.log('HOLD YOUR FRCKAKSJ HORSES!');
        return;
    }
    console.log('PLAYING');
    playClip();
};

document.getElementById('addSecond').onclick = function() {
    console.log('Adding a second!!');
    showShortNotification('SKIPPED! Adding another second...');
    tries++;
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
    let correctGuess = '';
    let noPar = '';

    if (songName) {
        if (/\(.*\)/.test(songName)) {
            noPar = songName.replace(/\s*\([^()]*\)$/, '').replace(/[^\w&]/g, '').toLowerCase();
        } 
        correctGuess = songName.replace(/[^\w&]/g, '').toLowerCase();
    }
    if (document.getElementById('guess').value === ''){
        showShortNotification('You have to type a guess!!');
    }else if (
        document.getElementById('guess').value.replace(/[^\w&]/g, '').toLowerCase() === correctGuess || 
        document.getElementById('guess').value.replace(/[^\w&]/g, '').toLowerCase() === noPar
    ) {
        showNotification(`YOU DID IT! I'm so proud of you :) The song was ${songName} by ${artistName}`);
    }else{
        tries++;
        showShortNotification('WRONG :( Adding another second...');
    }
    document.getElementById('guess').value = '';
}

function showShortNotification(message) {
    const notification = document.getElementById('notification');
    const messageElement = document.getElementById('notification-message');
    messageElement.textContent = message;
    notification.classList.remove('hidden');
    
    const closeButton = document.getElementById('close-btn');
    const newButton = document.getElementById('newSong');
    closeButton.style.display = 'none';
    newButton.style.display = 'none';
    
    setTimeout(() => {
        notification.classList.add('hidden');
    }, 3000);
}

function showNotification(message) {
    const notification = document.getElementById('notification');
    const messageElement = document.getElementById('notification-message');
    messageElement.textContent = message;
    notification.classList.remove('hidden');
    
    const closeButton = document.getElementById('close-btn');
    const newButton = document.getElementById('newSong');

    closeButton.style.display = 'inline-block';
    newButton.style.display = 'inline-block';
}

function closeNotification() {
    const notification = document.getElementById('notification');
    notification.classList.add('hidden');
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