package cmd

import (
	"os"

	"github.com/spf13/cobra"
)

var rootCmd = &cobra.Command{
	Use: "ndcli",
	Long: `A CLI for interacting with the Navidrome/Subsonic API.
Source code: https://github.com/iiPythonx/ndcli`,
}

func Execute() {
	err := rootCmd.Execute()
	if err != nil {
		os.Exit(1)
	}
}
