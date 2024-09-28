package main

import (
	"fmt"

	"github.com/iipythonx/ndcli/api"
)

func main() {
	nd := api.Initialize("https://navidrome.obrien.lan", api.Credentials{NavidromeUser: "iiPython"})
	fmt.Println(nd.Login("iiPython", "lmao i would never upload my password to github"))
}
