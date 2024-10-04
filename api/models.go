package api

type NavidromeItem interface {
	GetName() string
}

type Artist struct {
	PlayCount  int    `json:"playCount"`
	PlayDate   string `json:"playDate"`
	Rating     int    `json:"rating"`
	Starred    bool   `json:"starred"`
	StarredAt  string `json:"starredAt"`
	ID         string `json:"id"`
	Name       string `json:"name"`
	AlbumCount int    `json:"albumCount"`
	SongCount  int    `json:"songCount"`
	Size       int    `json:"size"`
}

type Album struct {
	PlayCount    int    `json:"playCount"`
	PlayDate     string `json:"playDate"`
	Rating       int    `json:"rating"`
	StarredAt    string `json:"starredAt"`
	ID           string `json:"id"`
	Name         string `json:"name"`
	Artist       string `json:"artist"`
	AlbumArtist  string `json:"albumArtist"`
	Date         string `json:"date"`
	OriginalDate string `json:"originalDate"`
	ReleaseDate  string `json:"releaseDate"`
	SongCount    int    `json:"songCount"`
	Duration     int    `json:"duration"`
	Size         int    `json:"size"`
	Genre        string `json:"genre"`
	Year         int    `json:"year"`
}

type Track struct {
	PlayCount    int    `json:"playCount"`
	PlayDate     string `json:"played"`
	ID           string `json:"id"`
	Name         string `json:"title"`
	Artist       string `json:"artist"`
	Album        string `json:"album"`
	TrackNumber  int    `json:"trackNumber"`
	DiscNumber   int    `json:"discNumber"`
	ContentType  string `json:"contentType"`
	BPM          int    `json:"bpm"`
	BitRate      int    `json:"bitRate"`
	Duration     int    `json:"duration"`
	Size         int    `json:"size"`
	Year         int    `json:"year"`
	ChannelCount int    `json:"channelCount"`
	SamplingRate string `json:"samplingRate"`
}

func (artist Artist) GetName() string {
	return artist.Name
}

func (album Album) GetName() string {
	return album.Name
}

func (track Track) GetName() string {
	return track.Name
}

type GenericResponse struct {
	Response SubsonicResponse `json:"subsonic-response"`
}

type SubsonicResponse struct {
	Status        string `json:"status"`
	Version       string `json:"version"`
	Type          string `json:"type"`
	ServerVersion string `json:"serverVersion"`
	OpenSubsonic  bool   `json:"openSubsonic"`

	// Responses
	SearchResult3 SearchResults `json:"searchResult3"`
}

type SearchResults struct {
	Artists []Artist `json:"artist"`
	Albums  []Album  `json:"album"`
	Tracks  []Track  `json:"song"`
}
