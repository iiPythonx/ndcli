package cmd

import (
	"bufio"
	"fmt"
	"os"

	"github.com/fatih/color"
	"github.com/iipythonx/ndcli/api"
	"github.com/spf13/cobra"
)

func Input(fgcolor color.Attribute, prompt string) string {
	reader := bufio.NewScanner(os.Stdin)
	color.New(fgcolor).Printf(prompt)
	reader.Scan()
	return reader.Text()
}

var loginCmd = &cobra.Command{
	Use:   "login",
	Short: "Authenticate with Navidrome.",
	Run: func(cmd *cobra.Command, args []string) {
		server := Input(color.FgCyan, "Navidrome URL: ")
		nd := api.Initialize(server, api.Credentials{})
		if !nd.Ping() {
			color.Red("Connection to specified server failed, check your URL.")
			return
		}
		fmt.Println(nd.Ping())
	},
}

func init() {
	rootCmd.AddCommand(loginCmd)
}
