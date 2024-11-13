const startupValue = parseInt(localStorage.getItem('value'));
const startupID = localStorage.getItem('id');

var recent = [];
const whileMargin = 50; 
const probabilityLimit = 20; 

function newSong() {

    specificSong = false;

    artistName = ''; 
    searchType = '';
    limit = 20; 
    endpoint = '';

    data = [];
    index = -1; 

    switch(startupValue) {
        case 1: // By Artist (Name)
            console.log("YA PICKED ARTIST BY NAME")
            getTracks('artist', startupID)

            break; 
        case 2: // By Artist (ID)
            console.log("YA PICKED ARTIST BY ID")


            break; 
        case 3: //By Playlist
            console.log("YA PICKED PLAYLIST")


            break; 
        case 4: //By Album 
            console.log("YA PICKED ALBUM")

            break; 
        case 5: //Specific song
            console.log("YA PICKED SONG")
            fetchTrackDetails(startupID);

            break; 
        case 6: //My top 50 songs
            console.log("YA PICKED TOP 50 SONGS")

            break; 
        case 7: //My liked songs
            console.log("YA PICKED LIKED SONGS")

            break; 
        default: 
            break; 
    }
}

newSong();

function getTracks(contentType, query) {
    const url = `/get_tracks/${contentType}/${encodeURIComponent(query)}/`;
    console.log('GETTING TRACKS');

    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.tracks) {
                const tracks = data.tracks;

                const lastItems = recent.length > probabilityLimit ? recent.slice(-probabilityLimit) : recent;
                let k = 0;
                let selectedTrack = null;

                do {
                    const index = Math.floor(Math.random() * tracks.length);
                    selectedTrack = tracks[index];
                    k++;

                } while (lastItems.some(item => item.title === selectedTrack.title) && k < whileMargin);

                if (selectedTrack) {
                    fetchTrackDetails(selectedTrack.uri.split(':')[2]);
                    // Add the selected track to the recent list
                    recent.push({
                        title: selectedTrack.title,
                        artist: selectedTrack.artist,
                        trackId: selectedTrack.uri.split(':')[2]
                    });
                    console.log('track uri: ' + selectedTrack.uri)
                    console.log('track id: ' + selectedTrack.uri)
                }else {
                    console.log("No valid track selected after multiple attempts.");
                }
            } else if (data.error) {
                console.error('Error:', data.error);
            }
        })
        .catch(error => {
            console.error('Request failed', error);
        });
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

                const song = responseData.song;

                localStorage.setItem('uri', responseData.uri);
                localStorage.setItem('song', song);
                localStorage.setItem('duration', responseData.duration);
            })
            .catch(error => console.error(error));
}