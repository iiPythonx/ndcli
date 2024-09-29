package api

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
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

func (nd Navidrome) Request(method string, endpoint string, payload io.Reader) (*http.Response, error) {
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
	// defer resp.Body.Close()
	// body, _ := io.ReadAll(resp.Body)
	// return body, nil
}

func Initialize(server string, creds Credentials) *Navidrome {
	return &Navidrome{server: server, client: &http.Client{}, credentials: creds}
}
