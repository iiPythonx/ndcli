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

func (nd Navidrome) Login(username string, password string) (bool, *Credentials) {
	payload, err := json.Marshal(map[string]interface{}{
		"username": username,
		"password": password,
	})
	if err != nil {
		return false, &nd.credentials
	}

	var credentials Credentials
	nd.Request("POST", "auth/login", bytes.NewBuffer(payload), &credentials)
	return true, &credentials
}

func (nd Navidrome) Request(method string, endpoint string, payload io.Reader, model interface{}) error {
	req, err := http.NewRequest(method, fmt.Sprintf("%s/%s", nd.server, endpoint), payload)
	if err != nil {
		return err
	}
	req.Header.Add("X-Nd-Authorization", fmt.Sprintf("Bearer: %s", nd.credentials.NavidromeToken))
	resp, err := nd.client.Do(req)
	if err != nil {
		return err
	}
	json.NewDecoder(resp.Body).Decode(model)
	defer resp.Body.Close()
	return nil
}

func Initialize(server string, creds Credentials) *Navidrome {
	return &Navidrome{server: server, client: &http.Client{}, credentials: creds}
}
