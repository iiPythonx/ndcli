package config

import (
	"encoding/json"
	"os"
	"path/filepath"

	"github.com/iipythonx/ndcli/api"
)

type Configuration struct {
	Credentials api.Credentials
	Server      string
}

func GetConfigFile() string {
	homeDirectory, _ := os.UserHomeDir()
	configFile := filepath.Join(homeDirectory, ".config", "ndcli", "config.json")
	return configFile
}

func DoesConfigExist() bool {
	_, err := os.Stat(GetConfigFile())
	return err == nil
}

func ReadConfiguration() Configuration {
	if !DoesConfigExist() {
		return Configuration{}
	}

	// JSON decode the file
	data, _ := os.ReadFile(GetConfigFile())
	var credentials Configuration
	json.Unmarshal(data, &credentials)
	return credentials
}

func WriteConfiguration(config Configuration) {
	data, _ := json.Marshal(config)
	os.WriteFile(GetConfigFile(), data, 0644)
}
