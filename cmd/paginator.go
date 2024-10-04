package cmd

import (
	"fmt"

	"github.com/iipythonx/ndcli/api"
)

type PageItem struct {
	ItemData api.NavidromeItem
	ItemText string
}

type PaginatorState struct {
	PageNumber int
	PageIndex  int
	Pages      [][]PageItem
	PageSize   int
}

func splitItems(items []PageItem, pageSize int) [][]PageItem {
	var result [][]PageItem
	for i := 0; i < len(items); i += pageSize {
		end := i + pageSize
		if end > len(items) {
			end = len(items)
		}
		result = append(result, items[i:end])
	}
	return result
}

func CreatePaginator(items []PageItem, pageSize int) {
	state := PaginatorState{
		PageNumber: 0,
		PageIndex:  0,
		Pages:      splitItems(items, pageSize),
		PageSize:   pageSize,
	}
	fmt.Println(state)
}
