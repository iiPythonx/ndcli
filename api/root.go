package api

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/url"
)

type ErrorResponse struct {
	Message string `json:"error"`
}

type Credentials struct {
	NavidromeUser  string `json:"username"`
	NavidromeToken string `json:"token"`
	SubsonicSalt   string `json:"subsonicSalt"`
	SubsonicToken  string `json:"subsonicToken"`
}

type Navidrome struct {
	server      string
	client      *http.Client
	credentials Credentials
}

func (nd Navidrome) Ping() bool {
	response, _ := nd.Request("GET", "ping", nil)
	body, _ := io.ReadAll(response.Body)
	return string(body) == "."
}

func (nd Navidrome) Login(username string, password string) (*ErrorResponse, *Credentials) {
	payload, err := json.Marshal(map[string]interface{}{
		"username": username,
		"password": password,
	})
	if err != nil {
		return &ErrorResponse{Message: "Failed to encode credentials"}, &nd.credentials
	}
	var (
		credentials   Credentials
		error_details ErrorResponse
	)
	nd.JsonRequest("POST", "auth/login", payload, &credentials, &error_details)
	return &error_details, &credentials
}

func (nd Navidrome) JsonRequest(method string, endpoint string, payload []byte, successModel interface{}, failureModel interface{}) {
	response, _ := nd.Request(method, endpoint, bytes.NewBuffer(payload))
	decoder := json.NewDecoder(response.Body)
	if response.StatusCode == 200 {
		decoder.Decode(&successModel)
		return
	}
	decoder.Decode(&failureModel)
}

func (nd Navidrome) JsonRequestSubsonic(method string, endpoint string, params url.Values, model interface{}) {
	credentials := url.Values{
		"c": {"ndcli"},
		"f": {"json"},
		"v": {"no idea"},
		"u": {nd.credentials.NavidromeUser},
		"s": {nd.credentials.SubsonicSalt},
		"t": {nd.credentials.SubsonicToken},
	}
	for param, value := range credentials {
		params[param] = append(params[param], value...)
	}

	response, _ := nd.Request(method, fmt.Sprintf("rest/%s?%s", endpoint, params.Encode()), nil)
	json.NewDecoder(response.Body).Decode(&model)
}

func (nd Navidrome) Request(method string, endpoint string, payload io.Reader) (*http.Response, error) {
	fmt.Printf("[Request] %s/%s\n", nd.server, endpoint)
	req, err := http.NewRequest(method, fmt.Sprintf("%s/%s", nd.server, endpoint), payload)
	if err != nil {
		return nil, err
	}
	req.Header.Add("X-Nd-Authorization", fmt.Sprintf("Bearer: %s", nd.credentials.NavidromeToken))
	resp, err := nd.client.Do(req)
	if err != nil {
		return nil, err
	}
	return resp, nil
}

func Initialize(server string, creds Credentials) *Navidrome {
	return &Navidrome{server: server, client: &http.Client{}, credentials: creds}
}

// API Requests
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

func (nd Navidrome) Search(query string, album_count int, artist_count int, song_count int) SearchResults {
	var results GenericResponse
	nd.JsonRequestSubsonic("GET", "search3.view", url.Values{
		"query":        {query},
		"albumCount":   {string(album_count)},
		"albumOffset":  {"0"},
		"artist_count": {string(artist_count)},
		"artistOffset": {"0"},
		"song_count":   {string(song_count)},
		"songOffset":   {"0"},
	}, &results)
	return results.Response.SearchResult3
}
