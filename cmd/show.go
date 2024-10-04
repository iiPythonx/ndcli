package cmd

import (
	"fmt"
	"strings"

	"github.com/fatih/color"
	"github.com/iipythonx/ndcli/api"
	"github.com/iipythonx/ndcli/config"
	"github.com/spf13/cobra"
)

func showItem(item api.NavidromeItem) {
	switch v := item.(type) {
	case api.Artist:
		fmt.Printf("Artist: %s\n", v.Name)
	case api.Album:
		fmt.Printf("Album: %s\n", v.Name)
	case api.Track:
		fmt.Printf("Track: %s\n", v.Name)
	}
}

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
		query := strings.ToLower(strings.TrimSpace(strings.Join(args, " ")))
		response := nd.Search(
			query,
			4,
			4,
			4,
		)

		// I'm not sure how I feel about this
		var results []api.NavidromeItem
		for _, artist := range response.Artists {
			results = append(results, artist)
		}
		for _, album := range response.Albums {
			results = append(results, album)
		}
		for _, track := range response.Tracks {
			results = append(results, track)
		}

		// Check for a direct match
		for _, item := range results {
			if strings.ToLower(item.GetName()) == query {
				showItem(item)
				return
			}
		}

		// Setup paginator
		pageItems := []PageItem{}
		for _, item := range results {
			pageItems = append(pageItems, PageItem{
				ItemData: item,
				ItemText: item.GetName(),
			})
		}
		CreatePaginator(pageItems, 10)

		// _, key, err := keyboard.GetSingleKey()
		// if err != nil {
		// 	return
		// }
		// fmt.Println(key)
	},
}

func init() {
	rootCmd.AddCommand(showCmd)
}
