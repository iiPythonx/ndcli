package cmd

import (
	"fmt"
	"strings"

	"github.com/fatih/color"
	"github.com/iipythonx/ndcli/api"
	"github.com/iipythonx/ndcli/config"
	"github.com/spf13/cobra"
)

var showCmd = &cobra.Command{
	Use:   "show",
	Short: "Search and show any Navidrome item.",
	Run: func(cmd *cobra.Command, args []string) {
		config := config.ReadConfiguration()
		if config.Server == "" {
			color.Red("You are not logged into Navidrome.")
			return
		}
		nd := api.Initialize(config.Server, config.Credentials)

		// Perform a search
		fmt.Println(nd.Search(
			strings.ToLower(strings.TrimSpace(strings.Join(args, " "))),
			4,
			4,
			4,
		))
	},
}

func init() {
	rootCmd.AddCommand(showCmd)
}
