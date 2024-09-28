package api

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
)

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
	return string(response) == "."
}

func (nd Navidrome) Login(username string, password string) (bool, *Credentials) {
	payload, err := json.Marshal(map[string]interface{}{
		"username": username,
		"password": password,
	})
	if err != nil {
		return false, &nd.credentials
	}

	var credentials Credentials
	nd.JsonRequest("POST", "auth/login", payload, &credentials)
	return true, &credentials
}

func (nd Navidrome) JsonRequest(method string, endpoint string, payload []byte, model interface{}) {
	response, _ := nd.Request(method, endpoint, bytes.NewBuffer(payload))
	json.Unmarshal(response, &model)
}

func (nd Navidrome) Request(method string, endpoint string, payload io.Reader) ([]byte, error) {
	req, err := http.NewRequest(method, fmt.Sprintf("%s/%s", nd.server, endpoint), payload)
	if err != nil {
		return nil, err
	}
	req.Header.Add("X-Nd-Authorization", fmt.Sprintf("Bearer: %s", nd.credentials.NavidromeToken))
	resp, err := nd.client.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()
	body, _ := io.ReadAll(resp.Body)
	return body, nil
}

func Initialize(server string, creds Credentials) *Navidrome {
	return &Navidrome{server: server, client: &http.Client{}, credentials: creds}
}
