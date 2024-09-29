package cmd

import (
	"bufio"
	"fmt"
	"os"
	"strings"

	"github.com/fatih/color"
	"github.com/iipythonx/ndcli/api"
	"github.com/spf13/cobra"
)

func Input(reader *bufio.Scanner, fgcolor color.Attribute, prompt string) string {
	color.New(fgcolor).Printf(prompt)
	reader.Scan()
	return reader.Text()
}

func EraseLine(lines int) {
	fmt.Printf("\033[%dF\033[2K", lines)
}

var loginCmd = &cobra.Command{
	Use:   "login",
	Short: "Authenticate with Navidrome.",
	Run: func(cmd *cobra.Command, args []string) {
		reader := bufio.NewScanner(os.Stdin)
		server := Input(reader, color.FgCyan, "Navidrome URL: ")
		if !strings.Contains(server, "://") {
			if !strings.Contains(server, ":") {
				server += ":4533"
			}
			server = fmt.Sprintf("http://%s", server)
		}

		nd := api.Initialize(server, api.Credentials{})
		if !nd.Ping() {
			EraseLine(1)
			color.Red("Navidrome URL: %s", server)
			color.Red("Connection to specified server failed, check your URL.")
			return
		}
		EraseLine(1)
		color.Green("Navidrome URL: %s", server)

		// Handle login credentials
		err, credentials := nd.Login(
			Input(reader, color.FgCyan, "Navidrome username: "),
			Input(reader, color.FgCyan, "Navidrome password: "),
		)
		EraseLine(2)
		if err != nil {
			color.Red("Login failed, Navidrome response: %s.", err.Message)
			return
		}
		color.Green("Logged in as %s.", credentials.NavidromeUser)
		fmt.Println(credentials)
	},
}

func init() {
	rootCmd.AddCommand(loginCmd)
}
