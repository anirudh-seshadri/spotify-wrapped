const startupValue = parseInt(localStorage.getItem('value'));
const startupID = localStorage.getItem('id');

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